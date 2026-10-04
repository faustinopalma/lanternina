#let data = json("source.json")
#let layout = data.layout
#set document(title: data.title)
#set page(paper: "a4", margin: (top: 16mm, bottom: 17mm, x: 17mm),
  footer: context align(right, text(size: 9pt, counter(page).display())))
#set text(font: "Libertinus Serif", size: 13pt, lang: data.language)
#set par(leading: 0.55em, spacing: layout.spacing * 1mm)
#set enum(indent: 8mm, body-indent: 2mm, spacing: 2.5mm, tight: false)
#let instructions() = {
  for paragraph in data.paragraphs { text(paragraph); parbreak() }
  enum(..data.steps.map(step => text(step)))
  for note in data.note { parbreak(); text(size: 12pt, note) }
}
#let material() = {
  if data.diagram != none {
    let diagram = data.diagram
    if diagram.kind == "grid" {
      if data.grid-field != "" { text(size: 12pt, weight: "bold", data.grid-field); v(3mm) }
      let cell = calc.min(165 / diagram.columns,
        (if layout.expanded { 110 } else { 85 }) / diagram.row_count) * 1mm
      align(center, grid(columns: (cell,) * diagram.columns,
        rows: (cell,) * diagram.row_count, gutter: 0pt,
        ..range(diagram.columns * diagram.row_count).map(index => rect(
          width: cell, height: cell, stroke: 0.5pt,
          fill: if calc.rem(index, diagram.columns) < diagram.split_at {
            white
          } else { luma(94%) }))))
    } else if diagram.kind == "table" {
      let rows = diagram.rows
      if layout.split == "table" and rows.len() > layout.table-break {
        table(columns: rows.first().len(), inset: 3mm, stroke: 0.5pt,
          ..rows.slice(0, layout.table-break).flatten().map(cell => text(size: 12pt, cell)))
        pagebreak()
        text(size: 20pt, data.title)
        v(5mm)
        table(columns: rows.first().len(), inset: 3mm, stroke: 0.5pt,
          ..(rows.slice(0, 1) + rows.slice(layout.table-break)).flatten().map(cell => text(size: 12pt, cell)))
      } else {
        table(columns: rows.first().len(), inset: 3mm, stroke: 0.5pt,
          ..rows.flatten().map(cell => text(size: 12pt, cell)))
      }
    }
    for label in diagram.labels { parbreak(); text(label) }
  } else if data.illustrated {
    image("illustration.png", width: 100%, height: layout.image * 1mm, fit: "contain")
  }
}
#let response-space(space) = block(breakable: false, above: 5mm, width: 100%)[
  #text(size: 12pt, weight: "bold", space.label)
  #v(3mm)
  #if space.room == "a_box" {
    rect(width: 100%, height: if layout.expanded { 52mm } else { 38mm }, stroke: 0.5pt)
  } else if space.room == "some_lines" {
    for row in range(if layout.split == "table" { 4 } else { 3 }) {
      block(width: 100%, height: if layout.expanded { 12mm } else { 9mm },
        above: 0pt, below: 0pt, stroke: (bottom: 0.5pt))
    }
  } else {
    v(if layout.expanded { 14mm } else { 10mm })
    line(length: 100%, stroke: 0.5pt)
  }
]
#let spaces = data.spaces.filter(space => space.label != data.grid-field)
#line(length: 100%, stroke: 1pt)
#v(5mm)
#text(size: 27pt, data.title)
#v(7mm)
#if layout.split == "workbook" {
  align(center, block(width: layout.reading * 1mm)[#set align(left)
    #instructions()
  ])
} else { instructions() }
#v(4mm)
#if layout.split in ("workspace", "workbook") { pagebreak(); text(size: 20pt, data.title); v(5mm) }
#material()
#if layout.split == "responses" { pagebreak(); text(size: 20pt, data.title); v(5mm) }
#if spaces.len() >= 4 {
  grid(columns: (1fr, 1fr), column-gutter: 8mm, row-gutter: 5mm,
    ..spaces.map(response-space))
} else { for space in spaces { response-space(space) } }