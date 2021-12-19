import cv2


class Window:

    floating = 0
    window_name = "Frame"
    window_width = 500
    corner_x = 0
    corner_y = 0
    aspects = 16, 9

    def __init__(self):
        self.window_height = self.get_height_from_width(
            self.window_width,
            self.aspect_ratio(self.aspects)
        )
        self.window_shape = [self.window_width, self.window_height]
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.moveWindow(self.window_name, self.corner_x, self.corner_y)
        cv2.resizeWindow(
            self.window_name,
            self.window_width,
            self.window_height
        )
        # always on top:
        # cv2.setWindowProperty(self.window_name, cv2.WND_PROP_TOPMOST, 0)

    def rebuild(self, new_dims):
        self.window_height = self.get_height_from_width(
            self.window_width,
            new_dims[0] / new_dims[1]
        )
        cv2.moveWindow(self.window_name, self.corner_x, self.corner_y)
        cv2.resizeWindow(
            self.window_name,
            self.window_width,
            self.window_height
        )

    def get_resized_dim(self, clip_dimensions: tuple) -> tuple:
        width, height = clip_dimensions
        aspect = width / height
        ratio = self.window_width / width
        width = int(width * ratio)
        height = int(width / aspect)
        return width, height

    def resize(self, frame, clip_dim: tuple):
        # resize image to window:
        cv2.moveWindow(self.window_name, int(self.corner_x), int(self.corner_y))
        resized = cv2.resize(frame, clip_dim, interpolation=cv2.INTER_AREA)
        return resized

    def center(self, img, dim: tuple):
        width, height = dim
        aspect = width / height
        # define the axis that should be padded (0-x, 1-y):
        dominant = int(self.aspect_ratio(self.aspects) < aspect)
        pads = self.pad(dominant, width, height)
        return pads

    def pad(self, dominant: int, width: int, height: int) -> tuple:
        if dominant == 0:
            # pad x:
            desired_width = self.get_width_from_height(
                    height,
                    self.aspect_ratio(self.aspects)
                )
            difference = desired_width - width
            top = 0
            left = difference / 2
        if dominant == 1:
            # pad y:
            desired_height = self.get_height_from_width(width, self.aspect_ratio(self.aspects))
            difference = desired_height - height
            top = difference / 2
            left = 0

        pads = (top, left)
        return pads

    def show(self, frame: object, dim: tuple) -> object:
        # make correct borders:
        pads = self.center(frame, dim)
        top = int(pads[0])
        bottom = top
        left = int(pads[1])
        right = left
        bordered = cv2.copyMakeBorder(frame, top, bottom, left, right, 0)
        x_delta = left * 2
        y_delta = top * 2
        new_dim = (dim[0] + x_delta, dim[1] + y_delta)

        # get size of the image fitted into window
        dim = self.get_resized_dim(new_dim)
        resized = self.resize(bordered, dim)
        # Display the resized frame
        cv2.imshow(self.window_name, resized)
        return cv2.waitKey(1)

    def fullscreen(self) -> None:
        self.window_width = 1440
        new_dims = 1440, 900
        self.aspects = new_dims
        self.rebuild(new_dims)
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        """Set display window to full screen."""
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, 1)

    def non_fullscreen(self) -> None:
        self.window_width = 600
        new_dims = 600, 336
        self.aspects = new_dims
        self.rebuild(new_dims)
        """Set display window to normal."""
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, 0)

    @staticmethod
    def get_height_from_width(width: int, aspect_ratio: float) -> int:
        return int(width / aspect_ratio)

    @staticmethod
    def get_width_from_height(height: int, aspect_ratio: float) -> int:
        return int(height * aspect_ratio)

    @staticmethod
    def aspect_ratio(aspects: tuple) -> float:
        x, y = aspects
        return x / y
