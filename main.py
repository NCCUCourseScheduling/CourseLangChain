import threading, sqlite3, logging, pickle
import fire
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores.faiss import VectorStore
from langchain.schema import Document
from langchain.llms.llamacpp import LlamaCpp
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from utils.prompt import get_prompt
from utils.time import getSessionArray, weekdayCode
from utils.callback import ChainStreamHandler
from detector import NegationDetector
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents import Tool, initialize_agent

logger = logging.getLogger('CourseLangchain')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class CourseLangChain():
  def __init__(self, pickleFile="vectorstore.pkl", modelFile="model/chinese-alpaca-2-7b.Q8_0.gguf", cli=False) -> None:
    
    # Model Name Defination
    instruction = """Context:\n{context}\n\nQuestion: {question}\nAnswer: """
    #print("Instruction:")
    #print(instruction)
    prompt_template = get_prompt(instruction)
    logger.info("Prompt Template:\n" + prompt_template)

    with open(pickleFile, "rb") as f:
      vectorstore: VectorStore = pickle.load(f)
    
    # RetrievalQA Requirements
    #retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
    retriever = vectorstore
    
    self.handler = ChainStreamHandler() if not cli else StreamingStdOutCallbackHandler()
    
    llm = LlamaCpp(
      model_path=modelFile,
      callback_manager=CallbackManager([self.handler]),
      n_gpu_layers=43,
      n_batch=512,
      n_ctx=4096,
      f16_kv=True,
      verbose=True,  # Verbose is required to pass to the callback manager
    )
    
    conversational_memory = ConversationBufferWindowMemory(
      memory_key="chat_history",
      k=5,
      return_messages=True,
    )

    self.qa = RetrievalQA.from_chain_type(
      llm=llm, chain_type='stuff',
      retriever=retriever,
      chain_type_kwargs={
       "prompt": PromptTemplate(
          template=prompt_template,
          input_variables=["context", "question"],),
     },
    )
    logger.info("Chain ready.")

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
      agent='chat-conversational-react-description',
      tools=self.tools,
      llm=llm,
      verbose=True,
      max_iterations=3,
      early_stopping_method='generate',
      memory=conversational_memory,
      handle_parsing_errors="Check your output and make sure it is in correct format.",
    )
    
  def query(self, query: str):
    def async_run():
      self.agent(query)
    thread = threading.Thread(target=async_run)
    thread.start()
    return self.handler.generate_tokens()

def main():
  chain = CourseLangChain(cli=True)
  while True:
    query = input("User:")
    negation_detector = NegationDetector(verbose=True)
    new_query = negation_detector.find_negation_sentences(query)
    print("positive_query:")
    print(new_query)
    print("Bot:")
    chain.agent(new_query)
  
if __name__ == "__main__":
  fire.Fire(main)
