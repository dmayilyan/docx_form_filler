# docx_form_filler

Tool to automate form filling of docx document and followed by pdf creation based on REST API POST calls.

# How to use

Document should contain placeholders of the form `<foo>` where _foo_ is a key that should match json payload keys.

Payload should be of the form:

```shell
curl -X POST localhost:8085/generate_cert -H 'Content-type:application/json' -d '{"first_name":"Hans","rate":12,"date":"01.01.2021","input":"./input_docs/dummy_doc.docx","output":"./pdf_docs/foobar.pdf"}'
```

Where:
- `name`, `first_name`, `rate`, `date` are placeholder keys to be searched for in the document.
- `input` corresponds to input docx document.
- `output` corresponds to pdf output path with its filename.

**Make sure to clean formatting (especially in tags) before adding placeholders.**

