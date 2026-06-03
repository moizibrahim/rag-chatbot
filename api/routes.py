from services.pdf_service import extract_pages
from services.chunk_service import create_chunks
from services.embedding_service import generate_embedding
from services.vectordb_service import (
    store_chunks,
    search
)
from services.rag_service import generate_answer
import os


def upload_document(pdf_path):

    pages = extract_pages(pdf_path)

    chunks = create_chunks(pages)

    embeddings = []

    for chunk in chunks:
        embeddings.append(
            generate_embedding(chunk["text"])
        )

    store_chunks(
        chunks,
        embeddings,
        os.path.basename(pdf_path)
    )


def ask_question(question):

    query_embedding = generate_embedding(
        question
    )

    results = search( query_embedding )

    answer = generate_answer(
        question,
        results["documents"]
    )

    return {
        "answer": answer,
        "sources": results["metadatas"],
        "debug_chunk": results["documents"][0]
    }