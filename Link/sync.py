import math


class Sync:
    bpm = 120
    time_signature = (4, 4)

    def __init__(self, bpm, time_signature):
        self.bpm = bpm
        self.one_beat_ms = float(60 / self.bpm)  # one beat in seconds

    def pattern(self, duration):
        """
        duration is a clip's length in milliseconds
        """
        total_beats = duration // self.one_beat_ms
        bars = total_beats // self.time_signature[0]
        if bars < 1:
            bars = 1
        print("bars", bars)
        square = math.log(bars, 2)
        print("rounded", pow(2, round(square)))
        return pow(2, round(square))


class Frame_watcher:
    def __init__(self):
        self.frame = None

    def new_frame_is_not_equal_to(self, frame):
        yield frame != self.frame
        self.frame = frame


class Direction:
    direction = 1  # defaults to forward (0 is backward, 2 is palindrome)
    offset = 0

    def __init__(self):
        pass

    def choose_direction(self, direction):
        self.direction = direction

    def move(self, ping, pattern):
        self.ping = ping
        if self.direction == 2:
            self.pattern = pattern * 2
            self.palindrome()
        else:
            self.pattern = pattern
            if self.direction == 0:
                self.backward()
            if self.direction == 1:
                self.forward()

        return self.position

    def render_position(self):
        self.position = (self.ping - self.offset) % self.pattern / self.pattern

    def backward(self):
        self.render_position()
        self.position = abs(self.position - 1)

    def forward(self):
        self.render_position()
        self.position = self.position

    def palindrome(self):
        self.render_position()
        self.position = abs(self.position * 2 - 1)

    def off_set(self):
        self.offset = self.ping
