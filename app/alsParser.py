#!/usr/bin/env python3
import gzip, base64
from xml.dom import minidom

def getOffsetTime(time_beats, tempo_intervals):
    total_seconds = 0
    remaining_beats = time_beats
    for tempo_interval in tempo_intervals:
        bpm = tempo_interval["bpm"]
        interval_duration = (tempo_interval["beats_end"] - tempo_interval["beats_start"])
        if tempo_interval["beats_start"] < time_beats:
            if (time_beats > tempo_interval["beats_end"] and tempo_interval["beats_end"] != -1):
                interval_seconds = interval_duration / (bpm / 60)
                total_seconds += interval_seconds
                remaining_beats -= interval_duration
            else:
                total_seconds += remaining_beats / (bpm / 60)
        
    return total_seconds

def getLocators(als):
    locators = als.getElementsByTagName('Locator')

    timestamps = [0.0]

    for locator in locators:
        time = float(locator.getElementsByTagName('Time')[0].getAttribute('Value'))
        timestamps.append(time)
    timestamps.sort()

    return timestamps

def als2xml(als_file):
    try:
        ableton_project_handle = gzip.open(als_file, 'r')
        raw_data = ableton_project_handle.read()
        ableton_project_handle.close()

        return minidom.parseString(raw_data)
    except Exception as e:
        print("Can't read Ableton project")
        print(e)
        raise

def raw2xml(raw_data):
    try:
        uncompressed_data = gzip.decompress(raw_data)
        return minidom.parseString(uncompressed_data)
    except Exception as e:
        print("Can't read Ableton project")
        print(e)
        raise

def getTempoAutomationId(als):
    try:
        return int(als.getElementsByTagName('Tempo')[0].getElementsByTagName('AutomationTarget')[0].getAttribute('Id'))
    except Exception as e:
        print("Can't find Tempo Automation Id")
        print(e)
        raise

def getTempoChanges(als):
    try:
        tempo_pointee_id = getTempoAutomationId(als)
        tempo_changes = []

        envelopes = als.getElementsByTagName('MasterTrack')[0].getElementsByTagName('AutomationEnvelope')
        for envelope in envelopes:
            pointee_id = int(envelope.getElementsByTagName("PointeeId")[0].getAttribute("Value"))
            if (pointee_id == tempo_pointee_id):
                events = envelope.getElementsByTagName("Events")[0].childNodes
                for event in events:
                    if event.nodeName != "#text":
                        time = float(event.getAttribute("Time"))
                        value = float(event.getAttribute("Value"))

                        if time < 0:
                            time = 0
                        tempo_changes.append({"time_beats": time, "bpm": value})
        return tempo_changes
    except Exception as e:
        print("Can't read Ableton project")
        print(e)
        raise

def getTempoIntervals(tempo_changes):
    tempo_intervals = []
    previous_time = 0
    previous_bpm = 0
    for tempo_change in tempo_changes:
        time_beats = tempo_change["time_beats"]
        bpm = tempo_change["bpm"]
        if (time_beats > 0 and time_beats > previous_time):
            tempo_intervals.append({"beats_start": previous_time, "beats_end": time_beats, "bpm": bpm})

        previous_time = time_beats
        previous_bpm = bpm
    tempo_intervals.append({"beats_start": previous_time, "beats_end": -1, "bpm": previous_bpm})
    return tempo_intervals
