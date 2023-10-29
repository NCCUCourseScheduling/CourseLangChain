from flask import Flask, request, Response, stream_with_context
from main import CourseLangChain
 
app = Flask(__name__)

@app.route('/api/ask', methods=['GET'])
def main():
  args = request.args
  question = args.get("question")
  # Lock here
  if question and chain.handler.finish:
    chain.handler.finish = False
    chain.handler.tokens = []
    return Response(stream_with_context(chain.query(question)), mimetype='text/event-stream')
  else:
    return Response("None", mimetype="text/html")

if __name__ == "__main__":
  try:
    chain = CourseLangChain()
    app.run(port=59014)
  finally:
    print("Deleting chain...")
    del chain