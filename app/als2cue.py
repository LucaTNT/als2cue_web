#!/usr/bin/env python3
import alsParser, base64, sys

def leadingZero(number, digits = 2):
    return str(number).zfill(digits)

def formatTimestamp(total_seconds, getFrames = True):
    minutes = int(total_seconds / 60)
    seconds = int(round(total_seconds - minutes * 60, 0))
    frames = 0

    if getFrames:
        return "%s:%s:%s" % (leadingZero(minutes), leadingZero(seconds), leadingZero(frames))
    else:
        return "%s:%s" % (leadingZero(minutes), leadingZero(seconds))

def getChapters(raw_data, filename):
    try:
        als = alsParser.raw2xml(raw_data)
        tempo_changes = alsParser.getTempoChanges(als)
        tempo_intervals = alsParser.getTempoIntervals(tempo_changes)
        locators = alsParser.getLocators(als)

        if len(locators) < 1:
            return (False, "No Ableton markers found")

        chapters = []
        cue = "FILE \"%s.mp3\" MP3\n" % filename

        j = 0
        for time in locators:
            j += 1
            cue += "    TRACK %s AUDIO\n" % leadingZero(j)
            cue += "        TITLE \"\"\n"
            cue += "        INDEX 01 %s\n" % formatTimestamp(time, alsParser.getOffsetTime(time, tempo_intervals))
            if j > 1:
                chapters.append({"chapter_number": j - 1, "chapter_start": formatTimestamp(alsParser.getOffsetTime(time, tempo_intervals), False)})

        return (True, chapters, cue, base64.b64encode(cue.encode('utf-8')).decode('utf-8'))

    except:
        return (False, "Can't read Ableton project")
