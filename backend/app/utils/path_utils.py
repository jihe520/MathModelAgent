"""Path validation helpers used by task and file operations."""

import ntpath
import os
import re
from pathlib import Path


TASK_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


def ensure_safe_task_id(task_id: str) -> str:
    """Validate a task ID before using it as a directory name."""
    normalized = (task_id or "").strip()
    if not normalized or not TASK_ID_PATTERN.fullmatch(normalized):
        raise ValueError("非法 task_id")
    return normalized


def ensure_safe_path_component(value: str, field_name: str = "路径组件") -> str:
    """Validate a single cross-platform path component.

    Absolute paths, drive-qualified paths, separators, traversal markers, and
    control characters are rejected instead of silently normalizing them.
    """
    normalized = (value or "").strip()
    drive, _ = ntpath.splitdrive(normalized)
    has_control_character = any(ord(character) < 32 for character in normalized)

    if (
        not normalized
        or normalized in {".", ".."}
        or drive
        or os.path.isabs(normalized)
        or "/" in normalized
        or "\\" in normalized
        or has_control_character
    ):
        raise ValueError(f"非法{field_name}")

    return normalized


def resolve_path_within(
    base_dir: str | os.PathLike[str],
    component: str,
    field_name: str = "文件名",
) -> Path:
    """Resolve one path component and guarantee it stays inside ``base_dir``."""
    safe_component = ensure_safe_path_component(component, field_name)
    resolved_base = Path(base_dir).resolve()
    resolved_path = (resolved_base / safe_component).resolve()

    try:
        resolved_path.relative_to(resolved_base)
    except ValueError as exc:
        raise ValueError(f"非法{field_name}") from exc

    return resolved_path
