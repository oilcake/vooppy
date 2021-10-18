import cv2


class Window:
    window_name = 'Frame'
    window_width = 700
    window_height = (window_width / 16) * 9
    corner_x = 0
    corner_y = 0

    def __init__(self):
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.moveWindow(self.window_name,
                       int(self.corner_x),
                       int(self.corner_y))
        cv2.setWindowProperty(
            self.window_name,
            cv2.WND_PROP_TOPMOST, 0)

    def resize(self, frame, dim):
        width, height = dim
        aspect = width / height
        ratio = self.window_width / width
        width = int(width * ratio)
        height = int(width / aspect)
        clip_dim = width, height
        cv2.moveWindow(self.window_name,
                       int(self.corner_x),
                       int(self.corner_y))
        resize = cv2.resize(frame, clip_dim, interpolation=cv2.INTER_AREA)
        return resize

    def show(self, frame, dim: tuple):
        # Display the resulting frame
        cv2.imshow(self.window_name, self.resize(frame, dim))
        return cv2.waitKey(1)

    def fullscreen(self):
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(
            self.window_name,
            cv2.WND_PROP_TOPMOST, 0)

        """Set disply window to either full screen or normal."""
        cv2.setWindowProperty(self.window_name,
                              cv2.WND_PROP_FULLSCREEN,
                              1)

    def non_fullscreen(self):
        cv2.setWindowProperty(
            self.window_name,
            cv2.WND_PROP_TOPMOST, 0)
        cv2.setWindowProperty(
            self.window_name,
            cv2.WND_PROP_TOPMOST, 0)

        """Set disply window to either full screen or normal."""
        cv2.setWindowProperty(self.window_name,
                              cv2.WND_PROP_FULLSCREEN,
                              0)
