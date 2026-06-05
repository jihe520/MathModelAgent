#set document(title: "[论文标题]", author: ())
#let song-font = ("Songti SC", "STSong", "Times New Roman")
#let hei-font = ("Heiti SC", "STHeiti", "Songti SC")
#let kai-font = ("Kaiti SC", "STKaiti", "Songti SC")
#let title-font = ("FZXiaoBiaoSong-B05S", "Songti SC", "STSong")
#let fang-font = ("FangSong_GB2312", "STFangsong", "Songti SC")
#let cn-numbering(..nums) = {
  let ns = nums.pos()
  if ns.len() == 1 {
    numbering("一、", ns.at(0))
  } else if ns.len() == 2 {
    [（#numbering("一", ns.at(1))）]
  } else {
    numbering("1.", ns.at(2))
  }
}
#set page(
  paper: "a4",
  margin: (top: 2.54cm, bottom: 2.54cm, left: 3.17cm, right: 3.17cm),
  numbering: none,
)
#set text(font: song-font, size: 10.5pt, lang: "zh")
#set par(
  first-line-indent: (amount: 2em, all: true),
  justify: true,
  leading: 1.05em,
  spacing: 0.35em,
)
#set heading(numbering: cn-numbering)
#set enum(numbering: "1.", spacing: 0.48em)
#show heading.where(level: 1): it => block(above: 1.2em, below: 0.42em)[#align(
  left,
)[#text(font: hei-font, size: 15pt, weight: "bold")[#it]]]
#show heading.where(level: 2): it => block(above: 0.9em, below: 0.65em, inset: (
  left: 2em,
))[
  #text(font: kai-font, size: 14pt)[#it]
]
#show heading.where(level: 3): it => block(above: 0.8em, below: 0.48em, inset: (
  left: 2em,
))[
  #text(font: song-font, size: 10.5pt, weight: "bold")[#it]
]
#show figure.caption: it => text(size: 9pt)[#it]

#let song = body => text(font: song-font, body)
#let hei = body => text(font: hei-font, weight: "bold", body)
#let kai = body => text(font: kai-font, body)
#let line-field(body, width: 8cm) = box(width: width)[
  #align(center)[#body]
  #v(-0.15em)
  #line(length: 100%, stroke: 0.55pt)
]
#let tight-title(body, size: 18pt) = align(center)[#text(
  font: title-font,
  size: size,
  weight: "bold",
)[#body]]
#let keywords-cn(body) = block(above: 0.85em)[#text(
    font: hei-font,
    weight: "bold",
  )[关键词：]#body]
#let numbered-page() = {
  pagebreak()
}
#let toc-page() = {
  align(center)[#text(
    font: hei-font,
    size: 14pt,
    weight: "bold",
  )[目 #h(1em) 录]]
  v(1.7em)
  set text(size: 10.5pt)
  let entry(title, page, indent: 0pt) = block(below: 0.86em)[
    #grid(
      columns: (auto, 1fr, auto),
      column-gutter: 0.45em,
      inset: (left: indent),
      title, repeat[.], page,
    )
  ]
  entry([摘要], [2])
  entry([Abstract], [3])
  entry([表格与插图清单], [5])
  entry([一、引言], [6])
  entry([（一）研究背景], [6], indent: 2em)
  entry([（二）研究目标], [6], indent: 2em)
  entry([二、方法], [6])
  entry([（一）统计模型], [6], indent: 2em)
  entry([（二）参数估计], [6], indent: 2em)
  entry([三、数据], [6])
  entry([（一）数据来源], [6], indent: 2em)
  entry([（二）数据预处理], [6], indent: 2em)
  entry([四、分析与建模], [6])
  entry([五、结果], [6])
  entry([六、结论], [6])
  entry([参考文献], [6])
  entry([附录], [6])
  entry([致谢], [6])
  pagebreak()
}
#let references-cn() = [
  = 参考文献
  #include "references.typ"
]
#let appendix-cn(file: "sections/A_code.typ") = [
  = 附录
  #include (file)
]

#let three-line-table(caption, columns, header, body, inset: (x: 0.35em, y: 0.52em), cell-align: center) = {
  let col-count = header.len()
  let body-rows = calc.floor(body.len() / col-count)
  let bottom-y = body-rows + 1
  let styled-header = header.map(cell => strong(cell))

  block(width: 100%, breakable: false)[
    #align(center)[
      #box[
        #align(center)[#text(font: hei-font, size: 10.5pt, weight: "bold")[#caption]]
        #v(0.6em)
        #table(
          columns: columns,
          align: cell-align,
          stroke: none,
          inset: inset,
          table.hline(y: 0, stroke: 0.8pt),
          table.hline(y: 1, stroke: 0.5pt),
          table.hline(y: bottom-y, stroke: 0.8pt),
          ..styled-header,
          ..body,
        )
      ]
    ]
  ]
}

#text(font: hei-font, size: 15pt, weight: "bold")[作品编号：TJJM]
#v(5.7cm)
#align(center)[
  #text(
    font: title-font,
    size: 18pt,
    weight: "bold",
  )[[竞赛年份]年（第[届数]届）全国大学生统计建模大赛]
  #v(22pt)
  #text(
    font: title-font,
    size: 26pt,
  )[参 #h(0.55em) 赛 #h(0.55em) 作 #h(0.55em) 品]
]
#v(4.4cm)
#align(center)[
  #set text(font: fang-font, size: 15pt)
  #grid(
    columns: (3.0cm, 8.5cm),
    row-gutter: 0.75em,
    [#align(right)[参赛学校：]], [#line-field([学校名称], width: 9cm)],
    [#align(right)[论文题目：]], [#line-field([论文标题], width: 9cm)],
    [#align(right)[参赛队员：]],
    [#line-field([队员1  队员2  队员3], width: 9cm)],

    [#align(right)[指导老师：]], [#line-field([指导老师], width: 9cm)],
  )
]

#numbered-page()
#set page(
  numbering: "1",
  footer: align(center)[#text(size: 10.5pt)[#context counter(page).display()]],
)
#align(center)[#text(font: title-font, size: 16pt, weight: "bold")[[论文标题]]]
#v(1.0em)
#align(center)[#text(font: hei-font, size: 14pt, weight: "bold")[摘要]]
#v(0.4em)
[中文摘要内容：500-700字]
#keywords-cn([[关键词1]；[关键词2]；[关键词3]；[关键词4]；[关键词5]])

#pagebreak()
#align(center)[#text(size: 14pt, weight: "bold")[Abstract]]
#v(0.4em)
[English abstract, 350-500 words]
#v(0.5em)
#text(weight: "bold")[Keywords:] [keyword1]; [keyword2]; [keyword3]; [keyword4]; [keyword5]

#pagebreak()
#toc-page()

#align(center)[#text(
  font: hei-font,
  size: 14pt,
  weight: "bold",
)[表格与插图清单]]
#v(1em)
#set par(first-line-indent: 0pt, leading: 1.15em, spacing: 0.35em)
表1.解释变量定义及其与居民消费的关系

表2.KMO和Bartlett球形检验结果

表3.时序全局主成分分析解释率

表4.时序全局主成分分析解释率

表5.时序全局主成分分析解释率

表6.时序全局主成分分析解释率

表7.时序全局主成分分析解释率

表8.性能评估指标

图1.流程图

图2.代表变量时间趋势图

图3.代表变量密度图
#pagebreak()

#counter(heading).update(0)
#set par(
  first-line-indent: (amount: 2em, all: true),
  justify: true,
  leading: 1.05em,
  spacing: 0.35em,
)
#align(center)[#text(font: title-font, size: 16pt, weight: "bold")[[论文标题]]]
#v(0.8em)

#include "sections/1_introduction.typ"
#include "sections/2_method.typ"
#include "sections/3_data.typ"
#include "sections/4_analysis.typ"
#include "sections/5_results.typ"
#include "sections/6_conclusion.typ"

#references-cn()
#v(1.2em)
#align(center)[#text(font: hei-font, size: 14pt, weight: "bold")[附录]]
#v(0.8em)
[附录内容：核心代码、补充表格等]
#include "sections/A_code.typ"

#v(1.2em)
#align(center)[#text(font: hei-font, size: 14pt, weight: "bold")[致谢]]
#v(0.8em)
[致谢内容]
