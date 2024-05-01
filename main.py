import threading, sqlite3, logging, pickle
import fire
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.llms.llamacpp import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from utils.prompt import get_prompt
from utils.callback import ChainStreamHandler
from detector import NegationDetector
from langchain.retrievers import EnsembleRetriever
from langchain.memory import ConversationBufferWindowMemory
from dotenv import load_dotenv
import os

# remember to add the .env file in order to use Langsmith API
load_dotenv()

MODAL_PATH = os.getenv("MODEL_PATH")

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
        modelFile=MODAL_PATH,
        cli=False,
    ) -> None:

        # Model Name Defination
        prompt = get_prompt()
        # logger.info("Prompt Template:\n" + prompt)

        with open(pickleFile, "rb") as f:
            retriever: EnsembleRetriever = pickle.load(f)

        self.handler = (
            ChainStreamHandler() if not cli else StreamingStdOutCallbackHandler()
        )

        model = LlamaCpp(
            model_path=modelFile,
            callback_manager=CallbackManager([self.handler]),
            n_gpu_layers=43,
            n_batch=512,
            n_ctx=4096,
            f16_kv=True,
            verbose=True,  # Verbose is required to pass to the callback manager
        )

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


def main():
    chain = CourseLangChain(cli=True)
    while True:
        query = input("User:")
        print("Bot:")
        chain.invoke(query)


if __name__ == "__main__":
    fire.Fire(main)
