import cv2
import os

path = '/Users/Oilcake/Movies/[VPP]/micro/[A_and_-3d_bright]_A/'
file_01 = 'A01Elsa.mov'
file_02 = 'A10MMBAAHD.mov'
unit = os.path.join(path, file_02)


def play(video):
    # Read until video is completed
    while(video.isOpened()):
        # Capture frame-by-frame
        ret, frame = video.read()
        if ret:
            # Display the resulting frame
            cv2.imshow('Frame', frame)
            cv2.setWindowProperty('Frame', cv2.WND_PROP_TOPMOST, 1)
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        # Press Q on keyboard to  exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # When everything done, release the video capture object
            return cap.release()




# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name


cap = cv2.VideoCapture(unit)
amount_of_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
print(amount_of_frames)

# Check if camera opened successfully
if cap.isOpened():
    while not play(cap) == cap.release():
        play(cap)
else:
    print("Error opening video stream or file")

# Closes all the frames
cv2.destroyAllWindows()
