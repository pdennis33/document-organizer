# document-organizer
Uses OCR and Machine Learning to classify and organize scanned documents

## Known Issues
- If you start with PDFs and use `save_pdf_single_pages` to split them into single pages, and then use `convert_pdfs_to_image.py` to convert the single pages to images, it results in OCR processing errors when running `extract_text_from_images.py`. The cause needs to be investigated further, but the workaround is to scan directly to images instead of PDFs. Because of this behavior, best guesses for reasons for the issues are:
  - The PDFs are not scanned at a high enough resolution
  - The PDF-to-image conversion is not working properly or is not using a high enough resolution
