import subprocess
import argparse
import time
import random

from player.clip import Clip
from player.window import Window
from files.files import filter_files, filter_with_prefix, best_match, add_to_set
from Link.client import Client
from Link.sync import Sync, FrameWatcher, Direction, Change


class Mpv:
    voop_mpv = '/Users/Oilcake/Documents/Dev/vooppy/vooplaylist.mpv'
    loop_what = "file"
    argloop = "--loop=" + loop_what
    player = None

    def __init__(self):
        self.loop_what = "file"
        self.argloop = "--loop=" + self.loop_what

    def stop(self):
        self.player.terminate()

    def start(self):
        playlist = self.voop_mpv
        arg = "--playlist=" + playlist
        self.player = subprocess.Popen(
            [
                "mpv",
                arg,
                "--shuffle",
                # "--ontop",
                # "--loop-file",
                "--loop-playlist",
                "-fullscreen",
                "--fs-screen=1",
                ]
            )


PREFIXES = ["", "A", "B", "C", "D"]


parser = argparse.ArgumentParser(description="arguments")
parser.add_argument("input", help="Input directory", type=str)
args = parser.parse_args()


def add_to_playlist(file):
    playlist = '/Users/Oilcake/Documents/Dev/vooppy/vooplaylist.mpv'
    with open(playlist, 'a') as vpllst:
        print(file, file=vpllst)


def default_playlist_to(file):
    playlist = '/Users/Oilcake/Documents/Dev/vooppy/vooplaylist.mpv'
    with open(playlist, 'w') as vpllst:
        print(file, file=vpllst)


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
# try:
#     mpv.start()
# except Exception:
#     default_playlist_to(file)
#     mpv.start()

detector = Change()

while True:
    clip = Clip(file)
    '''
    pattern is a number of bars that represents video length
    rounded to current music duration
    '''
    print(clip)
    pattern = int(sync.pattern(clip.duration))
    print(f"clip's duration is {clip.duration} seconds")
    print(f"total number of frames, is {clip.framecount}")
    print(f"pttrn lngth is {pattern}")
    print("image size", clip.dim)
    # audio part
    # if clip.audio.soundfile is not None:
    #     print(f"sound {clip.audio.soundfile}")
    # else:
    #     print("no audio")
    # new_lngth_of_clip = sync.one_bar_ms * pattern
    # clip.audio.ratio = float(clip.duration / new_lngth_of_clip)
    # print(f"new length in seconds? is {new_lngth_of_clip}")
    # print(f"desired sound ratio is {clip.audio.ratio}")
    while True:
        link.ping()
        '''
        playing position is calculated from link sync info
        multiplied by pattern
        '''
        position = direction.move(link.beat, pattern)
        frame = int(clip.framecount * position)
        # check that frame is unique to limit calculations:
        if watcher.new_frame_is_not_equal_to(frame):
            next_frame = window.show(clip.play(frame), clip.dim)
            # if detector.detected_beat_change(link.beat):
            #     index = int(clip.audio.length * position)
            #     clip.audio.play(index=index)
            # if detector.detected_bar_change(link.beat):
            #     print('WORKED WITH BAR')
            if next_frame & 0xFF == ord("r"):  # reset
                direction.off_set()
            elif next_frame & 0xFF == ord("t"):   # jump
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
            elif next_frame & 0xFF == ord("x"):
                # mpv.stop()
                add_to_playlist(file)
                add_to_set(file)
                # mpv.start()
            elif next_frame & 0xFF == ord("c"):
                default_playlist_to(file)
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

        still = float(1 / 55)
        time.sleep(still)
