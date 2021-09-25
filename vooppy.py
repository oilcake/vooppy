import cv2
import os
import click

SUPPORTED = ['.mp4', '.mpg', '.mov', '.avi', '.wmv', '.mkv']


@click.command()
@click.argument('input')
def filter_files(input):
    path = os.path.abspath(input)
    for root, dirs, files in os.walk(path):
        for file in files:
            if is_supported(file):
                yield(os.path.join(root, file))


def is_supported(file):
    filename, file_extension = os.path.splitext(file)
    print(file_extension)
    # return file_extension in SUPPORTED
    return True


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


folder = filter_files()

# Create a VideoCapture object and read from input file
caps = map(cv2.VideoCapture, folder)

for cap in caps:
    if cap.isOpened():
        while not play(cap) == cap.release():
            play(cap)
    else:
        print("Error opening video stream or file")

# Closes all the frames
cv2.destroyAllWindows()
