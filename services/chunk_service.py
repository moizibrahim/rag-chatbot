import re

def create_chunks(
    pages,
    chunk_size=1000,
    overlap=200
):

    chunks = []

    for page_data in pages:

        page_number = page_data["page"]

        text = page_data["text"]

        if not text:
            continue

        # Remove excessive whitespace
        text = re.sub(
            r"\s+",
            " ",
            text
        ).strip()

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end]

            # Skip tiny chunks
            if len(chunk_text.strip()) < 100:
                start += chunk_size - overlap
                continue

            # Skip probable TOC chunks
            dot_count = chunk_text.count("....")

            if dot_count > 5:
                start += chunk_size - overlap
                continue

            chunks.append(
                {
                    "text": chunk_text,
                    "page": page_number
                }
            )

            start += (
                chunk_size - overlap
            )

    return chunks