import argparse

import cv2
from player.clip import Clip
from files.files import filter_files
import random


parser = argparse.ArgumentParser(description='arguments')
parser.add_argument("input", help="Input directory", type=str)
args = parser.parse_args()

folder = args.input


files = list(filter_files(folder))
while True:
    index = random.randint(0, len(files))
    print(index)
    file = files[index]
    clip = Clip(file)
    print(clip)
    print('total frames', clip.framecount)
    clip.loop(2)
    # clip.play(3)


# Create a VideoCapture object and read from input file
# clips = map(cv2.VideoCapture, files)

# for clip in clips:
#     player = Clip(clip)
#     player.play(3)
#     print('3 was played')
#     input()
    # Press Q on keyboard to  exit
    # if cv2.waitKey(1) & 0xFF == ord('q'):


# Closes all the frames
cv2.destroyAllWindows()
