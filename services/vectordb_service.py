import uuid
import chromadb

client = chromadb.PersistentClient(
    path="db/chroma_db"
)

collection = client.get_or_create_collection(
    name="documents"
)
def clear_collection():

    global collection

    client.delete_collection(
        name="documents"
    )

    collection = client.get_or_create_collection(
        name="documents"
    )

    print("Collection cleared")

def store_chunks(chunks, embeddings, source_file):

    ids = []
    documents = []
    metadatas = []

    for chunk, embedding in zip(chunks, embeddings):

        ids.append(str(uuid.uuid4()))

        documents.append(chunk["text"])

        metadatas.append(
            {
                "source": source_file,
                "page": chunk["page"]
            }
        )

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )


def search(query_embedding):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    print("\n===== FIRST RETRIEVED DOCUMENT =====")
    print(results["documents"][0][0][:1000])

    print("\n===== FIRST METADATA =====")
    print(results["metadatas"][0][0])

    return {
        "documents": results["documents"][0],
        "metadatas": results["metadatas"][0]
    }