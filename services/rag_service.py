DEBUG_MODE = True

import google.generativeai as genai
from services.embedding_service import generate_embedding
from config.settings import GEMINI_API_KEY
from services.keyword_search_service import keyword_search
from services.vectordb_service import search

import re

def retrieve_context(question):

    query_embedding = generate_embedding(question)

    vector_results = search(query_embedding)

    keyword_results = keyword_search(question)

    combined = []
    seen = set()

    for doc in vector_results["documents"]:

        if doc not in seen:
            combined.append(doc)
            seen.add(doc)

    for doc in keyword_results:

        if doc["text"] not in seen:
            combined.append(doc["text"])
            seen.add(doc["text"])

    #----Re-ranking-----
    query_words = set(
        re.findall(r"\w+", question.lower())
    )

    scored_chunks = []

    for doc in combined:

        score = 0

        doc_lower = doc.lower()

        for word in query_words:

            if word in doc_lower:
                score += 1

        scored_chunks.append(
            (doc, score)
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
        print(doc[:300])
        print("----------------")

    return combined[:5]


genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def generate_answer(question):
    chunks = retrieve_context(question)

    print("===== RETRIEVED CHUNKS =====")

    for chunk in chunks:
        print(chunk)
        print("--------------------")

    context = "\n\n".join(chunks)
    print("===== CONTEXT =====")
    print(context)
    if DEBUG_MODE:
        return context

    prompt = f"""
You are a helpful assistant.

Answer ONLY using the provided context.

If the answer is not present in the context, say:
'I could not find that information in the uploaded documents.'

Context:
{context}

Question:
{question}
"""
    print (prompt)
    response = model.generate_content(contents=prompt)

    return response.text