import subprocess


class Mpv:
    voop_mpv = "/Users/Oilcake/Documents/Dev/vooppy/vooplaylist.mpv"
    loop_what = "file"
    argloop = "--loop=" + loop_what
    player = None

    def __init__(self):
        self.loop_what = "file"
        self.argloop = "--loop=" + self.loop_what

    def stop(self):
        self.player.terminate()

    def start(self):
        playlist = self.voop_mpv
        arg = "--playlist=" + playlist
        self.player = subprocess.Popen(
            [
                "mpv",
                arg,
                "--shuffle",
                "--ontop",
                "--loop-file",
                "--loop-playlist",
                "-fullscreen",
                "--fs-screen=1",
            ]
        )
