from rank_bm25 import BM25Okapi
import re

bm25 = None
documents = []


def build_index(chunks):

    global bm25
    global documents

    documents = chunks

    tokenized_docs = [
        re.findall(r"\w+", chunk["text"].lower())
        for chunk in chunks
    ]

    bm25 = BM25Okapi(tokenized_docs)


def keyword_search(query, top_k=3):

    global bm25
    global documents

    tokenized_query = re.findall(r"\w+", query.lower())

    scores = bm25.get_scores(tokenized_query)

    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        item[0]
        for item in ranked[:top_k]
    ]