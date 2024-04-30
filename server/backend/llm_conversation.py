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
        # "VoVanPhuc/sup-SimCSE-VietNamese-phobert-base"
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        model_kwargs = {'device': 'cpu'}
        encode_kwargs = {'normalize_embeddings': False}

        embeddings = HuggingFaceEmbeddings(
                    model_name=model_name,
                    model_kwargs=model_kwargs,
                    encode_kwargs=encode_kwargs
            )

        vector_store = ''

        if self.discipline_or_clubs == "Computer Engineering":
            vector_store_directory = os.path.join(parent_directory, "./courses/courses_compe/faiss")
            vector_store = FAISS.load_local(vector_store_directory, embeddings, allow_dangerous_deserialization=True)
        elif self.discipline_or_clubs == "Computer Engineering - Nanoscale System Design":
            vector_store_directory = os.path.join(parent_directory, "./courses/courses_compe_nano/faiss")
            vector_store = FAISS.load_local(vector_store_directory, embeddings, allow_dangerous_deserialization=True)
        elif self.discipline_or_clubs == "Software Engineering":
            vector_store_directory = os.path.join(parent_directory, "./courses/courses_softe/faiss")
            vector_store = FAISS.load_local(vector_store_directory, embeddings, allow_dangerous_deserialization=True)
        elif self.discipline_or_clubs == "Electrical Engineering - Biomedical Engineering Option":
            vector_store_directory = os.path.join(parent_directory, "./courses/courses_ee_bio/faiss")
            vector_store = FAISS.load_local(vector_store_directory, embeddings, allow_dangerous_deserialization=True)
        elif self.discipline_or_clubs == "Electrical Engineering - Nanoengineering Option":
            vector_store_directory = os.path.join(parent_directory, "./courses/courses_ee_nano/faiss")
            vector_store = FAISS.load_local(vector_store_directory, embeddings, allow_dangerous_deserialization=True)
        elif self.discipline_or_clubs == "Electrical Engineering":
            vector_store_directory = os.path.join(parent_directory, "./courses/courses_ee_normal/faiss")
            vector_store = FAISS.load_local(vector_store_directory, embeddings, allow_dangerous_deserialization=True)
        elif self.discipline_or_clubs == "Engineering Physics - Nanoengineering Option":
            vector_store_directory = os.path.join(parent_directory, "./courses/courses_enphys_nano/faiss")
            vector_store = FAISS.load_local(vector_store_directory, embeddings, allow_dangerous_deserialization=True)
        elif self.discipline_or_clubs == "Engineering Physics":
            vector_store_directory = os.path.join(parent_directory, "./courses/courses_enphys_normal/faiss")
            vector_store = FAISS.load_local(vector_store_directory, embeddings, allow_dangerous_deserialization=True)
        elif self.discipline_or_clubs == "clubs":
            vector_store_directory = os.path.join(parent_directory, "./courses/clubs_faiss")
            vector_store = FAISS.load_local(vector_store_directory, embeddings, allow_dangerous_deserialization=True)
        
        # LLM aspects initialized

        memory = ConversationBufferMemory(
            memory_key='chat_history', return_messages=True, output_key='answer')
        
        question = ''
        
        if self.discipline_or_clubs == 'clubs':
            template = """A student will ask you a variety of questions regarding clubs at the University of Alberta.
            Using your knowledge store, make sure to answer the user's questions using the information you have.
            The user may ask questions such as on what clubs they should join based off of their interests, what club may the best for them to help them in their career, what clubs may be the best for them based off of their university major, and so much more
            Only answer the question in the context of clubs at the University of Alberta. Make sure to give the information while keeping in mind the best clubs that fit what the question is asking.
            Answer the question {question} in the context of clubs at the University of Alberta to the best of your knowledge, and do not make up any information (say you don't know if you do not know).
            DO NOT MAKE UP ANY INFORMATION. Also, when answering questions about which clubs to join based off of the student's interests or what major or university program they plan to go into, also take the club name into consideration (e.g. if the student is interested in computer engineering, the best club to join would be the computer engineering club.)
            Only return the helpful answer below and nothing else. DO not make up any information. After responding to a question, make sure to say something like "I hope this helps! Let me know if you have any other questions." or something similar to it.

            question: {question}
            Conversation history (make sure to remember this as the student may ask you about questions they asked or answers you gave at certain points in the conversation): {chat_history}
            Use this context to answer the question: {context}

            Helpful answer:
            """
            #memory = VectorStoreRetrieverMemory(retriever=retriever, memory_key="chat_history", return_docs=False, return_messages=True)
            retriever = vector_store.as_retriever(search_kwargs={"k": 80})
        elif self.discipline_or_clubs == "Engineering Physics - Nanoengineering Option":
            template = """A student in the """ + self.discipline_or_clubs + """ major will ask you a variety of questions regarding Technical Electives offered at the University of Alberta for their elective.
            Using your knowledge store, make sure to answer the user's questions using the information you have.
            The user may ask questions such as on what courses they should take based off of their interests, what course is offered during a certain term, what instructor teaches a certain course at a certain term, how the professor is (when asked how the professor is, give the professor's Rate My Professor rating or if it isn't available, say that there isn't a Rate My Professor rating available), or what courses may the best to take for certain career aspirations, or what the course difficulty is, and so much more.
            Only answer the question in the context of clubs at the University of Alberta. Make sure to give the answer based off of the information that fits what the question is asking.
            Answer the question {question} in the context of courses offered for the """ + self.discipline_or_clubs + """ major at the University of Alberta to the best of your knowledge, and do not make up any information (say you don't know if you do not know).
            DO NOT MAKE UP ANY INFORMATION. Also, when answering questions on what the course is about or a student wanting to take course(s) based off of their interests, make sure to keep the course description in mind.
            Only return the helpful answer below and nothing else. DO not make up any information. After responding to a question, make sure to say something like "I hope this helps! Let me know if you have any other questions." or something similar to it.
            Remember, DO NOT make up any information such as course names or courses, instructors, course descriptions, when courses are being offered, etc.
            Also, if a student asks you when a course is being offered, do not list the prerequisites as being offered as well (unless they really are). Not all of a course's prerequisites are offered at the same time a course is being offered at. Carefully check if a course is being offered during a certain period before saying that it is. Do not confuse which instructor/professor is teaching which course.
            To recommend the best match for a course based off of a topic (such as machine learning), make sure to check the course description carefully. For example, if a student asks about the best course for machine learning, recommend the course that explicitly mentions machine learning first. If there are no courses that mention the topic the student wants a course for explicitly or if the student asks for other courses on the topic, then feel free to recommend the closest matches.
            Also, do not state the wrong terms that a course is offered in. Only state the correct ones.

            Question: {question}
            Conversation history (make sure to remember this as the student may ask you about questions they asked or answers you gave at certain points in the conversation): {chat_history}
            Use this context to answer the question: {context}

            Helpful answer:
            """
            retriever = vector_store.as_retriever(search_kwargs={"k": 80})
        
        else:
            template = """A student in the """ + self.discipline_or_clubs + """ major will ask you a variety of questions regarding Group 2 Electives offered at the University of Alberta for their elective.
            Using your knowledge store, make sure to answer the user's questions using the information you have.
            The user may ask questions such as on what courses they should take based off of their interests, what courses are offered during certain terms, what instructor teaches a certain course at a certain term, how the professor is (when asked how the professor is, give the professor's Rate My Professor rating or if it isn't available, say that it isn't available), or what courses may the best to take for certain career aspirations, or what the course difficulty is, and so much more.
            Only answer the question in the context of clubs at the University of Alberta. Make sure to give the answer based off of the information that fits what the question is asking.
            Answer the question {question} in the context of courses offered for the """ + self.discipline_or_clubs + """ major at the University of Alberta to the best of your knowledge, and do not make up any information (say you don't know if you do not know).
            DO NOT MAKE UP ANY INFORMATION. Also, when answering questions on what the course is about or a student wanting to take course(s) based off of their interests, make sure to keep the course description in mind.
            Only return the helpful answer below and nothing else. DO not make up any information. After responding to a question, make sure to say something like "I hope this helps! Let me know if you have any other questions." or something similar to it.
            Remember, DO NOT make up any information such as course names or courses, instructors, course descriptions, when courses are being offered, etc.
            Also, if a student asks you when a course is being offered, do not list the prerequisites as being offered as well (unless they really are). Not all of a course's prerequisites are offered at the same time a course is being offered at. Carefully check if a course is being offered during a certain period before saying that it is. Do not confuse which instructor/professor is teaching which course.
            If the student asks you all the course being offered during a certain term, only list the ones actually being offered during the term. DO NOT MAKE UP INFORMATION.
            When a student asks you about what course(s) to take based off of their interests, make sure to answer based off of the Course Description and also Course Difficulty (if the Course Difficulty section has relevant information).

            Question: {question}
            Conversation history (make sure to remember this as the student may ask you about questions they asked or answers you gave at certain points in the conversation): {chat_history}
            Use this context to answer the question. Make sure to only use information from the context that correctly answers what the student is asking: {context}

            Helpful answer:
            """
            vector_store = FAISS.load_local(r"C:\umer files\Programming PREJE'S\OfCourse\server\courses\test", embeddings, allow_dangerous_deserialization=True)
            retriever = vector_store.as_retriever(search_kwargs={"k": 15})
            print(retriever)
            
        prompt = PromptTemplate(template=template, input_variables=['context','question','chat_history'])
        # llm_chain = LLMChain(prompt=prompt, llm=llm)

        while True:
            question = input(f'Ask any question you have regarding courses for the {self.discipline_or_clubs} program at the UofA: ')


            #matching_docs = db.similarity_search(question)

            #answer = llm_chain.run({
            #    "question": question,
            #    "context": matching_docs
            # })

            """
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
            """
            #print(retrieval_chain.run((question)))
            #print(answer(question)["answer"])

            answer = ConversationalRetrievalChain.from_llm(llm, 
                    retriever=retriever, memory=memory, return_source_documents=True, combine_docs_chain_kwargs={'prompt': prompt})
            print(answer(question)["answer"])

if __name__ == "__main__":
    test_run = LLMConversations('Computer Engineering')

    test_run.electives()

