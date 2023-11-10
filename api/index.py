from flask import Flask, request
from flask_rq2 import RQ
import demucs.separate
from os.path import join
import time

app = Flask(__name__)
rq = RQ(app)


@rq.job
def separate_song_parts(path, model="htdemucs", jobs='1'):
    demucs.separate.main(
        ["-n", model, "--mp3", "-j", jobs, "--two-stems", "vocals", path]
    )


@app.route("/api/separate", methods = ['POST', 'GET'])
def separate():
    if request.method == 'POST':
        path = request.form.get('path', join("data", "file.mp4"))
    else:
        path = join("data", "file.mp4")

    job = separate_song_parts.queue(path)
    status = job.get_status()

    return '<a href="/api/jobs/' + job.id + '/status">' + status + "</a>"

@app.route("/api/jobs/<job_id>/status")
def job_status(job_id):
    job = rq.get_queue().fetch_job(job_id)
    if job is None:
        return "No such job", 404
    return job.get_status()
