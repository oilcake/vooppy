import argparse
import time
import json

from player.clip import Clip
from player.window import Window
from files.files import filter_files, filter_with_prefix, best_match, new_index
from Link.client import Client
from Link.sync import Sync, Frame_watcher, Direction


PREFIXES = ['', 'A', 'B', 'C', 'D']


parser = argparse.ArgumentParser(description='arguments')
parser.add_argument("input", help="Input directory", type=str)
args = parser.parse_args()


def json_write(voop_set, data):
    outfile = open(voop_set, 'w')
    json.dump(data, outfile)


folder = args.input
link = Client()
sync = Sync(link.bpm, (4, 4))
watcher = Frame_watcher()
direction = Direction()


window = Window()

prefix = ''
files = list(filter_files(folder, prefix))


index = new_index(files)
file = files[index]

while True:
    clip = Clip(file)
    pattern = int(sync.pattern(clip.duration))
    print(clip)
    print('total frames', clip.framecount)
    print('pttrn lngth is', pattern)
    while True:
        link.ping()
        position = direction.move(link.beat, pattern)
        frame = int(clip.framecount * position)
        if watcher.new_frame_is_not_equal_to(frame):
            next_frame = window.show(clip.play(frame), clip.dim)
            if next_frame & 0xFF == ord('q'):
                index = new_index(files)
                file = files[index]
                break
            elif next_frame & 0xFF == ord('z'):
                closest = best_match(file, folder)
                file = closest
                break
            elif next_frame & 0xFF == ord('['):
                pattern = pattern * 2
            elif next_frame & 0xFF == ord(']'):
                pattern = pattern / 2
            elif next_frame & 0xFF == ord('f'):
                window.fullscreen()
            elif next_frame & 0xFF == ord('g'):
                window.non_fullscreen()
            elif next_frame & 0xFF == ord('<'):
                direction.direction = 0
            elif next_frame & 0xFF == ord('>'):
                direction.direction = 1
            elif next_frame & 0xFF == ord('/'):
                direction.direction = 2
            elif next_frame & 0xFF in range(48, 52):
                prefix_index = next_frame - 48
                prefix = PREFIXES[prefix_index]
                files = list(filter_with_prefix(folder, prefix, file, 0))

        still = 1 / 55
        time.sleep(float(still))
