from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from dotenv import load_dotenv
import os

class LLMConversations():

    def __init__(self):
        load_dotenv()
        self.HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    
    def electives(self, discipline_or_clubs, question):
        repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

        llm = HuggingFaceEndpoint(
              repo_id=repo_id, max_length = 100, temperature=0.1, token=self.HUGGINGFACEHUB_API_TOKEN
        )

        current_directory = os.getcwd()
        parent_directory = os.path.dirname(current_directory)
        vector_store = ''

        if discipline_or_clubs == "compe normal":
            vector_store = os.path.join(parent_directory, "courses_compe/chroma_db")
        elif discipline_or_clubs == "compe nano":
            vector_store = os.path.join(parent_directory, "courses_compe_nano/chroma_db")
        elif discipline_or_clubs == "software":
            vector_store = os.path.join(parent_directory, "courses_softe/chroma_db")
        elif discipline_or_clubs == "ee bio":
            vector_store = os.path.join(parent_directory, "courses_ee_bio/chroma_db")
        elif discipline_or_clubs == "ee nano":
            vector_store = os.path.join(parent_directory, "courses_ee_nano/chroma_db")
        elif discipline_or_clubs == "ee normal":
            vector_store = os.path.join(parent_directory, "courses_ee_normal/chroma_db")
        elif discipline_or_clubs == "enphys nano":
            vector_store = os.path.join(parent_directory, "courses_enphys_nano/chroma_db")
        elif discipline_or_clubs == "enphys normal":
            vector_store = os.path.join(parent_directory, "courses_enphys_normal/chroma_db")
        elif discipline_or_clubs == "clubs":
            vector_store = os.path.join(parent_directory, "clubs_chroma_db")