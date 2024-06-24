import sqlite3
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
import os


conn = sqlite3.connect('data.db')
cursor = conn.cursor()


query = "SELECT nameEn, timeEn, teacherEn, unitEn FROM COURSE WHERE y = 112 AND s = 1"
cursor.execute(query)
rows = cursor.fetchall()


documents = []
for row in rows:
    nameEn, timeEn, teacherEn, unitEn = row  # 假設這些欄位正確對應於你的數據庫結構
    page_content = f"the course name is {nameEn.lower()}, the course is given at {timeEn}, the teacher is {teacherEn}"
    metadata = {
        "name": nameEn,
        "time": timeEn,
        "teacher": teacherEn,
        "unit": unitEn
    }
    documents.append(Document(page_content=page_content, metadata=metadata))


model_name = "BAAI/bge-m3"
encode_kwargs = {'normalize_embeddings': True} 

embedding_function = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs={'device': 'cpu'},
    encode_kwargs=encode_kwargs,
)


persist_directory = './chroma_db'


chroma_db = Chroma.from_texts([doc.page_content for doc in documents], embedding_function, persist_directory=persist_directory)


for i, doc in enumerate(documents[:3]):
    print(f"Document {i+1}:")
    print(f"Page Content: {doc.page_content}")
    print("Metadata:")
    for key, value in doc.metadata.items():
        print(f"  {key}: {value}")
    print()

print("Chroma DB has been created and is ready for use.")
