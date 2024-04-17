from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

def vectordb(file, directory):
    loader = PyPDFLoader(file)
    docs = loader.load()

    embeddings = HuggingFaceEmbeddings()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)
    all_splits = text_splitter.split_documents(text_splitter)

    nested_directory_path = os.path.join(directory, "chroma_db")

    # Create the nested directory if it doesn't exist
    os.makedirs(nested_directory_path, exist_ok=True)

    db = Chroma.from_documents(all_splits, embeddings, persist_directory = nested_directory_path)

    return

