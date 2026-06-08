DEBUG_MODE = True

import google.generativeai as genai
from services.embedding_service import generate_embedding
from config.settings import GEMINI_API_KEY
from services.keyword_search_service import keyword_search
from services.vectordb_service import search
from services.reranker_service import rerank

import re

def retrieve_context(question):
    print("RETRIEVE_CONTEXT CALLED")
    query_embedding = generate_embedding(question)

    vector_results = search(query_embedding)

    keyword_results = keyword_search(question)

    combined = []
    seen = set()

    for doc, metadata in zip(
        vector_results["documents"],
        vector_results["metadatas"]
    ):

        if doc not in seen:
            combined.append(
                {
                    "text": doc,
                    "metadata": metadata
                }
            )
            seen.add(doc)

    for doc in keyword_results:

        if doc["text"] not in seen:
            combined.append(
                {
                    "text":doc["text"],
                    "metadata":{
                        "page": doc["page"],
                        "source": doc["source"]
                    }
                }
            )
            seen.add(doc["text"])

    #----Re-ranking-----
    query_words = set(
        re.findall(r"\w+", question.lower())
    )

    scored_chunks = []

    for item in combined:

        score = 0

        doc_lower = item["text"].lower()

        for word in query_words:

            if word in doc_lower:
                score += 1

        scored_chunks.append(
            (item, score)
        )

    scored_chunks.sort(
        key=lambda x: x[1],
        reverse=True
    )

    combined = [
        item[0]
        for item in scored_chunks
    ]

    # Debug output
    print("\n===== HYBRID RESULTS =====")

    for idx, doc in enumerate(combined):

        print(f"\nCHUNK {idx + 1}")
        print(doc["text"][:300])
        print("----------------")

    print("Before rerank")
    ranked = rerank(
        question,
        combined
    )
    print("After rerank")
    print("\n===== RE-RANKED RESULTS =====")
    for doc in ranked[:5]:
        print(doc["text"][:200])
        print("----------------")

    return ranked[:5]


genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def generate_answer(question):
    chunks = retrieve_context(question)
    sources = []

    for chunk in chunks:
        metadata = chunk["metadata"]
        if metadata not in sources:
            sources.append(metadata)


    print("===== RETRIEVED CHUNKS =====")

    for chunk in chunks:
        print(chunk)
        print("--------------------")

    #Adding Inline citations
    context_parts = []

    for chunk in chunks:

        page = chunk["metadata"]["page"]

        context_parts.append(
            f"[PAGE {page}]\n{chunk['text']}"
        )

    context = "\n\n".join(context_parts)

    print("===== CONTEXT =====")
    print(context)
    if DEBUG_MODE:
        return {
            "answer": context,
            "sources": sources
        }

    prompt = f"""
You are a helpful assistant.

Answer ONLY using the provided context.

Whenever information comes from a page,
include the citation in this format:

[Page X]

Example:
A Flow Service is a service written in the
webMethods flow language [Page 198].

Rules:
1. Answer in clear sentences.
2. If information is missing, say:
   "I could not find that information in the uploaded documents."
3. Do not make up facts.
4. Cite source pages when possible.

Context:
{context}

Question:
{question}
"""
    print (prompt)
    response = model.generate_content(contents=prompt)

    return {
        "answer": response.text,
        "sources": sources
    }