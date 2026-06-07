from services.pdf_service import extract_pages
from services.chunk_service import create_chunks
from services.embedding_service import generate_embedding
from services.vectordb_service import (
    store_chunks,
    search
)
from services.rag_service import generate_answer
from services.keyword_search_service import build_index
import os
import time

def upload_document(pdf_path):

    start = time.time()

    pages = extract_pages(pdf_path)
    print("PDF Extraction:", time.time() - start)

    chunks = create_chunks(pages)
    print("Chunking:", time.time() - start)
    print("PDF:", os.path.basename(pdf_path))
    print("Total Pages:", len(pages))
    print("Total Chunks:", len(chunks))

    start = time.time()

    embeddings = []

    for chunk in chunks:
        embeddings.append(
            generate_embedding(chunk["text"])
        )
    print("Embedding:", time.time() - start)

    start = time.time()
    store_chunks(
        chunks,
        embeddings,
        os.path.basename(pdf_path)
    )
    print("chromaDB:", time.time() - start)

    build_index(chunks)


def ask_question(question):

    answer = generate_answer(question)

    return {
        "answer": answer,
        "sources": []
    }