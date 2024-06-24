from urllib import response
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo, StructuredQueryOutputParser, get_query_constructor_prompt
from langchain_community.llms import Ollama
import os
import time


os.environ["TOKENIZERS_PARALLELISM"] = "false"


embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")


#llm = Ollama(model="cwchang/llama3-taide-lx-8b-chat-alpha1", stop=["<|eot_id|>"])
llm = Ollama(model="llama3")



model_name = "BAAI/bge-m3"
encode_kwargs = {'normalize_embeddings': True} 

embedding_function = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs={'device': 'cpu'},
    encode_kwargs=encode_kwargs,
)
persist_directory = "./chroma_db"
chroma_db = Chroma(persist_directory=persist_directory, embedding_function=embedding_function)



print("Vectorstore ready")


metadata_field_info = [
    AttributeInfo(
        name="name",
        description="the name of the course",
        type="string or list[string]",
    ),
    AttributeInfo(
        name="y",
        description="The academic year the course is given in",
        type="string or list[string]",
    ),
    AttributeInfo(
        name="time",
        description="The time the course is given at",
        type="string or list[string]",
    ),
    AttributeInfo(
        name="teacher",
        description="The name of the teacher",
        type="string or list[string]",
    ),
    AttributeInfo(
        name="unit",
        description="The department the course belongs to",
        type="string or list[string]",
    ),
]
print("Metadata field info ready")


document_content_description = "Brief description of the course"


retriever = SelfQueryRetriever.from_llm(
    llm, chroma_db, 
    document_content_description, 
    metadata_field_info, 
    verbose=True,
    k=5
)



#response = retriever.invoke("Tell me about Management course?")
#response = retriever.invoke("Tell me about the course given in the year 112-1")
#response = retriever.invoke("Tell me about the course whose time is Wednesday 8910.")
#response = retriever.invoke("告訴我管理學相關課程?")

#print(response)

###格式化輸出
def extract_and_print_page_contents(input_string):

    if input_string.startswith("Document("):
        input_string = input_string[len("Document("):]
    if input_string.endswith(")"):
        input_string = input_string[:-1]
    
    input_string = input_string.replace("), Document(", ")|")
    documents = input_string.split("|")
    
    for doc in documents:
        start = doc.find("page_content='") + len("page_content='")
        end = doc.find("',", start)
        page_content = doc[start:end]
        print(page_content)
#########################


print("Ready:")
while True:
    query = input("Enter your query: ")
    start_time = time.time()
    response = retriever.invoke(query)
    #print(response)
    extract_and_print_page_contents(str(response))
    end_time = time.time() 
    elapsed_time = end_time - start_time  
    print(f"Query processed in {elapsed_time:.2f} seconds")

