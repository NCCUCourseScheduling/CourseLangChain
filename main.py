import threading
import logging
import pickle
import fire
# from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores.faiss import VectorStore
# from langchain.schema import Document
from langchain.llms.llamacpp import LlamaCpp
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from utils.prompt import get_prompt
# from utils.time import getSessionArray, weekdayCode
from utils.callback import ChainStreamHandler
from detector import NegationDetector
from langchain.retrievers import EnsembleRetriever
from langchain.memory import ConversationBufferWindowMemory
from dotenv import load_dotenv

# remember to add the .env file in order to use Langsmith API
load_dotenv()

logger = logging.getLogger('CourseLangchain')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class CourseLangChain():
    def __init__(self, pickleFile="vectorstore.pkl", modelFile="model/taide-8b-a.3-q4_k_m.gguf", cli=False) -> None:

        # Model Name Defination
        instruction = """Context:\n{context}\n\nQuestion: {question}\nAnswer: """
        prompt_template = get_prompt(instruction)
        logger.info("Prompt Template:\n" + prompt_template)

        with open(pickleFile, "rb") as f:
            retriever: EnsembleRetriever = pickle.load(f)

        self.handler = ChainStreamHandler() if not cli else StreamingStdOutCallbackHandler()

        llm = LlamaCpp(
            model_path=modelFile,
            callback_manager=CallbackManager([self.handler]),
            n_gpu_layers=43,
            n_batch=512,
            n_ctx=4096,
            f16_kv=True,
            verbose=True,    # Verbose is required to pass to the callback manager
        )

        conversational_memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            k=5,
            return_messages=True,
        )

        self.chain = RetrievalQA.from_chain_type(
            llm=llm, chain_type='stuff',
            retriever=retriever,
            chain_type_kwargs={
             "prompt": PromptTemplate(
                    template=prompt_template,
                    input_variables=["context", "question"],),
            },
        )
        logger.info("Chain ready.")
        
        ## increase chat history
        self.chat_history = []

        """
        self.tools = [
            Tool(
                name='Knowledge Base',
                func=self.qa.run,
                description=(
                    'use this tool to answer questions about course information.'
                    
                ),
            )
        ]
        
        self.agent = initialize_agent(
            agent='chat-conversation',
            tools=self.tools,
            llm=llm,
            verbose=True,
            max_iterations=3,
            early_stopping_method='generate',
            memory=conversational_memory,
            handle_parsing_errors="Check your output and make sure it is in correct format.",
        )
        """
    def query(self, query: str):
        def async_run():
            self.chain.invoke(query)
        thread = threading.Thread(target=async_run)
        thread.start()
        return self.handler.generate_tokens()
    

    def save_to_history(self, user_query, bot_response):
        self.chat_history.append((user_query, bot_response))

    def combine_with_history(self, new_query):
        combined_query = " ".join([f"User: {pair[0]} Bot: {pair[1]}" for pair in self.chat_history])
        combined_query += f" User: {new_query}"
        return combined_query


def main():
    # chain = CourseLangChain(cli=True, modelFile="../models/ggml-model-q4_k.gguf?download=true")
    chain = CourseLangChain(cli=True)
    while True:
        query = input("User:")
        negation_detector = NegationDetector(verbose=True)
        new_query = negation_detector.find_negation_sentences(query)
        #combine
        new_query_with_history = chain.combine_with_history(new_query)
        print("positive_query:")
        print(new_query_with_history)
        print("Bot:")
        bot_response = chain.chain.invoke(new_query_with_history)
        chain.save_to_history(new_query, bot_response)

    
if __name__ == "__main__":
    fire.Fire(main)
