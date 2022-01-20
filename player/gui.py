#!/usr/bin/env python
import PySimpleGUI as sg

# from PIL import Image
import cv2 as cv


DISPLAY_SIZE = sg.Window.get_screen_size()


class Gui:
    sg.theme("Black")
    layout = [
        [sg.Image(filename="", key="-image-")],
    ]

    # create the window and show it without the plot
    window = sg.Window(
        "voop",
        layout,
        no_titlebar=True,
        location=(0, 0),
        size=(640, 486),
        keep_on_top=True,
        return_keyboard_events=True,
        use_default_focus=False,
        # grab_anywhere=True,
    )

    # locate the elements we'll be updating. Does the search only 1 time
    image_elem = window["-image-"]

    # make window fullscreen
    window.Finalize()

    window.Maximize()

    def show(self, frame):
        event, values = self.window.read(timeout=0)

        imgbytes = cv.imencode(".png", frame)[1].tobytes()  # ditto
        self.image_elem.update(data=imgbytes)

        if event is not sg.TIMEOUT_KEY:
            if len(event) == 1:
                print("%s - %s" % (event, ord(event)))
            else:
                print(event)
