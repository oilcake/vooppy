import argparse
import time
import random

from player.clip import Clip
from player.mpv import Mpv

from player.window import Window

from files.files import filter_files, filter_with_prefix, best_match
from Link.client import Client
from Link.sync import Sync, FrameWatcher, Direction, Change


PREFIXES = ["", "A", "B", "C", "D"]


parser = argparse.ArgumentParser(description="arguments")
parser.add_argument("input", help="Input directory", type=str)
args = parser.parse_args()


folder = args.input
link = Client()
sync = Sync(link.bpm, (4, 4))
watcher = FrameWatcher()
direction = Direction()


window = Window()

prefix = "A"
files = list(filter_files(folder, prefix))

mpv = Mpv()


file = random.choice(files)

detector = Change()

while True:
    clip = Clip(file)
    """
    pattern is a number of bars that represents video length
    rounded to current music duration
    """
    print(clip)
    pattern = int(sync.pattern(clip.duration))
    print(f"clip's duration is {clip.duration} seconds")
    print(f"total number of frames, is {clip.framecount}")
    print(f"pttrn lngth is {pattern}")
    print("image size", clip.dim)
    while True:
        link.ping()
        """
        playing position is calculated from link sync info
        multiplied by pattern
        """
        position = direction.move(link.beat, pattern)
        frame = int(clip.framecount * position)
        # check that frame is unique to limit calculations:
        if watcher.new_frame_is_not_equal_to(frame):
            next_frame = window.show(clip.play(frame), clip.dim)
            # next_frame = window.show(clip.play(frame))
            if next_frame is not None:
                if next_frame & 0xFF == ord("r"):  # reset
                    direction.off_set()
                elif next_frame & 0xFF == ord("t"):  # jump
                    direction.jump()
                elif next_frame & 0xFF == ord("q"):
                    file = random.choice(files)
                    break
                elif next_frame & 0xFF == ord("z"):
                    closest = best_match(file, folder)
                    file = closest
                    break
                elif next_frame & 0xFF == ord("["):
                    pattern = pattern * 2
                elif next_frame & 0xFF == ord("]"):
                    pattern = pattern / 2
                elif next_frame & 0xFF == ord("-"):
                    pattern = pattern * 1.5
                elif next_frame & 0xFF == ord("="):
                    pattern = pattern / 1.5
                elif next_frame & 0xFF == ord("f"):
                    window.fullscreen()
                elif next_frame & 0xFF == ord("g"):
                    window.non_fullscreen()
                elif next_frame & 0xFF == ord("<"):
                    direction.direction = 0
                elif next_frame & 0xFF == ord(">"):
                    direction.direction = 1
                elif next_frame & 0xFF == ord("/"):
                    direction.direction = 2
                elif next_frame & 0xFF in range(48, 52):
                    prefix_index = next_frame - 48
                    prefix = PREFIXES[prefix_index]
                    files = list(filter_with_prefix(folder, prefix, file, 0))

        still = float(1 / 25)
        time.sleep(still)
