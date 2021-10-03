import math


class Sync:
    bpm = 120
    time_signature = (4, 4)

    def __init__(self, bpm, time_signature):
        self.bpm = bpm
        self.one_beat_ms = float(60 / self.bpm)  # one beat in milliseconds

    def pattern(self, duration):
        total_beats = duration // self.one_beat_ms
        bars = total_beats // self.time_signature[0]
        print('bars', bars)
        square = math.log(bars, 2)
        print('rounded', pow(2, round(square)))
        return pow(2, round(square))


class Frame_watcher:

    def __init__(self):
        self.frame = None

    def new_frame_is_not_equal_to(self, frame):
        yield frame != self.frame
        self.frame = frame
