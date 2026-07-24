#!/usr/bin/env python3
import base64
import dawtool

def leadingZero(number, digits = 2):
    return str(number).zfill(digits)

def formatTimestamp(total_seconds, getFrames = True):
    # CUE sheets use 75 frames per second, if Wikipedia is to be believed
    total_frames = int(round(total_seconds * 75))
    total_seconds_from_frames = total_frames // 75
    minutes = total_seconds_from_frames // 60
    seconds = total_seconds_from_frames % 60
    frames = total_frames % 75
    
    if not getFrames:
        return "%s:%s" % (leadingZero(minutes), leadingZero(seconds))
    
    return "%s:%s:%s" % (leadingZero(minutes), leadingZero(seconds), leadingZero(frames))

def getChapters(stream, filename):
    try:
        locators = sorted(dawtool.extract_markers(filename, stream), key=lambda l: l.time)

        if len(locators) < 1:
            return (False, "No Ableton markers found")

        chapters = []
        cue = "FILE \"%s.mp3\" MP3\n" % filename.replace("\"", "\\\"")

        # Make sure there's always a chapter at the beginning
        j_offset = 1 if locators[0].time > 0 else 0

        for j, locator in enumerate(locators, start=1):
            if locator.time > 0 and j == 1:
                cue += "    TRACK 01 AUDIO\n"
                cue += "        TITLE \"\"\n"
                cue += "        INDEX 01 %s\n" % formatTimestamp(0)
                chapters.append({
                    "chapter_number": 1,
                    "chapter_start": formatTimestamp(0),
                    "chapter_title": ""
                })

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
