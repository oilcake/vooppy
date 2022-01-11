import math
import random


class Sync:
    bpm = 120
    time_signature = (4, 4)

    def __init__(self, bpm, time_signature):
        self.bpm = bpm
        self.one_beat_ms = float(60 / self.bpm)  # one beat in seconds
        self.one_bar_ms = self.one_beat_ms * self.time_signature[0]  # one bar in seconds

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
        rounded = pow(2, round(square))
        print("rounded", rounded)
        return rounded


class FrameWatcher:
    def __init__(self):
        self.frame = None

    def new_frame_is_not_equal_to(self, frame):
        yield frame != self.frame
        self.frame = frame


class Change:
    after = None
    ping = None
    bar_duration = (4, 4)

    def detected_beat_change(self, ping):
        self.ping = ping
        before = int(self.ping)
        if self.after is None:
            self.after = before
        if before != self.after:
            return True
        return False

    def detected_bar_change(self, ping):
        if self.detected_beat_change(ping):
            beat = int(self.ping) % self.bar_duration[0]
            print(f"beat number is {beat}")
            return beat == 0
        return False


class Direction:
    direction = 1  # defaults to forward (0 is backward, 2 is palindrome)
    offset = 0
    jump_to = 0
    pattern = 0
    ping = None
    position = 0
    detector = Change()

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
        bars_now = self.ping - self.offset
        self.position = (bars_now + self.jump_to) % self.pattern / self.pattern

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
        self.jump_to = 0
        self.offset = self.ping
        print(self.offset)

    def jump(self):
        jump = random.randint(1, int(self.pattern))
        self.jump_to = jump
