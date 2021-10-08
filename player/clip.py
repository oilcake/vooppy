import cv2


class Clip():
    framecount = None
    dim = (0, 0)

    def __init__(self, clip):
        self.filename = clip
        # open a stream
        self.clip = cv2.VideoCapture(self.filename)
        if not self.clip.isOpened():
            print("Error opening video stream or file")
        # get number of frames in video
        self.framecount = int(self.clip.get(cv2.CAP_PROP_FRAME_COUNT))
        self.find_duration()
        self.get_dimensions()

    def get_dimensions(self):
        width = self.clip.get(3)  # float `width`
        height = self.clip.get(4)  # float `height`
        self.dim = (width, height)

    def play(self, frame_):
        if not frame_ > self.framecount:
            self.clip.set(cv2.CAP_PROP_POS_FRAMES, frame_)
            ret, frame = self.clip.read()
            if ret:
                return frame

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
                cv2.imshow(self.window_name, frame)
                cv2.setWindowProperty(
                    self.window_name,
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
        self.duration = seconds * 4

    def __repr__(self):
        return(self.filename)

    def close(self):
        self.clip.release()
        # Closes all the frames
        cv2.destroyAllWindows()

    @staticmethod
    def direction(rate):
        pass
