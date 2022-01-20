import cv2


from player.resizer import Resizer


resizer = Resizer()


class Window:

    floating = 1
    visible = True
    is_fullscreen = False
    window_name = "Frame"
    window_width = 640
    corner_x = 0
    corner_y = 0
    aspects = 16, 9

    def __init__(self):
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.moveWindow(self.window_name, self.corner_x, self.corner_y)
        # always on top:
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_TOPMOST, self.floating)

    def show(self, frame: object, dim: tuple) -> object:
        resized = resizer.resize_and_pad(frame, dim)
        # Display the resized frame
        cv2.imshow(self.window_name, resized)
        # gui.show(resized)
        return cv2.waitKey(1)

    def fullscreen(self) -> None:
        self.is_fullscreen = not self.is_fullscreen
        print("fullscr", float(self.is_fullscreen))
        # print("visible", float(not self.is_fullscreen))

        cv2.setWindowProperty(
            self.window_name, cv2.WND_PROP_FULLSCREEN, float(self.is_fullscreen)
        )

        if self.is_fullscreen:
            resizer.window_width = 1440
            cv2.resizeWindow(self.window_name, 1440, 900)
        else:
            resizer.window_width = 300
            cv2.resizeWindow(self.window_name, 300, 200)
        # cv2.namedWindow(self.window_name, cv2.WINDOW_AUTOSIZE)
        # cv2.setWindowProperty(
        #     self.window_name, cv2.WND_PROP_VISIBLE, float(not self.is_fullscreen)
        # )

        # cv2.destroyWindow(self.window_name)
        # self.window_name += "_fullscreen"
        # cv2.namedWindow(self.window_name, cv2.WINDOW_GUI_EXPANDED)
        # """Set display window to full screen."""
        # cv2.setWindowProperty(self.window_name, cv2.WND_PROP_TOPMOST, 0)

    def non_fullscreen(self) -> None:
        self.visible = not self.visible
        # cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, 0)
        cv2.setWindowProperty(
            self.window_name, cv2.WND_PROP_VISIBLE, float(self.visible)
        )
        # cv2.destroyWindow(self.window_name)
        # self.window_name = "Frame"
        # cv2.namedWindow(self.window_name)
        # cv2.setWindowProperty(self.window_name, cv2.WND_PROP_TOPMOST, self.floating)

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
        x, y = aspects
        return x / y
        x, y = aspects
        return x / y
        return x / y
        x, y = aspects
        return x / y
