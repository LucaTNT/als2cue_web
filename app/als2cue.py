#!/usr/bin/env python3
import gzip, base64, os
from xml.dom import minidom

def leadingZero(number, digits = 2):
    return str(number).zfill(digits)

def getOffsetTime(time, tempo, getFrames = True):
    time = time / (tempo / 60)
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

        cue = "FILE \"%s.mp3\" MP3\n" % filename

        timestamps = [0.0]
        chapters = []

        for locator in locators:
            time = float(locator.getElementsByTagName('Time')[0].getAttribute('Value'))
            timestamps.append(time)

        timestamps.sort()

        j = 0
        for time in timestamps:
            j += 1
            cue += "    TRACK %s AUDIO\n" % leadingZero(j)
            cue += "        TITLE \"\"\n"
            cue += "        INDEX 01 %s\n" % getOffsetTime(time, tempo)
            if j > 1:
                chapters.append({"chapter_number": j - 1, "chapter_start": getOffsetTime(time, tempo, False)})

        return (True, chapters, cue, base64.b64encode(cue.encode('utf-8')).decode('utf-8'))

    except Exception as e:
        return (False, "Can't read Ableton project")
