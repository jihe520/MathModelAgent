# 内置模板

用户提供的 `Conference-LaTeX-template_10-17-19` 目录已原样放入 `assets/ieee-conference-2019/`，保留原文件中的声明和许可文字：

- `conference_101719.tex`：IEEE conference 示例源码。
- `IEEEtran.cls`：IEEEtran 类文件，V1.8b（2015）。
- `fig1.png`：示例源码的图件依赖，不能作为用户研究结果。
- `conference_101719.pdf`：原模板预览。
- `IEEEtran_HOWTO.pdf`：类文件使用说明。

这是用户提供的 2019 模板快照，不代表已核验为任何目标会议的最新要求。文件 SHA-256 存于 `assets/template-sha256.json`，便于检查拷贝完整性。技能和复制脚本不依赖原机器上的下载路径。

初始化脚本将示例源码复制为 `main.tex`，同时复制类文件和示例图。转换论文时替换所有示例内容，移除不再使用的 `fig1.png`。根据新稿实际需要添加 bib、图件及少量必要宏包，不修改 `IEEEtran.cls` 来挤页数。

默认入口是 `\documentclass[conference]{IEEEtran}`。作者匿名、纸张尺寸、版权行、页数上限等以目标会议要求为准。没有要求时使用模板默认设置并在改稿说明中记录；不要凭空添加版权号、基金或 DOI。

通常用 pdfLaTeX 编译英文正文；当确有 Unicode/字体需求时按环境选择其他引擎。内置编辑器可能无法访问项目外部图件或额外文件，应使用完整项目编译结果判断交付质量。无法编译时明确告知而不伪造成功记录。
