import sys
import os

# 🔹 FIX: Ensure current folder is first in module search path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, send_from_directory
from text_to_video import generate_video
from text_to_voice import generate_voice

app = Flask(__name__)

print("Current directory:", os.getcwd())
print("Templates folder exists:", os.path.exists(os.path.join(os.getcwd(), "templates")))

# Video save folder
VIDEO_FOLDER = os.path.join("static", "videos")
os.makedirs(VIDEO_FOLDER, exist_ok=True)

# Audio save folder
AUDIO_FOLDER = os.path.join("static", "audios")
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# ---------------- Routes ---------------- #

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/generate")
def generate():
    return render_template("generate.html")

@app.route("/text-to-video")
def text_to_video_page():
    return render_template("text_to_video.html")

@app.route("/text-to-voice")
def text_to_voice_page():
    return render_template("text_to_voice.html")

# Generate Video
@app.route("/generate-video", methods=["POST"])
def generate_video_route():
    user_text = request.form.get("user_text")
    if not user_text:
        return "Please enter some text!", 400

    video_path = os.path.join(VIDEO_FOLDER, "output.mp4")
    generate_video(user_text, video_path)

    return render_template("result.html", video_file=video_path)

# Generate Voice
@app.route("/generate-voice", methods=["POST"])
def generate_voice_route():
    user_text = request.form.get("text")
    if not user_text:
        return "Please enter some text!", 400

    audio_path = os.path.join(AUDIO_FOLDER, "output_audio.wav")
    generate_voice(user_text, audio_path)

    return send_from_directory(AUDIO_FOLDER, "output_audio.wav", as_attachment=False)

# Download video
@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(VIDEO_FOLDER, filename, as_attachment=True)

# ---------------- Run App ---------------- #
if __name__ == "__main__":
    app.run(debug=True)

