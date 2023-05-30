import sys
import os
from time import sleep
from flask import Response, jsonify, request, Flask
from flask_cors import CORS
import openai
from uuid import uuid4

app = Flask(__name__, static_folder='public')
CORS(app)
app.config["UPLOAD_DIR"] = "uploads"

# req_id: {generator, }
reqQueue = {}


@app.route('/test', methods=["GET"])
def test():
    def gen():
        cnt = 0
        while True:
            sleep(1)
            cnt += 1
            yield f"{cnt}\n"
    return Response(gen(), mimetype='text/plain')


@app.route('/post_webm', methods=["POST"])
def post_webm():
    file = request.files['file']
    name = f'{str(uuid4())}.webm'
    pth = os.path.join(app.config['UPLOAD_DIR'], name)
    file.save(pth)

    with open(pth, 'rb') as f:
        text = useWhisper(f)

    os.remove(pth)

    req_id = str(uuid4())

    gen = useChat(text)
    reqQueue[req_id] = gen

    return jsonify({"text": text, "req_id": req_id})


@app.route('/get_chat_res', methods=["GET"])
def get_chat_res():
    req_id = request.args.get('req_id')
    gen = reqQueue.get(req_id)

    if gen:
        reqQueue.pop(req_id)
        return Response(gen, mimetype='text/plain')
    else:
        return Response(status=400)


def useWhisper(file):
    # audio_file = open(file, "rb")
    transcript = openai.Audio.transcribe("whisper-1", file)
    return transcript['text']
    # print(transcript["text"])


def useChat(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.7,
        messages=[
            {"role": "system", "content": "あなたは役に立つアシスタントです。"},
            {"role": "user", "content": prompt}
        ],
        stream=True
    )
    print(prompt)
    print(response)
    # response_text = ""
    for chunk in response:
        if chunk:
            content = chunk["choices"][0]["delta"].get('content')
            if content:
                # response_text += content
                yield content
    # return response_text


if __name__ == "__main__":
    # print(app.url_map)
    # app.run()
    app.run(host="0.0.0.0")


'''
from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route("/upload", methods = ["GET", "POST"])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_DIR'], file.filename))
        return render_template("upload.html", msg = "File uplaoded successfully.")

    return render_template("upload.html", msg = "")

if __name__ == "__main__":
    app.run()
'''
