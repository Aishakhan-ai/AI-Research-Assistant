
import streamlit as st
import requests
import numpy as np
from pypdf import PdfReader
from io import BytesIO

# Configuration
CHAT_MODEL = "llama3.2:1b"
EMBED_MODEL = "nomic-embed-text"
OLLAMA_URL = "http://localhost:11434"

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🤖"
)

st.title("🤖 AI Research Assistant")
st.write("Chat with your research papers using RAG.")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "embeddings" not in st.session_state:
    st.session_state.embeddings = []

if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = ""


# Split PDF text into smaller sections
def split_text(text, chunk_size=1000, overlap=150):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# Create embeddings using Ollama
def get_embedding(text):
    response = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={
            "model": EMBED_MODEL,
            "prompt": text
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()["embedding"]


# Retrieve relevant sections
def retrieve_chunks(question, chunks, embeddings, top_k=4):
    question_embedding = np.array(
        get_embedding(question)
    )

    vectors = np.array(embeddings)

    similarities = np.dot(
        vectors,
        question_embedding
    ) / (
        np.linalg.norm(vectors, axis=1)
        * np.linalg.norm(question_embedding)
        + 1e-10
    )

    best_indices = np.argsort(similarities)[-top_k:][::-1]

    return best_indices.tolist()


# Upload PDF
uploaded_file = st.file_uploader(
    "Upload a research paper (PDF)",
    type=["pdf"]
)

if uploaded_file:
    if st.button("Process PDF"):
        try:
            reader = PdfReader(
                BytesIO(uploaded_file.getvalue())
            )

            full_text = ""

            for page in reader.pages:
                full_text += page.extract_text() or ""

            if not full_text.strip():
                st.error("No readable text found in this PDF.")

            else:
                chunks = split_text(full_text)
                embeddings = []

                progress = st.progress(0)

                for i, chunk in enumerate(chunks):
                    embeddings.append(get_embedding(chunk))
                    progress.progress((i + 1) / len(chunks))

                st.session_state.chunks = chunks
                st.session_state.embeddings = embeddings
                st.session_state.messages = []
                st.session_state.pdf_name = uploaded_file.name

                st.success(
                    f"PDF processed successfully! "
                    f"{len(chunks)} sections created."
                )

        except Exception as error:
            st.error(f"PDF processing error: {error}")


# PDF status
if st.session_state.chunks:
    st.success(
        f"RAG ready: {st.session_state.pdf_name}"
    )

    st.info(
        f"{len(st.session_state.chunks)} sections available."
    )


# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message["role"] == "assistant" and "sources" in message:
            with st.expander("View source sections"):
                for source in message["sources"]:
                    st.markdown(
                        f"**Section {source['number']}**"
                    )
                    st.write(source["text"])


# Ask questions
question = st.chat_input("Ask a question about your research paper...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Finding relevant information..."):

            try:
                context = ""
                sources = []

                if st.session_state.chunks:
                    best_indices = retrieve_chunks(
                        question,
                        st.session_state.chunks,
                        st.session_state.embeddings
                    )

                    for index in best_indices:
                        chunk = st.session_state.chunks[index]

                        sources.append({
                            "number": index + 1,
                            "text": chunk
                        })

                        context += (
                            f"\n\nSection {index + 1}:\n{chunk}"
                        )

                system_prompt = (
                    "You are a helpful AI research assistant. "
                    "Answer questions clearly and accurately. "
                    "Use the supplied research paper sections "
                    "as evidence. If the answer is not present "
                    "in the sections, say so clearly. "
                    "Do not invent facts.\n\n"
                    "RESEARCH PAPER SECTIONS:\n"
                    + context
                )

                chat_messages = [
                    {
                        "role": "system",
                        "content": system_prompt
                    }
                ]

                chat_messages += st.session_state.messages

                response = requests.post(
                    f"{OLLAMA_URL}/api/chat",
                    json={
                        "model": CHAT_MODEL,
                        "messages": chat_messages,
                        "stream": False
                    },
                    timeout=180
                )

                response.raise_for_status()

                answer = response.json()["message"]["content"]

                st.write(answer)

                if sources:
                    with st.expander("View source sections"):
                        for source in sources:
                            st.markdown(
                                f"**Section {source['number']}**"
                            )
                            st.write(source["text"])

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except Exception as error:
                st.error(f"Error: {error}")



