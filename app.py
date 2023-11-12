import os
import uuid
import whisper
from flask import Flask, request, Response, stream_with_context, jsonify, abort
from main import CourseLangChain

UPLOAD_FOLDER = './uploads'
 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

@app.route('/api/upload', methods=['POST'])
def upload_file():
  if request.method == 'POST':
    # check if the post request has the file part
    if 'file' not in request.files:
      abort(500, "No file part")
    file = request.files['file']
    if file.filename == '':
      abort(500, "No selected file")
    id = uuid.uuid4()
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], f"{id}.mp3"))
    result = model.transcribe(os.path.join(app.config['UPLOAD_FOLDER'], f"{id}.mp3"))
    return {"text": result["text"]}

@app.errorhandler(500)
def custom400(error):
    return jsonify({'message': error.description})

if __name__ == "__main__":
  try:
    model = whisper.load_model("medium")
    chain = CourseLangChain()
    app.run(port=59014)
  finally:
    print("Deleting chain...")
    del chain