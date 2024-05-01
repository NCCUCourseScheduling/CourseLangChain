from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from main import CourseLangChain

app = FastAPI()


async def generate(query):
    async for chunk in chain.chain.astream(query):
        yield chunk


@app.get("/api/ask")
async def main(question:str = "你好"):
    return StreamingResponse(generate(question))

if __name__ == "__main__":
    chain = None
    try:
        import uvicorn
        chain = CourseLangChain()
        uvicorn.run(app, host="localhost", port=59014)
    finally:
        print("Deleting chain...")
        del chain
    

