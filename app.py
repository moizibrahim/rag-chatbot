import streamlit as st
import os

os.makedirs("uploads", exist_ok=True)

from api.routes import (
    upload_document,
    ask_question
)

st.title(
    "Enterprise RAG Chatbot"
)

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:

    file_path = (
        f"uploads/{uploaded_file.name}"
    )

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    upload_document(file_path)

    st.success(
        "Document processed successfully"
    )

question = st.text_input(
    "Ask Question"
)

if st.button("Ask"):

    result = ask_question(question)

    st.subheader("Answer")

    st.write(result["answer"])

    st.subheader("Sources")

    for source in result["sources"]:

        st.write(
            f'{source["source"]} - Page {source["page"]}'
        )