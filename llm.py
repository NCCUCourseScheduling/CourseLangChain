from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.manager import CallbackManager
from utils.callback import ChainStreamHandler

callback_manager = CallbackManager([ChainStreamHandler()])

llm = LlamaCpp(
  model_path="model/chinese-alpaca-2-13b.Q8_0.gguf",
  callback_manager=callback_manager,
  n_gpu_layers=100,
  n_batch=512,
  n_ctx=4096,
  verbose=True,  # Verbose is required to pass to the callback manager
)

if __name__ == "__main__":
  template = """Question: {question}\nAnswer: Let's work this out in a step by step way to be sure we have the right answer."""
  prompt = PromptTemplate(template=template, input_variables=["question"])

  llm_chain = LLMChain(prompt=prompt, llm=llm)
  question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"
  llm_chain.run(question)