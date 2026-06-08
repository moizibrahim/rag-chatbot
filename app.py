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

if "current_file" not in st.session_state:
    st.session_state.current_file = None

if "document_processed" not in st.session_state:
    st.session_state.document_processed = False

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)
if uploaded_file:

    if st.session_state.current_file != uploaded_file.name:

        st.session_state.current_file = uploaded_file.name
        st.session_state.document_processed = False

    if not st.session_state.document_processed:

        file_path = f"uploads/{uploaded_file.name}"

        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        upload_document(file_path)

        st.session_state.document_processed = True

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

        st.markdown(
            f'{source.get("source","Unknown")} - Page {source.get("page","?")}'
        )