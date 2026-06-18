---
name: doctor
description: "环境检查与安装向导。检查数学建模工作流所需的全部依赖是否已安装，对缺失项提供安装命令，并在用户确认后执行安装。手动触发。"
allowed-tools: Bash(*), Read, Write
---

# Doctor — 环境检查与安装向导

本 skill 检查完整数学建模工作流所需的所有工具是否已就绪，并帮助用户安装缺失项。**本 skill 只在用户显式触发时运行，不自动执行。**

## 检查项清单

### 核心工具

| 工具 | 用途 | 检测命令 |
| --- | --- | --- |
| `typst` | 论文编译（5writing、6verity，Typst 引擎） | `command -v typst` |
| `xelatex` | 论文编译（5writing、6verity，LaTeX 引擎，中文模板必需） | `command -v xelatex` |
| `python3` | 数值计算与图表（3coding-visual） | `command -v python3` |
| `drawio` / `draw.io` | DrawIO 流程图导出 PDF（4drawio） | `command -v drawio \|\| command -v draw.io` |
| `pdftoppm` | PDF 转 PNG 视觉检查（6verity） | `command -v pdftoppm` |
| `mutool` | PDF 转 PNG 备用（6verity） | `command -v mutool` |
| `magick` | PDF 转 PNG 备用（6verity） | `command -v magick` |

### Python 包

| 包 | 用途 |
| --- | --- |
| `numpy` | 数值计算 |
| `scipy` | 科学计算、优化求解 |
| `pandas` | 数据处理 |
| `matplotlib` | 图表生成 |
| `scikit-learn` | 机器学习建模 |
| `openpyxl` | 读写 Excel 数据附件 |

## 工作流程

### Step 1：检测当前平台

```bash
case "$(uname -s)" in
  Darwin) echo "PLATFORM=mac" ;;
  Linux)  echo "PLATFORM=linux" ;;
  MINGW*|MSYS*|CYGWIN*) echo "PLATFORM=windows" ;;
  *)      echo "PLATFORM=unknown" ;;
esac
```

Windows 下优先使用 winget，备用 scoop 或 choco。Linux 下优先使用 apt（Debian/Ubuntu），备用 dnf（Fedora/RHEL）或 pacman（Arch）。  
检测包管理器：

```bash
# Linux 发行版检测
if [ -f /etc/os-release ]; then
  . /etc/os-release
  echo "DISTRO=$ID"
fi
# Windows 包管理器检测（在 Git Bash / PowerShell 中）
command -v winget >/dev/null 2>&1 && echo "PKG=winget"
command -v scoop  >/dev/null 2>&1 && echo "PKG=scoop"
command -v choco  >/dev/null 2>&1 && echo "PKG=choco"
```

### Step 2：检查所有工具

```bash
check_cmd() {
  if command -v "$1" >/dev/null 2>&1; then
    echo "OK  $1 ($(command -v "$1"))"
  else
    echo "MISS $1"
  fi
}

check_cmd typst
check_cmd xelatex
check_cmd python3 || check_cmd python   # Windows 上可能是 python
command -v drawio >/dev/null 2>&1 || command -v draw.io >/dev/null 2>&1 \
  && echo "OK  drawio" || echo "MISS drawio"
check_cmd pdftoppm
check_cmd mutool
check_cmd magick

python3 - <<'PYEOF'
import importlib
pkgs = ["numpy", "scipy", "pandas", "matplotlib", "sklearn", "openpyxl"]
for p in pkgs:
    try:
        importlib.import_module(p)
        import importlib.metadata as meta
        try:
            ver = meta.version(p if p != "sklearn" else "scikit-learn")
        except Exception:
            ver = "?"
        print(f"OK  {p} ({ver})")
    except ImportError:
        print(f"MISS {p}")
PYEOF
```

### Step 3：输出检查报告

将结果整理展示：

```
状态   工具/包              说明
----   --------             ----
✓      typst 0.13.0         论文编译
✗      drawio               DrawIO 导出 PDF（可选）
✓      python3 3.11.x       数值计算
✗      scipy                科学计算（可选）
...
```

**必须项：** typst 或 xelatex（至少一个论文编译器）、python3、numpy、pandas、matplotlib  
**可选项：** drawio、pdftoppm/mutool/magick 三选一、scipy、scikit-learn、openpyxl

### Step 4：提供安装命令（按平台）

仅对缺失项输出对应平台的命令。

#### typst

| 平台 | 命令 |
| --- | --- |
| macOS | `brew install typst` |
| Linux (apt) | `snap install typst` 或从 GitHub Releases 下载二进制 |
| Linux (arch) | `pacman -S typst` |
| Windows (winget) | `winget install Typst.Typst` |
| Windows (scoop) | `scoop install typst` |
| 通用 | `cargo install --locked typst-cli`（需要 Rust） |

#### xelatex（TeX 发行版）

xelatex 包含在主流 TeX 发行版中（TeX Live / MiKTeX / MacTeX）。安装发行版即可获得 xelatex。

| 平台 | 命令 |
| --- | --- |
| macOS | `brew install --cask mactex` 或 `brew install texlive` |
| Linux (apt) | `sudo apt install texlive-full` |
| Linux (dnf) | `sudo dnf install texlive-scheme-full` |
| Linux (arch) | `sudo pacman -S texlive` |
| Windows (winget) | `winget install MiKTeX.MiKTeX` 或 `winget install TeXLive` |
| Windows (scoop) | `scoop install latex`（需先添加 extras bucket） |

注意：`texlive-full` 体积较大（约 5GB），如需精简可只装 `texlive-xetex` + `texlive-lang-chinese`（中文支持）。

#### Python 3

| 平台 | 命令 |
| --- | --- |
| macOS | `brew install python` |
| Linux (apt) | `sudo apt install python3 python3-pip` |
| Linux (dnf) | `sudo dnf install python3 python3-pip` |
| Windows | `winget install Python.Python.3` 或从 python.org 下载安装包 |

#### Python 包（批量安装缺失项）

```bash
pip3 install <缺失的包>
# Windows: pip install <缺失的包>
# 例如: pip3 install scipy scikit-learn openpyxl
```

#### drawio

| 平台 | 命令 |
| --- | --- |
| macOS | `brew install --cask drawio` |
| Linux | 从 https://github.com/jgraph/drawio-desktop/releases 下载 AppImage 或 deb |
| Windows | `winget install JGraph.Draw` 或从上述页面下载安装包 |

#### pdftoppm（来自 poppler）

| 平台 | 命令 |
| --- | --- |
| macOS | `brew install poppler` |
| Linux (apt) | `sudo apt install poppler-utils` |
| Linux (dnf) | `sudo dnf install poppler-utils` |
| Windows | `winget install oschwartz10612.poppler` 或 `scoop install poppler` |

#### mutool（来自 mupdf）

| 平台 | 命令 |
| --- | --- |
| macOS | `brew install mupdf` |
| Linux (apt) | `sudo apt install mupdf-tools` |
| Windows | `scoop install mupdf` 或从 mupdf.com 下载 |

#### ImageMagick

| 平台 | 命令 |
| --- | --- |
| macOS | `brew install imagemagick` |
| Linux (apt) | `sudo apt install imagemagick` |
| Linux (dnf) | `sudo dnf install imagemagick` |
| Windows | `winget install ImageMagick.ImageMagick` 或 `choco install imagemagick` |

### Step 5：询问用户是否安装

列出所有缺失的**必须项**后，询问用户：

> 以上必须项缺失，是否现在安装？(y/N)

- 若用户确认，按检测到的平台依次执行安装命令，每步完成后打印结果。
- 若用户拒绝或只有可选项缺失，打印可手动执行的命令列表并退出。
- 安装完成后重新运行 Step 2，确认已生效。

### Step 6：最终摘要

```
Doctor 检查完成（macOS）
必须项：5/5 ✓
可选项：2/4（drawio、scipy 缺失）

工作流就绪状态：
  1start-mathmodel   ✓
  2analysis-modeling ✓
  3coding-visual     ✓（scipy 缺失，部分功能受限）
  4drawio            ⚠ drawio 未安装，PDF 导出将跳过
  5writing           ✓（typst ✓，xelatex ✓）
  6verity            ⚠ 无 PDF 转 PNG 工具，视觉检查将跳过
```

## 注意事项

- 执行安装前必须获得用户明确确认，不得静默安装。
- Windows 下建议在 PowerShell（管理员）或 Git Bash 中运行，部分命令需要管理员权限。
- Linux 的 `sudo` 命令会请求密码，执行前告知用户。
- drawio 和 PDF 转 PNG 工具缺失不影响核心工作流，仅影响导出质量。
- 如平台检测为 unknown，打印所有平台命令供用户手动选择。
