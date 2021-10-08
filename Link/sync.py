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


class Direction:
    direction = 1  # defaults to forward

    def __init__(self):
        pass

    def choose_direction(self, direction):
        self.direction = direction

    def move(self, ping, pattern):
        if self.direction == 2:
            pattern = pattern * 2
            print('ping', ping)
            ping = abs(ping - 1)
        boom = ping % pattern
        position = boom / pattern
        return position
