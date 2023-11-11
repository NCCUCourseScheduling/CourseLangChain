import whisper
from flask import Flask, request, Response, stream_with_context, render_template
from main import CourseLangChain
 
app = Flask(__name__)

def chain_run(query):
  chain = CourseLangChain(cli=True)
  while True:
    print(query)
    print("Bot:")
    chain.chain.run(query)


@app.route('/')
def base():
    return render_template('index.html')


@app.route('/save_sound', methods=['POST'])
def save_sound_route():
    sound = request.files['sound']
    sound.save("sound.wav")
    return "录音已保存"


@app.route('/convert_audio')
def convert_audio():
    # 在这里进行音频转文本的处理，已经将转换后的文本保存在变量 text 中
    model = whisper.load_model("base")
    result = model.transcribe("sound.wav")
    text = result["text"]
    chain_run(text)
    return text


if __name__ == '__main__':
    app.run(debug=True)