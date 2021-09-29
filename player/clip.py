import cv2


class Clip():
    framecount = 0

    def __init__(self, clip):
        self.filename = clip
        # open a stream
        self.clip = cv2.VideoCapture(self.filename)
        # get number of frames in video
        self.framecount = int(self.clip.get(cv2.CAP_PROP_FRAME_COUNT))
        if not self.clip.isOpened():
            print("Error opening video stream or file")
        self.find_duration()

    def play(self, frame_):
        if not frame_ > self.framecount:
            self.clip.set(cv2.CAP_PROP_POS_FRAMES, frame_)
            ret, frame = self.clip.read()
            if ret:
                # Display the resulting frame
                cv2.namedWindow('Frame', cv2.WINDOW_FREERATIO)
                # image = cv2.resize(frame, (960, 540))
                # cv2.setWindowProperty('Frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.imshow('Frame', frame)
                cv2.setWindowProperty(
                    'Frame',
                    cv2.WND_PROP_TOPMOST, 1,
                )
                return cv2.waitKey(1)

    def loop(self, rate):
        i = 0
        # Read until video is completed
        while i >= 0 and i <= self.framecount:
            print(i)
            self.clip.set(cv2.CAP_PROP_POS_FRAMES, i)
            # Capture frame-by-frame
            ret, frame = self.clip.read()
            if ret:
                # Display the resulting frame
                cv2.imshow('Frame', frame)
                cv2.setWindowProperty(
                    'Frame',
                    cv2.WND_PROP_TOPMOST, 1,
                )
            else:
                i = 0
                print('ret is false')
            i += 1
            # Press Q on keyboard to  exit
            if cv2.waitKey(int(25 / rate)) & 0xFF == ord('q'):
                break
        self.close()

    def find_duration(self):
        self.fps = int(self.clip.get(cv2.CAP_PROP_FPS))

        # calculate dusration of the video
        seconds = self.framecount / self.fps
        self.duration = seconds
        print("duration in seconds:", self.duration)

    def __repr__(self):
        return(self.filename)

    def close(self):
        # Press Q on keyboard to  exit
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        # When everything done, release the video capture object
        self.clip.release()
        # Closes all the frames
        cv2.destroyAllWindows()

    @staticmethod
    def direction(rate):
        pass
