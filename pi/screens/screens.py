import sys
from ui.ui import UserInterface
from datetime import datetime
import pygame
import socket

from ui import colours
from ui.widgets.background import LcarsBackgroundImage, LcarsImage
from ui.widgets.gifimage import LcarsGifImage
from ui.widgets.lcars_widgets import *
from ui.widgets.screen import LcarsScreen
from ui.widgets.sprite import LcarsMoveToMouse


class ScreenMain(LcarsScreen):
    def setup(self, all_sprites):
        all_sprites.add(LcarsBackgroundImage("assets/lcars_screen_1.png"), layer=0)
        
        # panel text
        all_sprites.add(LcarsText(colours.BLACK, (15, 44), "DYN"), layer=1)
        all_sprites.add(LcarsText(colours.ORANGE, (0, 135), "ELECTRIC SLIDE", 2), layer=1)

        all_sprites.add(LcarsBlockMedium(colours.RED_BROWN, (145, 16), "TOP 10"), layer=1)
        all_sprites.add(LcarsBlockSmall(colours.ORANGE, (211, 16), "PICTURE"), layer=1)
        all_sprites.add(LcarsBlockLarge(colours.BEIGE, (249, 16), "ENERGY"), layer=1)

        # Get ip address of machine
        ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
        all_sprites.add(LcarsText(colours.BLACK, (444, 612), ip), layer=1)

        # info text
        all_sprites.add(LcarsText(colours.WHITE, (192, 174), "TOP 10", 1.5), layer=3)
        all_sprites.add(LcarsText(colours.BLUE, (222, 174), "one", 1.5), layer=3)
        all_sprites.add(LcarsText(colours.BLUE, (252, 174), "two", 1.5), layer=3)
        all_sprites.add(LcarsText(colours.BLUE, (282, 174), "three", 1.5), layer=3)
        all_sprites.add(LcarsText(colours.BLUE, (312, 174), "four", 1.5), layer=3)
        all_sprites.add(LcarsText(colours.BLUE, (342, 174), "five", 1.5), layer=3)
        self.info_text = all_sprites.get_sprites_from_layer(3)

        # date display (get's set to date in update())
        self.stardate = LcarsText(colours.BLUE, (12, 380), "STAR DATE 2711.05 17:54:32", 1.5)
        self.lastClockUpdate = 0
        all_sprites.add(self.stardate, layer=1)

        # buttons        
        all_sprites.add(LcarsButton(colours.RED_BROWN, (6, 662), "LOGOUT", self.logoutHandler), layer=4)
        all_sprites.add(LcarsButton(colours.BEIGE, (107, 127), "TOP 10", self.sensorsHandler), layer=4)
        all_sprites.add(LcarsButton(colours.PURPLE, (107, 262), "LAST", self.gaugesHandler), layer=4)
        # all_sprites.add(LcarsButton(colours.PEACH, (107, 398), "WEATHER", self.weatherHandler), layer=4)

        # gadgets        
        # all_sprites.add(LcarsGifImage("assets/gadgets/fwscan.gif", (277, 556), 100), layer=1)
        
        self.sensor_gadget = LcarsGifImage("assets/gadgets/lcars_anim2.gif", (235, 150), 100) 
        self.sensor_gadget.visible = False
        all_sprites.add(self.sensor_gadget, layer=2)

        self.dashboard = LcarsImage("assets/gadgets/dashboard.png", (187, 232))
        self.dashboard.visible = False
        all_sprites.add(self.dashboard, layer=2) 

        #all_sprites.add(LcarsMoveToMouse(colours.WHITE), layer=1)

    def update(self, screenSurface, fpsClock):
        if pygame.time.get_ticks() - self.lastClockUpdate > 1000:
            self.stardate.setText("STAR DATE {}".format(datetime.now().strftime("%d%m.%y %H:%M:%S")))
            self.lastClockUpdate = pygame.time.get_ticks()
        LcarsScreen.update(self, screenSurface, fpsClock)
        
    def handleEvents(self, event, fpsClock):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return False

        if event.type == pygame.MOUSEBUTTONUP:
            return False

    def hideInfoText(self):
        if self.info_text[0].visible:
            for sprite in self.info_text:
                sprite.visible = False

    def updateInfoText(self):
        for sprite in self.info_text:
            sprite.setText("Test")
            
    def gaugesHandler(self, item, event, clock):
        self.hideInfoText()
        self.sensor_gadget.visible = False
        self.dashboard.visible = True

    def sensorsHandler(self, item, event, clock):
        #self.hideInfoText()
        self.sensor_gadget.visible = False
        self.dashboard.visible = False
        self.updateInfoText()
        for sprite in self.info_text:
            sprite.visible = True
    
    def logoutHandler(self, item, event, clock):
        sys.exit(0)
    

