#!/usr/bin/env python3
import base64
import dawtool

def leadingZero(number, digits = 2):
    return str(number).zfill(digits)

def formatTimestamp(total_seconds, getFrames = True):
    minutes = int(total_seconds / 60)
    seconds = int(round(total_seconds - minutes * 60, 0))
    
    if not getFrames:
        return "%s:%s" % (leadingZero(minutes), leadingZero(seconds))
    
    frames = 0
    return "%s:%s:%s" % (leadingZero(minutes), leadingZero(seconds), leadingZero(frames))

def getChapters(stream, filename):
    try:
        locators = dawtool.extract_markers(filename, stream)

        if len(locators) < 1:
            return (False, "No Ableton markers found")

        chapters = []
        cue = "FILE \"%s.mp3\" MP3\n" % filename

        for j, locator in enumerate(locators, start=1):
            # Make sure there's always a chapter at the beginning
            j_offset = 0
            if locator.time > 0 and j == 1:
                cue += "    TRACK 01 AUDIO\n"
                cue += "        TITLE \"\"\n"
                cue += "        INDEX 01 %s\n" % formatTimestamp(0)
                chapters.append({
                    "chapter_number": j + j_offset, 
                    "chapter_start": formatTimestamp(0),
                    "chapter_title": ""
                })
                j_offset = 1

            cue += "    TRACK %s AUDIO\n" % leadingZero(j + j_offset)
            cue += "        TITLE \"%s\"\n" % locator.text.replace("\"", "\\\"")
            cue += "        INDEX 01 %s\n" % formatTimestamp(locator.time)
            chapters.append({
                "chapter_number": j + j_offset, 
                "chapter_start": formatTimestamp(locator.time),
                "chapter_title": locator.text
            })

        return (True, chapters, cue, base64.b64encode(cue.encode('utf-8')).decode('utf-8'))

    except Exception as e:
        return False, f"Can't read Ableton project - {e}"
