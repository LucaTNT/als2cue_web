#!/usr/bin/env python3
import os
from flask import Flask, render_template, request
from als2cue import getChapters

app = Flask(__name__)

@app.route("/")
def uploadForm():
    return render_template("upload.html")

@app.route("/upload", methods=["GET", "POST"])
def handleUpload():
    if request.method == 'POST':
        if ("als" in request.files and request.files["als"].filename != ""):
            valid_chapters, *details = getChapters(request.files["als"].read(), request.files["als"].filename)
            if valid_chapters:
                chapters, cue, cue_base64 = details
                return render_template("chapters.html", chapters=chapters, cue=cue, cue_base64=cue_base64)
            else:
                return render_template("error.html", error_title=details[0])
        return render_template("error.html", error_title="No file uploaded", error_text="You have not uploaded any file. Go back and try again.")
    else:
        return uploadForm()

if __name__ == "__main__":
    app.run(debug=("DEBUG" in os.environ))
