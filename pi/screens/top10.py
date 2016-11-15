import socket
from datetime import datetime
import pygame
from pygame.mixer import Sound

from ui import colours
from ui.widgets.background import LcarsBackgroundImage, LcarsImage
from ui.widgets.gifimage import LcarsGifImage
from ui.widgets.lcars_widgets import *
from ui.widgets.screen import LcarsScreen
from ui.widgets.sprite import LcarsMoveToMouse

# from electricslide import get_leaderboard
import sqlite3

con = sqlite3.connect('electricslide.db', check_same_thread=False)

def get_leaderboard(limit = 10):
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users ORDER BY count desc LIMIT ?", (limit,))
        rows = cur.fetchall()
        pos = 0
        for row in rows:
            pos += 1
            print "{} - id:{} {} ({})".format(pos, row[0], row[1], row[2])
        cur.close()
        return rows

class Top10(LcarsScreen):
    def setup(self, all_sprites):
        all_sprites.add(LcarsBackgroundImage("assets/lcars_screen_1.png"),
                        layer=0)

        # panel text
        all_sprites.add(LcarsText(colours.BLACK, (15, 44), "LCARS 105"),
                        layer=1)
        all_sprites.add(LcarsText(colours.ORANGE, (0, 135), "DynSlide Top 10", 2),
                        layer=1)
        all_sprites.add(LcarsBlockMedium(colours.RED_BROWN, (145, 16), "TOP 10", self.top10_gadget), layer=1)
        all_sprites.add(LcarsBlockSmall(colours.ORANGE, (211, 16), "STATS", self.stats_gadget), layer=1)
        all_sprites.add(LcarsBlockLarge(colours.BEIGE, (249, 16), "LAST SLIDE", self.last_gadget), layer=1)

        # Get ip address of machine
        ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
        all_sprites.add(LcarsText(colours.BLACK, (444, 612), ip), layer=1)

        # Leader Board
        rows = get_leaderboard()
        i = 0
        for row in rows:

            y = 107 + int(i/5) * 180
            x = 130 + i%5 * 130
            text = "#" + str(i+1) + " - " + str(row[2])

            all_sprites.add(LcarsText(colours.WHITE, (y+90 ,x) , text, 1.5))

            # self.dashboard = LcarsImage("65573701.jpg", (y, x))
            img = LcarsImage(str(row[0]) +".jpg", (y, x))
            #print img.image #.__dict__ # img.image.transform.scale(picture, (1280, 720))
            # img_scaled = pygame.transform.scale(img.image, (10,10))
            img.image = pygame.transform.scale(img.image, (120, 90))
            all_sprites.add(img,  layer=2)

            i += 1

        self.info_text = all_sprites.get_sprites_from_layer(3)

        # date display
        self.stardate = LcarsText(colours.BLUE, (12, 380), "STAR DATE 2711.05 17:54:32", 1.5)
        self.lastClockUpdate = 0
        all_sprites.add(self.stardate, layer=1)

        self.top10_gadget = LcarsGifImage("assets/gadgets/lcars_anim2.gif", (235, 150), 100)
        self.top10_gadget.visible = False
        all_sprites.add(self.top10_gadget, layer=2)

        self.stats_gadget = LcarsImage("assets/gadgets/dashboard.png", (187, 232))
        self.stats_gadget.visible = False
        all_sprites.add(self.stats_gadget, layer=2)

        self.last_gadget = LcarsImage("assets/weather.jpg", (188, 122))
        self.last_gadget.visible = False
        all_sprites.add(self.last_gadget, layer=2)

    def update(self, screenSurface, fpsClock):
        if pygame.time.get_ticks() - self.lastClockUpdate > 1000:
            self.stardate.setText("STAR DATE {}".format(datetime.now().strftime("%d%m.%y %H:%M:%S")))
            self.lastClockUpdate = pygame.time.get_ticks()
        LcarsScreen.update(self, screenSurface, fpsClock)

    def updateTop10(self):
        self.top10_gadget.visible = False
        self.stats_gadget.visible = False
        self.last_gadget.visible = False

    def top10_gadget(self, item, event, clock):
        # self.hideInfoText()
        self.top10_gadget.visible = False
        self.stats_gadget.visible = True
        self.last_gadget.visible = False

    def stats_gadget(self, item, event, clock):
        # self.hideInfoText()
        self.top10_gadget.visible = True
        self.stats_gadget.visible = False
        self.last_gadget.visible = False

    def last_gadget(self, item, event, clock):
        # self.hideInfoText()
        self.top10_gadget.visible = False
        self.stats_gadget.visible = False
        self.last_gadget.visible = True
