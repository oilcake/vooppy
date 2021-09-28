import math


class Sync:
    bpm = 120
    time_signature = (4, 4)

    def __init__(self, bpm, time_signature):
        self.bpm = bpm
        self.one_beat_ms = float(60 / self.bpm)

    def pattern(self, duration):
        total_beats = duration / self.one_beat_ms
        beats_lg = math.log(total_beats, 2)
        return pow(2, round(beats_lg))


class Frame_watcher:

    def __init__(self):
        self.frame = None

    def nextframe(self, frame):
        return frame != self.frame
