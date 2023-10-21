from flask import Flask, request, Response, stream_with_context
from main import CourseLangChain
 
app = Flask(__name__)

chain = CourseLangChain()

@app.route('/ask', methods=['GET'])
def main():
  args = request.args
  question = args.get("question")
  chain.handler.finish = False
  if question:
    return Response(stream_with_context(chain.query(question)), mimetype='text/event-stream')
  else:
    return Response("None", mimetype="text/html")

if __name__ == "__main__":
  app.run(port=59014)