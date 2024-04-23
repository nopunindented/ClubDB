from langchain_community.document_loaders import PyPDFLoader, PDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma, FAISS
import os
from docx2pdf import convert
from git import Repo

def vectordb(file, directory):
    loader = PDFPlumberLoader(file)
    docs = loader.load()

    model_name = "VoVanPhuc/sup-SimCSE-VietNamese-phobert-base"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}

    embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
    )
    text_splitter = ''

    if file == 'list_of_clubs.pdf':
        nested_directory_path = "clubs_faiss"
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)
    else:
        nested_directory_path = os.path.join(directory, "faiss")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 2000, chunk_overlap = 250)
    
    all_splits = text_splitter.split_documents(docs)

    # Create the nested directory if it doesn't exist
    os.makedirs(nested_directory_path, exist_ok=True)

    db = FAISS.from_documents(all_splits, embeddings)

    db.save_local(nested_directory_path)

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
                    print(pdf_file_path)
                    convert(nested_item_path, pdf_file_path)

                    vectordb(pdf_file_path, item_path)
    convert('list_of_clubs.docx', 'list_of_clubs.pdf')

    vectordb('list_of_clubs.pdf', 'hello')