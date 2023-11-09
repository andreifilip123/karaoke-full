from flask import Flask
import demucs.separate
from os.path import join

app = Flask(__name__)

@app.route("/api/python")
def hello_world():
    path = join('data', 'file.mp4')
    demucs.separate.main(["--mp3", "--two-stems", "vocals", path])
    return "<p>Hello, World!</p>"