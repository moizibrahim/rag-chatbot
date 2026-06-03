from pypdf import PdfReader

def extract_pages(pdf_path):

    reader = PdfReader(pdf_path)

    pages = []

    for idx, page in enumerate(reader.pages):

        pages.append(
            {
                "page": idx + 1,
                "text": page.extract_text()
            }
        )

    return pages