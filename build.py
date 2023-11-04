import sqlite3, pickle
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from utils.time import getSessionArray, weekdayCode

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
    
    contentStr = "課程名稱: {}\n課程內容: {}\n上課時間: {}\n老師名稱: {}".format(content["name"], content["objective"], timeStr, content["teacher"])
    
    self.page_content = contentStr
    self.metadata = content

def dict_factory(cursor, row):
  d = {}
  for idx, col in enumerate(cursor.description):
      d[col[0]] = row[idx]
  return ClassDocument(d)

def build(dataFile="data.db", pickleFile="vectorstore.pkl", embeddingModel="shibing624/text2vec-base-chinese"):
  con = sqlite3.connect(dataFile)
  con.row_factory = dict_factory
  cursor = con.cursor()
  
  req = cursor.execute("SELECT * FROM COURSE WHERE y = 112 AND s = 1")
  res = req.fetchall()
  
  embeddings = HuggingFaceEmbeddings(model_name=embeddingModel)

  # initialize the faiss retriever
  vectorStore = FAISS.from_documents(res, embedding=embeddings)
  faiss_retriever = vectorStore.as_retriever(search_kwargs={"k": 10})
    
  # initialize the bm25 retriever
  bm25_retriever = BM25Retriever.from_documents(res, embedding=embeddings)
  bm25_retriever.k = 10

  # initialize the ensemble retriever
  ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, faiss_retriever], weights=[0, 1])
  #ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, faiss_retriever], weights=[0.5, 0.5])
  
  with open(pickleFile, "wb") as f:
    pickle.dump(vectorStore, f)

if __name__ == "__main__":
  build()
