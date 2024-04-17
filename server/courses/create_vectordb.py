from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os
from docx2pdf import convert
from git import Repo

def vectordb(file, directory):
    loader = PyPDFLoader(file)
    docs = loader.load()

    embeddings = HuggingFaceEmbeddings()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)
    all_splits = text_splitter.split_documents(docs)

    if file == 'courses\list_of_clubs.pdf':
        nested_directory_path = os.path.join(directory, "clubs_chroma_db")
    else:
        nested_directory_path = os.path.join(directory, "chroma_db")

    # Create the nested directory if it doesn't exist
    os.makedirs(nested_directory_path, exist_ok=True)

    db = Chroma.from_documents(all_splits, embeddings, persist_directory = nested_directory_path)

    return db

if __name__ == "__main__":

    directory_path = os.getcwd()

    contents = os.listdir(directory_path)

    for file in contents:
        item_path = os.path.join(directory_path, file)

        if os.path.isdir(item_path) and "cache" not in item_path:
            directory_contents = os.listdir(item_path)

            for i in range(0, len(directory_contents)):
                if ".docx" in directory_contents[i]:
                    nested_item_path = os.path.join(item_path, directory_contents[i])

                    file_minus_extension = nested_item_path.split('.')
                    pdf_file_path = file_minus_extension[0] + '.pdf'
                    convert(nested_item_path, pdf_file_path)

                    vectordb(pdf_file_path, item_path)
                    convert('courses\list_of_clubs.docx', 'courses\list_of_clubs.pdf')

                    vectordb('courses\list_of_clubs.pdf', 'courses')