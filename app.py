from main import CourseLangChain
import chainlit as cl

chain = CourseLangChain()

@cl.on_chat_start
def main():

  # Store the chain in the user session
  cl.user_session.set("llm_chain", chain)


@cl.on_message
async def main(message: str):
    # Retrieve the chain from the user session
    _chain = cl.user_session.get("llm_chain")  # type: LLMChain

    # Call the chain asynchronously
    res = await cl.make_async(_chain.query)(
        message
    )

    # Do any post processing here

    # "res" is a Dict. For this chain, we get the response by reading the "text" key.
    # This varies from chain to chain, you should check which key to read.
    await cl.Message(content=res).send()
    return _chain