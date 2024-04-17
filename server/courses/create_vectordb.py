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

    nested_directory_path = os.path.join(directory, "chroma_db")

    # Create the nested directory if it doesn't exist
    os.makedirs(nested_directory_path, exist_ok=True)

    db = Chroma.from_documents(all_splits, embeddings, persist_directory = nested_directory_path)

    return db

if __name__ == "__main__":

    directory_path = os.getcwd()

    repo = Repo('C:\\umer files\\Programming PREJE\'S\\OfCourse')

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

                    repo.git.add(update=True)

                    # Commit changes
                    repo.index.commit("Automated commit after converting {}".format(file))

                    vectordb(pdf_file_path, item_path)

                    repo.git.add(update=True)

                    # Commit changes
                    repo.index.commit("Automated commit after processing {}".format(file))