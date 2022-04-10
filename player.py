from googlecontroller import GoogleAssistant
import time
import os


class Player:
    def __init__(self, host, azaan_directory):
        self.host = host
        self.azaan_directory = azaan_directory

    def play(self, fajr):
        home = GoogleAssistant(self.host)
        home.say("Azaan")
        home.volume(30)
        f_name = "azaan_normal.mp3" if not fajr else "azaan_fajr.mp3"
        home.serve_media(f_name, self.azaan_directory, 0)


if __name__ == '__main__':
    p = Player("192.168.1.152", "{}/azaans".format(os.getcwd()))
    # time.sleep(10)
    p.play(True)
    time.sleep(7)
    p.play(True)
