import argparse
import random
import time

from player.clip import Clip
from player.window import Window
from files.files import filter_files
from Link.client import Client
from Link.sync import Sync, Frame_watcher

PREFIXES = ['', 'A', 'B', 'C', 'D']

parser = argparse.ArgumentParser(description='arguments')
parser.add_argument("input", help="Input directory", type=str)
args = parser.parse_args()

folder = args.input

link = Client()
sync = Sync(link.bpm, (4, 4))
watcher = Frame_watcher()

prefix = ''

files = list(filter_files(folder, prefix))

window = Window()
while True:
    index = random.randint(0, len(files) - 1)
    file = files[index]
    clip = Clip(file)
    pattern = int(sync.pattern(clip.duration))
    print(clip)
    print('total frames', clip.framecount)
    print('pttrn lngth is', pattern)
    while True:
        link.ping()
        beat = link.beat % pattern
        position = beat / pattern
        frame = int(clip.framecount * position)
        if watcher.new_frame_is_not_equal_to(frame):
            next_frame = window.show(clip.play(frame), clip.dim)
            if next_frame & 0xFF == ord('q'):
                break
            elif next_frame & 0xFF == ord('['):
                pattern = pattern * 2
            elif next_frame & 0xFF == ord(']'):
                pattern = pattern / 2
            elif next_frame & 0xFF == ord('f'):
                window.fullscreen()
            elif next_frame & 0xFF == ord('g'):
                window.non_fullscreen()
            elif next_frame & 0xFF in range(48, 52):
                number = next_frame - 48
                prefix = PREFIXES[number]
                files = list(filter_files(folder, prefix))
                break

        still = 1 / 60
        time.sleep(float(still))
    clip.close()
