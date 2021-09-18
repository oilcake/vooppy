import cv2
import os

path = '/Users/Oilcake/Movies/[VPP]/micro/[A_and_-3d_bright]_A/'
file_01 = 'A01Elsa.mov'
file_02 = 'A10MMBAAHD.mov'
unit = os.path.join(path, file_02)

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
while True:
    cap = cv2.VideoCapture(unit)

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error opening video stream or file")
    # Read until video is completed
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            # Display the resulting frame
            cv2.imshow('Frame', frame)
            cv2.setWindowProperty('Frame', cv2.WND_PROP_TOPMOST, 1)

            # Press Q on keyboard to  exit
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break

    # When everything done, release the video capture object
    cap.release()

# Closes all the frames
cv2.destroyAllWindows()
