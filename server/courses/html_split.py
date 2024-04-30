from langchain_text_splitters import HTMLHeaderTextSplitter
from langchain_community.document_loaders import PyPDFLoader, PDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma, FAISS
import os
from langchain_community.document_loaders import BSHTMLLoader

with open("courses_compe\compe_group2_electives.html", "r", encoding="utf-8") as file:
    html_content = file.read()

headers_to_split_on = [
    ("title", "Header 1"),
    ("h2", "Header 2")
]

model_name = "sentence-transformers/all-MiniLM-L6-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}

embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
    )

html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
html_header_splits = html_splitter.split_text(html_content)

print(html_header_splits)

db = FAISS.from_documents(html_header_splits, embeddings)

db.save_local('test')