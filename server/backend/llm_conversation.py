from langchain_community.llms import HuggingFaceHub, HuggingFaceEndpoint
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.memory import ConversationSummaryMemory, ConversationBufferMemory
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import VectorStoreRetriever
from dotenv import load_dotenv
import os

class LLMConversations():

    def __init__(self, discipline_or_clubs):
        self.discipline_or_clubs = discipline_or_clubs
    
    def electives(self):
        load_dotenv()
        HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
        repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"

        llm = HuggingFaceEndpoint(
              repo_id=repo_id,
              task ="text-generation",
              temperature= 0.1,
              model_kwargs={"max_length":80000}
        )

        current_directory = os.getcwd()
        parent_directory = os.path.dirname(current_directory)

        model_name = "VoVanPhuc/sup-SimCSE-VietNamese-phobert-base"
        model_kwargs = {'device': 'cpu'}
        encode_kwargs = {'normalize_embeddings': False}

        embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )

        vector_store = ''

        if self.discipline_or_clubs == "compe normal":
            vector_store = os.path.join(parent_directory, "courses_compe/faiss")
        elif self.discipline_or_clubs == "compe nano":
            vector_store = os.path.join(parent_directory, "courses_compe_nano/faiss")
        elif self.discipline_or_clubs == "software":
            vector_store = os.path.join(parent_directory, "courses_softe/faiss")
        elif self.discipline_or_clubs == "ee bio":
            vector_store = os.path.join(parent_directory, "courses_ee_bio/faiss")
        elif self.discipline_or_clubs == "ee nano":
            vector_store = os.path.join(parent_directory, "courses_ee_nano/faiss")
        elif self.discipline_or_clubs == "ee normal":
            vector_store = os.path.join(parent_directory, "courses_ee_normal/faiss")
        elif self.discipline_or_clubs == "enphys nano":
            vector_store = os.path.join(parent_directory, "courses_enphys_nano/faiss")
        elif self.discipline_or_clubs == "enphys normal":
            vector_store = os.path.join(parent_directory, "courses_enphys_normal/faiss")
        elif self.discipline_or_clubs == "clubs":
            vector_store_directory = os.path.join(parent_directory, "./courses/clubs_faiss")
            print(vector_store_directory)
            vector_store = FAISS.load_local(vector_store_directory, embeddings, allow_dangerous_deserialization=True)
            print(vector_store)
        
        # LLM aspects initialized

        memory = ConversationBufferMemory(memory_key='chat_history', output_key='answer')
        memory_two = ConversationBufferMemory(
            memory_key='chat_history', return_messages=True, output_key='answer')
        
        if self.discipline_or_clubs == 'clubs':
            template = """A student will ask you a variety of questions regarding clubs at the University of Alberta.
            Using your knowledge store, make sure to answer the user's questions using the information you have.
            The user may ask questions such as on what clubs they should join based off of their interests, what club may the best for them to help them in their career, what clubs may be the best for them based off of their university major, and so much more
            Only answer the question in the context of clubs at the University of Alberta. Make sure to give the information while keeping in mind the best clubs that fit what the question is asking.
            Answer the question {question} in the context of clubs at the University of Alberta to the best of your knowledge, and do not make up any information.
            DO NOT MAKE UP ANY INFORMATION. Also, when answering questions about which clubs to join based off of the student's interests or what major or university program they plan to go into, also take the club name into consideration (e.g. if the student is interested in computer engineering, the best club to join would be the computer engineering club.)
            Only return the helpful answer below and nothing else.

            question: {question}
            Use this context to answer the question: {context}

            Helpful answer:
            """
            retriever = vector_store.as_retriever(search_kwargs={"k": 60})
            #memory = VectorStoreRetrieverMemory(retriever=retriever, memory_key="chat_history", return_docs=False, return_messages=True)
    

        prompt = PromptTemplate(template=template, input_variables=['context','question'])
        # llm_chain = LLMChain(prompt=prompt, llm=llm)

        while True:
            question = input('Ask any question you have regarding clubs & student organizations at the UofA: ')


            #matching_docs = db.similarity_search(question)

            #answer = llm_chain.run({
            #    "question": question,
            #    "context": matching_docs
            # })

            retrieval_chain = RetrievalQA.from_chain_type(
                llm=llm, chain_type="stuff", retriever=retriever,
                verbose=True,
                chain_type_kwargs={
                "verbose": True,
                "prompt": prompt,
                "memory": ConversationBufferMemory(
                    memory_key="history",
                    input_key="question"),
                })
            print(retrieval_chain.run({"query": question}))

            #print(retrieval_chain.run((question)))
            #print(answer(question)["answer"])

            #answer = ConversationalRetrievalChain.from_llm(llm, 
            #        retriever=retriever, memory=memory, return_source_documents=True, combine_docs_chain_kwargs={'prompt': prompt})
            #print(answer(question)["answer"])

if __name__ == "__main__":
    test_run = LLMConversations('clubs')

    test_run.electives()

