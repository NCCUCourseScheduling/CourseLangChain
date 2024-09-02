import logging, pickle
import fire
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
from utils.prompt import get_prompt
from langchain.retrievers import EnsembleRetriever
from dotenv import load_dotenv
import os

# remember to add the .env file in order to use Langsmith API
load_dotenv()

MODAL = os.getenv("MODEL")

logger = logging.getLogger("CourseLangchain")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


class CourseLangChain:
    def __init__(
        self,
        pickleFile="vectorstore.pkl",
        cli=False,
    ) -> None:

        # Model Name Defination
        prompt = get_prompt()
        # logger.info("Prompt Template:\n" + prompt)

        with open(pickleFile, "rb") as f:
            retriever: EnsembleRetriever = pickle.load(f)
        
        model = Ollama(model=MODAL, stop=["<|eot_id|>"])

        def format_docs(docs):
            return "\n".join(f"- {doc.page_content}" for doc in docs)

        self.chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
        )
        logger.info("Chain ready.")

    def invoke(self, input) -> str:
        return self.chain.invoke(input)


async def main():
    chain = CourseLangChain(cli=True)
    while True:
        query = input("User:")
        print("Bot:")
        async for chunk in chain.chain.astream(query):
            print(chunk, end="", flush=True)


if __name__ == "__main__":
    fire.Fire(main)
