import argparse

import cv2
import os

SUPPORTED = ['.mp4', '.mpg', '.mov', '.avi', '.wmv', '.mkv']

parser = argparse.ArgumentParser(description='arguments')
parser.add_argument("input", help="Input directory", type=str)
args = parser.parse_args()

folder = args.input


def filter_files(path_to_files):
    path = os.path.abspath(path_to_files)
    for root, dirs, files in os.walk(path):
        for file in files:
            if supported(file):
                yield(os.path.join(root, file))


def supported(file):
    filename, file_extension = os.path.splitext(file)
    return file_extension in SUPPORTED


def play(cap):
    # get number of frames in video
    frames_total = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print(frames_total)
    # Read until video is completed
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            # Display the resulting frame
            cv2.namedWindow('Frame', cv2.WINDOW_FREERATIO)
            cv2.imshow('Frame', frame)
            cv2.setWindowProperty(
                'Frame',
                cv2.WND_PROP_TOPMOST, 1,
            )
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        # Press Q on keyboard to  exit
        if cv2.waitKey(46) & 0xFF == ord('q'):
            # When everything done, release the video capture object
            return cap.release()


files = filter_files(folder)


# Create a VideoCapture object and read from input file
caps = map(cv2.VideoCapture, files)

for cap in caps:
    if cap.isOpened():
        while not play(cap) == cap.release():
            play(cap)
    else:
        print("Error opening video stream or file")

# Closes all the frames
cv2.destroyAllWindows()
