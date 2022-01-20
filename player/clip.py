import json
import os

import cv2
import librosa

import sounddevice as sd


DEFAULT_PREFS = {
    "multiplier": 1,
    "palindrome": 0,
    "direction": 1,
}


def find_prefs(video, extension) -> str:
    filename, file_extension = os.path.splitext(video)
    name = filename + extension
    return name


class Clip:
    framecount = None
    dim = (0, 0)
    fps = 0
    duration = 0
    audio = None
    prefs = None

    def __init__(self, clip):
        self.filename = clip
        # open a stream
        self.clip = cv2.VideoCapture(self.filename)
        if not self.clip.isOpened():
            print("Error opening video stream or file")
        # get number of frames in video
        self.framecount = int(self.clip.get(cv2.CAP_PROP_FRAME_COUNT))
        self.find_duration()
        self.get_dimensions()

        self.prefs = find_prefs(self.filename, ".json")

        # WARNING! Don't forget to delete this line
        self.wipe_prefs()

        if not os.path.isfile(self.prefs):
            print("OOOPS")
            self.wipe_prefs()

    def wipe_prefs(self):
        try:
            os.remove(self.prefs)
        except FileNotFoundError:
            with open(self.prefs, "w") as prefs:
                prefs.write(self.filename)
                print("", file=prefs)
                data = json.dumps(DEFAULT_PREFS)
                prefs.write(data)
                print("Done!")

    def update_prefs(self, _prefs):
        with open(self.prefs, "a") as prefs:
            data = json.dumps(_prefs)
            prefs.write(data)
            print("Done!")

    def read_prefs(self, _prefs):
        with open(self.prefs, "r") as prefs:
            data = json.dumps(_prefs)
            prefs.write(data)
            print("Done!")

    def get_dimensions(self):
        width = int(self.clip.get(3))  # float `width`
        height = int(self.clip.get(4))  # float `height`
        self.dim = (width, height)

    def play(self, frame_number):
        if not frame_number > self.framecount:
            self.clip.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = self.clip.read()
            if ret:
                return frame

    def find_duration(self):
        self.fps = int(self.clip.get(cv2.CAP_PROP_FPS))
        # calculate duration of the video
        milliseconds = self.framecount / self.fps
        self.duration = milliseconds * 4

    def __repr__(self):
        return self.filename

    def close(self):
        self.clip.release()


class Audio:
    ratio = 1
    soundfile = None
    length = 0

    def __init__(self, videofile: str) -> None:
        prefs = find_prefs(videofile, ".aiff")
        if os.path.isfile(prefs):
            self.soundfile = prefs
            self.data, self.fs = librosa.load(self.soundfile)
            self.stretched = librosa.effects.time_stretch(self.data, self.ratio)
            self.length = len(self.stretched)

    def play(self, index):
        if self.soundfile is not None:
            buffer = 8192
            chunk = self.stretched[index : index + buffer]
            sd.play(chunk, self.fs)
