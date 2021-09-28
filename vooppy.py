import argparse
import random

import cv2

from player.clip import Clip
from files.files import filter_files
from Link.client import Client
from Link.sync import Sync, Frame_watcher


parser = argparse.ArgumentParser(description='arguments')
parser.add_argument("input", help="Input directory", type=str)
args = parser.parse_args()

folder = args.input

link = Client()
sync = Sync(link.bpm, (4, 4))
watcher = Frame_watcher()

files = list(filter_files(folder))
while True:
    index = random.randint(0, len(files))
    file = files[index]
    clip = Clip(file)
    pattern = int(sync.pattern(clip.duration) / 2)
    print(clip)
    print('total frames', clip.framecount)
    print('pttrn lngth is', pattern)
    while True:
        link.ping()
        beat = link.beat % pattern
        position = beat / pattern
        frame = clip.framecount * position
        if watcher.nextframe(frame):
            next_frame = clip.play(frame)
            if next_frame & 0xFF == ord('q'):
                break
            elif next_frame & 0xFF == ord('['):
                pattern = pattern * 2
            elif next_frame & 0xFF == ord(']'):
                pattern = pattern / 2
    clip.close()

# Closes all the frames
cv2.destroyAllWindows()
