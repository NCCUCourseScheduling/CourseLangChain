import sqlite3, pickle, json
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.retrievers.bm25 import BM25Retriever
from langchain.schema import Document
from utils.time import getSessionArray, weekdayCode
from utils.retriever import EnsembleRetriever

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
  return d

def document_factory(cursor, row):
  return ClassDocument(dict_factory(cursor, row))

def build(dataFile="data.db", vectorStorePkl="vectorstore.pkl", embeddingModel="shibing624/text2vec-base-chinese"):
  con = sqlite3.connect(dataFile)
  con.row_factory = document_factory
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
  # ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, faiss_retriever], weights=[0, 1])
  ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, faiss_retriever], weights=[0.5, 0.5])
  
  with open(vectorStorePkl, "wb") as f:
    pickle.dump(ensemble_retriever, f)
    
  con.row_factory = dict_factory
  cursor = con.cursor()
  
  req = cursor.execute("SELECT * FROM COURSE WHERE y = 112 AND s = 1")
  res = req.fetchall()
  
  with open('output.json', 'w') as f:
    rows = list()
    for row in res:
      tmp = dict()
      timeStr = ""
      sessionArray = getSessionArray(row["time"])
      if len(sessionArray) > 0:
        for i, session in enumerate(sessionArray):
          if i > 0:
            timeStr += "、"
          timeStr += f'星期{weekdayCode[session["week_code"] - 1]} {session["start_time"]}:00-{session["end_time"]}:00'
      else:
        timeStr = "未定"
      tmp["課程名稱"] = row["name"]
      tmp["課程內容"] = row["objective"]
      tmp["上課時間"] = timeStr
      tmp["老師名稱"] = row["teacher"]
      rows.append(tmp)
    f.write(json.dumps(rows))
    
      

if __name__ == "__main__":
  build()
