# Attach

# pdf.attach

A file that will be attached to the output PDF.

This can be used to distribute additional files associated with the PDF within it. PDF readers will display the files in a file listing.

Some international standards use this mechanism to attach machine-readable data (e.g., ZUGFeRD/Factur-X for invoices) that mirrors the visual content of the PDF.

## Example

```typst
#pdf.attach(
  "experiment.csv",
  relationship: "supplement",
  mime-type: "text/csv",
  description: "Raw Oxygen readings from the Arctic experiment",
)
```

## Notes

- This element is ignored if exporting to a format other than PDF.
- File attachments are not currently supported for PDF/A-2, even if the attached file conforms to PDF/A-1 or PDF/A-2.

```typst
#pdf.attach(
  path,
  data,
  relationship: none | str,
  mime-type: none | str,
  description: none | str
) -> content
```

## Parameters

- path:
  - description: The [path](/docs/reference/syntax/#paths) of the file to be attached. Must always be specified, but is only read from if no data is provided in the following argument.
  - type: str
  - default: None
- data:
  - description: Raw file data, optionally. If omitted, the data is read from the specified path.
  - type: bytes
  - default: None
- relationship:
  - description: The relationship of the attached file to the document. Ignored if export doesn\'t target PDF/A-3.
  - type: none | str
  - default: none
- mime-type:
  - description: The MIME type of the attached file.
  - type: none | str
  - default: none
- description:
  - description: A description for the attached file.
  - type: none | str
  - default: none


