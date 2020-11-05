#!/usr/bin/env python3
import gzip, base64, os
from xml.dom import minidom
from flask import Flask, render_template, request
#from . import app
app = Flask(__name__)

def leadingZero(number, digits = 2):
    return str(number).zfill(digits)

def getOffsetTime(time, tempo, getFrames = True):
    time = time / (tempo / 120 * 2)
    minutes = int(time / 60)
    seconds = int(round(time - minutes * 60, 0))
    frames = 0

    if getFrames:
        return "%s:%s:%s" % (leadingZero(minutes), leadingZero(seconds), leadingZero(frames))
    else:
        return "%s:%s" % (leadingZero(minutes), leadingZero(seconds))

def getChapters(als, filename):
    try:
        raw_data = gzip.decompress(als)
        doc = minidom.parseString(raw_data)
        tempo = float(doc.getElementsByTagName('Tempo')[0].getElementsByTagName('Manual')[0].getAttribute('Value'))

        locators = doc.getElementsByTagName('Locator')

        if len(locators) < 1:
            return (False, "No Ableton markers found")

        print("Found %s Ableton markers" % str(len(locators)))

        cue = '''TITLE "EasyPodcast"
        PERFORMER "EasyPodcast"
        FILE "%s" MP3
        ''' % (filename)
        list = ""

        timestamps = [0.0]
        chapters = []

        for locator in locators:
            time = float(locator.getElementsByTagName('Time')[0].getAttribute('Value'))
            timestamps.append(time)

        timestamps.sort()

        j = 0
        for time in timestamps:
            j += 1
            cue += "  TRACK " + leadingZero(j) + " AUDIO" + '''
            TITLE ""
            PERFORMER "EasyPodcast"''' + "\n    INDEX 01 "+ getOffsetTime(time, tempo) + "\n"
            list += getOffsetTime(time, tempo) + "\n"
            if j > 1:
                print(" %s. %s" % (str(j - 1), getOffsetTime(time, tempo, False)))
                chapters.append({"chapter_number": j - 1, "chapter_start": getOffsetTime(time, tempo, False)})

        return (True, chapters, cue, base64.b64encode(cue.encode('utf-8')).decode('utf-8'))

    except Exception as e:
        print("Can't read Ableton project", e)
        return (False, "Can't read Ableton project")

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
                print(cue_base64)
                return render_template("chapters.html", chapters=chapters, cue=cue, cue_base64=cue_base64)
            else:
                return render_template("error.html", error_title=details[0])
        return render_template("error.html", error_title="No file uploaded", error_text="You have not uploaded any file. Go back and try again.")
    else:
        return uploadForm()

if __name__ == "__main__":
    app.run(debug=("DEBUG" in os.environ))
