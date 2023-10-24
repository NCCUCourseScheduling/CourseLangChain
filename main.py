import threading, sqlite3, logging
import fire
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain.llms.llamacpp import LlamaCpp
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from utils.prompt import get_prompt
from utils.time import getSessionArray, weekdayCode
from utils.callback import ChainStreamHandler

logger = logging.getLogger('CourseLangchain')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class ClassDocument(Document):
  def __init__(self, content: dict) -> None:
    super().__init__(page_content=str(content), metadata=content)
    
    timeStr = ""
    sessionArray = getSessionArray(content["time"])
    if len(sessionArray) > 0:
      for i, session in enumerate(sessionArray):
        if i > 0:
          timeStr += "、"
        timeStr += f'星期{weekdayCode[session["week_code"] - 1]} {session["start_time"]}:00-{session["end_time"]}:00'
    else:
      timeStr = "未定"
    
    contentStr = "課程名稱: {}\n課程內容: {}\n上課時間: {}".format(content["name"], content["objective"], timeStr)
    
    self.page_content = contentStr
    self.metadata = content

def dict_factory(cursor, row):
  d = {}
  for idx, col in enumerate(cursor.description):
      d[col[0]] = row[idx]
  return ClassDocument(d)

class CourseLangChain():
  def __init__(self, dataFiles="data.db", embeddingModel="shibing624/text2vec-base-chinese", modelFile="model/chinese-alpaca-2-13b.Q8_0.gguf", cli=False) -> None:
    
    # Model Name Defination
    instruction = """Context:\n{context}\n\nQuestion: {question}\nAnswer: """
    prompt_template = get_prompt(instruction)
    logger.info("Prompt Template:\n" + prompt_template)
    
    # Create sqlite connection and query all courses
    con = sqlite3.connect(dataFiles)
    con.row_factory = dict_factory
    cursor = con.cursor()
    
    req = cursor.execute("SELECT * FROM COURSE WHERE y = 112 AND s = 1")
    res = req.fetchall()
    
    # Transform into embedding vector and store to vector store
    embeddings = HuggingFaceEmbeddings(model_name=embeddingModel)
    vectorStore = FAISS.from_documents(res, embedding=embeddings)
    logger.info("Vector store ready.")
    
    # RetrievalQA Requirements
    retriever = vectorStore.as_retriever(search_kwargs={"k": 10})
    
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
    
    self.chain = RetrievalQA.from_chain_type(
      llm=llm, chain_type='stuff',
      retriever=retriever,
      chain_type_kwargs={
        "prompt": PromptTemplate(
          template=prompt_template,
          input_variables=["context", "question"],
        ),
      },
    )
    logger.info("Chain ready.")
    
  def query(self, query: str):
    def async_run():
      self.chain.run(query)
    thread = threading.Thread(target=async_run)
    thread.start()
    return self.handler.generate_tokens()

def main():
  chain = CourseLangChain(cli=True)
  while True:
    query = input("User:")
    print("Bot:")
    chain.chain.run(query)
  
if __name__ == "__main__":
  fire.Fire(main)
