from services.pdf_service import extract_pages

pages = extract_pages("uploads/Mohammed_Ibrahim_Moiz_Resume_A.pdf")

for page in pages:
    print(page["text"])