import cv2


class Resizer:

    aspects = 16, 9
    window_width = 0

    def __init__(self, window_size=(300, 200)):
        self.window_width, self.window_height = window_size
        self.window_shape = [self.window_width, self.window_height]

    def get_resized_dim(self, clip_dimensions: tuple) -> tuple:
        width, height = clip_dimensions
        aspect = width / height
        ratio = self.window_width / width
        width = int(width * ratio)
        height = int(width / aspect)
        return width, height

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
                height, self.aspect_ratio(self.aspects)
            )
            difference = desired_width - width
            top = 0
            left = difference / 2
        if dominant == 1:
            # pad y:
            desired_height = self.get_height_from_width(
                width, self.aspect_ratio(self.aspects)
            )
            difference = desired_height - height
            top = difference / 2
            left = 0

        pads = (top, left)
        return pads

    def resize_and_pad(self, frame: object, dim: tuple) -> object:
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
        # get size of the image fitted into window:
        dim = self.get_resized_dim(new_dim)
        resized = cv2.resize(bordered, dim, interpolation=cv2.INTER_NEAREST)
        return resized

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
