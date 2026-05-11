"""CLI 显示工具模块，提供 ASCII 横幅和终端居中显示功能。"""

from textwrap import dedent


def center_cli_str(text: str, width: int | None = None):
    """将多行文本在终端中居中显示。

    Args:
        text: 待居中的多行文本。
        width: 终端宽度，默认自动检测。
    """
    import shutil

    width = width or shutil.get_terminal_size().columns
    lines = text.split("\n")
    max_line_len = max(len(line) for line in lines)
    return "\n".join(
        (line + " " * (max_line_len - len(line))).center(width) for line in lines
    )


def get_ascii_banner(center: bool = True) -> str:
    """获取项目 ASCII 横幅。

    Args:
        center: 是否居中显示。

    Returns:
        ASCII 横幅字符串。
    """
    text = dedent(
        r"""
        ===============================================================================
         __  __       _   _     __  __           _      _                          _   
        |  \/  |     | | | |   |  \/  |         | |    | |   /\                   | |  
        | \  / | __ _| |_| |__ | \  / | ___   __| | ___| |  /  \   __ _  ___ _ __ | |_ 
        | |\/| |/ _` | __| '_ \| |\/| |/ _ \ / _` |/ _ \ | / /\ \ / _` |/ _ \ '_ \| __|
        | |  | | (_| | |_| | | | |  | | (_) | (_| |  __/ |/ ____ \ (_| |  __/ | | | |_ 
        |_|  |_|\__,_|\__|_| |_|_|  |_|\___/ \__,_|\___|_/_/    \_\__, |\___|_| |_|\__|
                                                                    __/ |               
                                                                |___/                
        ===============================================================================
        """,
    ).strip()
    if center:
        return center_cli_str(text)
    else:
        return text
