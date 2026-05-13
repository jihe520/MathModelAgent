#!/usr/bin/env bash
# PostToolUse hook: 根据修改的文件路径运行对应的 lint 检查

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# 读取 stdin JSON，用 sed 提取 file_path（避免 jq 吞掉 Windows 反斜杠）
input=$(cat)
file=$(echo "$input" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
# 将 Windows 反斜杠转为正斜杠，并合并连续斜杠
file=$(echo "$file" | sed 's/\\/\//g' | tr -s '/')
[[ -z "$file" ]] && exit 0
file=$(echo "$file" | xargs)

# 去掉 REPO_ROOT 前缀得到相对路径
# REPO_ROOT 格式：/c/Users/...（Git Bash），文件路径格式：C:/Users/...（Windows）
norm_root="$REPO_ROOT"
if [[ "$norm_root" =~ ^/([a-zA-Z])/(.*) ]]; then
    drive="${BASH_REMATCH[1]}"
    rest="${BASH_REMATCH[2]}"
    drive="${drive^^}"
    norm_root="${drive}:/${rest}"
fi
if [[ "$file" == "$norm_root"/* ]]; then
    file="${file#$norm_root/}"
elif [[ "$file" == "$norm_root"* ]]; then
    file="${file#$norm_root}"
    file="${file#/}"
elif [[ "$file" == "$REPO_ROOT"/* ]]; then
    file="${file#$REPO_ROOT/}"
elif [[ "$file" == "$REPO_ROOT"* ]]; then
    file="${file#$REPO_ROOT}"
    file="${file#/}"
fi

run_check() {
    local output
    local exit_code=0
    output=$("$@" 2>&1) || exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        echo "$output" >&2
        exit 2
    fi
}

case "$file" in
    backend/*.py)
        cd "$REPO_ROOT/backend" || exit 0
        export PYTHONIOENCODING=utf-8
        run_check ./.venv/Scripts/python.exe -m ruff check app/
        ;;
    frontend/src/*.vue|frontend/src/*.ts|frontend/src/*/*.vue|frontend/src/*/*.ts|frontend/src/*/*/*.vue|frontend/src/*/*/*.ts|frontend/src/*/*/*/*.vue|frontend/src/*/*/*/*.ts)
        cd "$REPO_ROOT/frontend" || exit 0
        # 去掉 frontend/ 前缀，因为已经 cd 到 frontend 目录
        rel_file="${file#frontend/}"
        run_check npx biome check "$rel_file"
        ;;
esac

exit 0
