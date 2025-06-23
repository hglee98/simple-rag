from langchain_community.document_loaders import DirectoryLoader
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import os
import chromadb

from core.embedding_client import EmbeddingModel

DATA_PATH = "data"


def load_documents():
    """
    Load documents from the specified directory.

    Returns:
        list: A list of loaded documents.
    """
    loader = DirectoryLoader(DATA_PATH, glob="**/*.md")
    documents = loader.load()
    return documents


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[10]
    print(document.page_content)
    print(document.metadata)

    return chunks


def calculate_chunk_ids(chunks):
    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the chunk meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks


def add_to_chroma(chunks: list[Document]):
    """
    Add chunks to Chroma vector store.

    Args:
        chunks (list[Document]): List of document chunks to add.
    """
    embedding = EmbeddingModel()
    db = Chroma(
        collection_name="rag_collection",
        embedding_function=embedding,
        client=chromadb.HttpClient(
            host=os.getenv("VECTOR_DB_HOST", "localhost"), port=os.getenv("VECTOR_DB_PORT", "8000")
        ),
    )

    chunks_with_ids = calculate_chunk_ids(chunks)
    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)
    max_docs = 10
    new_chunks = new_chunks[:max_docs]  # Limit to max_docs for testing
    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("✅ No new documents to add")


if __name__ == "__main__":
    docs = load_documents()
    print(f"Loaded {len(docs)} documents from {DATA_PATH}")
    chunks = split_text(docs)
    print(f"Total chunks created: {len(chunks)}")
    add_to_chroma(chunks)
    # for doc in docs:
    #     print(
    #         f"Document: {doc.metadata.get('source', 'Unknown source')}, Content: {doc.page_content[:100]}..."
    #     )
