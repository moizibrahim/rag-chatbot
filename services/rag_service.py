import google.generativeai as genai

from config.settings import GEMINI_API_KEY

genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def generate_answer(question, chunks):

    print("===== RETRIEVED CHUNKS =====")

    for chunk in chunks:
        print(chunk)
        print("--------------------")

    context = "\n\n".join(chunks)
    print("===== CONTEXT =====")
    print(context)

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