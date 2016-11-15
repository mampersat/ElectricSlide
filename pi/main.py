import argparse
import pigpio
import sqlite3
import sys
import time
import reader
from PIL import Image
from electricslide import ElectricSlide
from screens.top10 import Top10
from ui.ui import UserInterface

# global config
UI_PLACEMENT_MODE = True
RESOLUTION = (800, 480)
FPS = 60
DEV_MODE = True

top10Screen = Top10()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", help="Initialize database", action="store_true")
    args = parser.parse_args()

    slide = ElectricSlide()
    if args.init:
        slide.initialize_db()

    pi = pigpio.pi()

    ui = UserInterface(top10Screen, RESOLUTION, UI_PLACEMENT_MODE, FPS, DEV_MODE)

    def callback(bits, value):
        print("bits={} value={}".format(bits, value))
        slide.ride(value)
        slide.get_leaderboard(limit=10)
        top10Screen.updateTop10()

    w = reader.decoder(pi, 14, 15, callback)
    top10Screen.updateTop10()

    try:
        while (True):
            ui.tick()
    finally:
        w.cancel()
        pi.stop()
