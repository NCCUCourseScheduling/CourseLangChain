from torch import cuda
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig, pipeline
from utils.prompt import get_prompt
from utils.time import getSessionArray, weekdayCode
import fire, torch, sqlite3

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
  def __init__(self, dataFiles="data.db", k=10) -> None:
    
    # Model Name Defination
    embeddingModelName = "shibing624/text2vec-base-chinese"
    transformerModelName = "FlagAlpha/Llama2-Chinese-13b-Chat"
    instruction = """{context}\n\nQuestion: {question}"""
    
    # Create sqlite connection and query all courses
    con = sqlite3.connect(dataFiles)
    con.row_factory = dict_factory
    cursor = con.cursor()
    
    req = cursor.execute("SELECT * FROM COURSE WHERE y = 112 AND s = 1")
    res = req.fetchall()
    
    # Transform into embedding vector and store to vector store
    embeddings = HuggingFaceEmbeddings(model_name=embeddingModelName)
    vectorStore = FAISS.from_documents(res, embedding=embeddings)
    
    # RetrievalQA Requirements
    tokenizer = AutoTokenizer.from_pretrained(transformerModelName)
    model = AutoModelForCausalLM.from_pretrained(transformerModelName, device_map='auto', torch_dtype=torch.float16, load_in_8bit=True)
    retriever = vectorStore.as_retriever(search_kwargs={"k": k})
    
    generationConfig = GenerationConfig(
      return_full_text=True,
      temperature=0.0,  # 'randomness' of outputs, 0.0 is the min and 1.0 the max
      max_new_tokens=512,  # mex number of tokens to generate in the output
    )
  
    hfPipeline = pipeline(
        model=model, tokenizer=tokenizer,
        task='text-generation',
        generation_config=generationConfig
    )
    llm = HuggingFacePipeline(pipeline=hfPipeline)

    prompt_template = get_prompt(instruction)
    
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
    
  def query(self, query: str):
    # docs = self.retriever.get_relevant_documents(query)
    # res = str([doc.metadata["name"] for doc in docs])
    
    print(self.chain.combine_documents_chain.llm_chain.prompt.template)
    res = self.chain.run(query)
    
    return res

if __name__ == "__main__":
  chain = CourseLangChain()
  fire.Fire(chain.query)