# AI Research Assistant 🤖

An AI-powered research assistant that helps users understand research papers by uploading PDF documents and asking questions.

## Features

- Upload research papers in PDF format.
- Extract text from PDF documents.
- Split documents into smaller sections.
- Generate embeddings using Ollama.
- Retrieve relevant sections using cosine similarity.
- Answer questions using a local AI model.
- Display source sections used for answers.

## Technologies Used

- Python
- Streamlit
- Ollama
- Llama 3.2
- Nomic Embed Text
- NumPy
- PyPDF

## How It Works

This project uses Retrieval-Augmented Generation (RAG).

1. Upload a PDF research paper.
2. The application extracts its text.
3. Text is divided into smaller chunks.
4. Ollama generates embeddings.
5. Relevant chunks are retrieved for each question.
6. The language model generates an answer using the retrieved information.

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
```

Open the project folder:

```bash
cd AI-Research-Assistant
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Make sure Ollama is installed and the required models are available:

```bash
ollama pull llama3.2:1b
ollama pull nomic-embed-text
```

Run the application:

```bash
streamlit run app.py
```

## Project Goal

The goal of this project is to explore local AI models, document understanding, embeddings, semantic search, and Retrieval-Augmented Generation.

## Author

AI Student | Aspiring AI Engineer
