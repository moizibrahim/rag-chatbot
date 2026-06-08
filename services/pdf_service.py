from pypdf import PdfReader
from services.text_cleaner import remove_repeated_headers

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
    pages = remove_repeated_headers(pages)

    return pages