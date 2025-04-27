import os, uuid
from flask import Flask, request, jsonify, send_from_directory, render_template_string
from modules.stt import transcribe
from modules.amazon_q import ask
from modules.public_voice import synthesize
from modules.musetalk_wrapper import animate

app = Flask(__name__, static_folder="static")
ASSETS = "assets"
TMP = os.getenv("TMP", ".")

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/talk", methods=["POST"])
def talk():
    audio_file = request.files["audio"]
    sess = str(uuid.uuid4())
    in_wav = f"{TMP}/{sess}_in.wav"
    audio_file.save(in_wav)

    user_text = transcribe(in_wav)
    q_text = ask(user_text, session_id=sess)

    idol_wav = f"{TMP}/{sess}_idol.wav"
    synthesize(q_text, idol_wav)

    out_mp4 = f"static/{sess}_out.mp4"
    animate(idol_wav, os.path.join(ASSETS, "idol_face.jpg"), out_mp4)

    return jsonify({"text": q_text, "video": f"/{out_mp4}"})

if __name__ == "__main__":
    app.run(debug=True)