from flask import Flask
from flask_rq2 import RQ
import demucs.separate
from os.path import join
import time

app = Flask(__name__)

def separate_song_parts(path, model='htdemucs', jobs=1):
    demucs.separate.main(['-n',model, '--mp3', '-j', jobs, '--two-stems', 'vocals', path])

@app.route("/api/python")
def hello_world():
    path = join('data', 'file.mp4')
    start_time = time.time()
    separate_song_parts(path)
    seconds = time.time() - start_time
    minutes = seconds / 60
    return f"Separation took {minutes:.2f} minutes"
