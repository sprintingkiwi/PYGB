import pygame
import os
import time
import subprocess
from menu import Menu


class Pygb():

    def __init__(self):
        #super(Pygb, self).__init__()
        pygame.init()
        self.width = 800
        self.height = 480
        self.screen = pygame.display.set_mode([self.width, self.height])
        #self.screen = pygame.display.set_mode([self.width, self.height], pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        # Define some colors
        self.white = [255, 255, 255]
        self.red = [255, 0, 0]
        self.blue = [0, 0, 255]
        self.green = [0, 255, 0]
        self.black = [0, 0, 0]
        # Available games list
        self.GAMES_list = os.listdir("/home/pi/PYGB_GAMES/")
        self.GAMES_list.remove(".git")
        self.GAMES_list.remove(".gitignore")
        self.GAMES_list.remove("README.md")
        self.GAMES_list.remove("LICENSE")
        print("Available Games:")
        for game in self.GAMES_list:
            print("*  " + game)
        self.buttonA = False
        self.buttonB = False
        self.buttonSTART = False
        self.buttonESCAPE = False
        self.needupdate = True
        # LOGO
        self.logo = pygame.image.load("/home/pi/PYGB_OS/images/logo.png").convert_alpha()
        self.logo = pygame.transform.scale(self.logo, [self.width, self.height])
        #CONSOLE
        self.console = pygame.image.load("/home/pi/PYGB_OS/images/console.png").convert_alpha()
        self.console = pygame.transform.scale(self.console, [self.width_adapt(800), self.height_adapt(750)])
        # BACKGROUND
        self.background = pygame.image.load("/home/pi/PYGB_OS/images/background.png").convert()
        self.background = pygame.transform.scale(self.background, [self.width, self.height])
        # ACTUAL MENU
        self.actual_menu = Menu(self)
        # CREATE MAIN MENU
        self.mainmenu = Menu(self, fontname="PermanentMarker", size=64, color=self.white, location=[950, 250])
        # CREATE GAMES MENU
        self.gamesmenu = Menu(self, fontname="PermanentMarker", size=48, color=self.white, parent=self.mainmenu)
        # CREATE OPTIONS MENU
        self.optionsmenu = Menu(self, fontname="PermanentMarker", size=48, color=self.blue, parent=self.mainmenu)
        # CREATE CREDITS MENUS
        self.credits_scroll = Menu(self,
                              fontname="PermanentMarker",
                              size=32,
                              color=self.green,
                              selection_color=self.green,
                              selection_zoom=1,
                              parent=self.optionsmenu)
        self.cred_details = Menu(self,
                              fontname="PermanentMarker",
                              size=32,
                              location=[300, 200],
                              color=self.green,
                              selection_color=self.green,
                              selection_zoom=1,
                              parent=self.credits_scroll)
        # Add Games Menu choices
        for game in self.GAMES_list:
            self.gamesmenu.create_choice(self.GAMES_list.index(game),
                                         text=str(game),
                                         effect=self.playgame,
                                         thumb="/home/pi/PYGB_GAMES/" + str(game) + "/thumb.png")
        # Add Options Menu chioces
        self.optionsmenu.create_choice(0, text="Update Games", effect=self.update_games)
        self.optionsmenu.create_choice(1, text="Add Games")
        self.optionsmenu.create_choice(2, text="go to openbox", effect=self.openbox)
        self.optionsmenu.create_choice(3, text="CREDITS", effect=self.change_menu, param=self.credits_scroll)
        # Add Main Menu choices
        self.mainmenu.create_choice(0, text="PLAY", thumb="/home/pi/PYGB_OS/images/play.png", effect=self.change_menu, param=self.gamesmenu)
        self.mainmenu.create_choice(1, text="Options", thumb="/home/pi/PYGB_OS/images/options.png", effect=self.change_menu, param=self.optionsmenu)
        self.mainmenu.create_choice(2, text="QUIT", thumb="/home/pi/PYGB_OS/images/quit.png", effect=self.quit_pygb)
        # Add Credits Menu choices
        for game in self.GAMES_list:
            self.credits_scroll.create_choice(self.GAMES_list.index(game),
                                              text=str(game),
                                              thumb="/home/pi/PYGB_GAMES/" + str(game) + "/credits/thumb.png",
                                              effect=self.show_credits,
                                              param=game)
        # Actual Menu
        self.actual_menu = self.mainmenu
        self.actual_menu.update()

    def width_adapt(self, number):
        return int((number * self.width) / 1280)

    def height_adapt(self, number):
        return int((number * self.height) / 720)

    def size_adapt(self, picture, ratio=1):
        newpic = pygame.transform.scale(picture, [int(self.width * ratio), int(self.height * ratio)])
        return newpic

    def welcome_screen(self):
        done = False
        while not done:
            self.screen.blit(self.logo, [0, 0])
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        done = True

    def change_menu(self, newmenu):
        global actual_menu
        self.actual_menu = newmenu

    def playgame(self, *args):
        newdir = "/home/pi/PYGB_GAMES/" + str(self.GAMES_list[self.actual_menu.actual_choice])
        print(newdir)
        subprocess.Popen(["python", "main.py"], cwd=newdir)
        pygame.quit()
        quit()

    def update_games(self, *args):
        subprocess.call(["git", "checkout", "."], cwd="/home/pi/PYGB_GAMES/")
        subprocess.Popen(["git", "pull"], cwd="/home/pi/PYGB_GAMES/")

    def openbox(self, *args):
        pygame.quit()
        quit()

    def show_credits(self, game, *args):
        self.cred_details.empty()
        self.cred_details.actual_choice = 0
        creds = open("/home/pi/PYGB_GAMES/" + game + "/credits/credits.txt")
        lines = creds.readlines()
        for line in lines:
            self.cred_details.create_choice(lines.index(line), text=line)
        self.actual_menu = self.cred_details

    def quit_pygb(self, *args):
        os.system("sudo poweroff")

    def events_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.openbox()
            if event.type == pygame.KEYDOWN:
                self.needupdate = True
                if event.key == pygame.K_ESCAPE:
                    self.buttonESCAPE = True
                    self.openbox()
                if event.key == pygame.K_RETURN:
                    self.buttonSTART = True
                    print("Button START pressed")
                if event.key == pygame.K_DOWN:
                    menuentries = len(self.actual_menu.sprites())
                    if menuentries > 1:
                        if self.actual_menu.actual_choice < menuentries - 1:
                            self.actual_menu.actual_choice += 1
                        else:
                            self.actual_menu.actual_choice = 0
                        self.actual_menu.update()
                if event.key == pygame.K_UP:
                    menuentries = len(self.actual_menu.sprites())
                    if menuentries > 1:
                        if self.actual_menu.actual_choice > 0:
                            self.actual_menu.actual_choice -= 1
                        else:
                            self.actual_menu.actual_choice = menuentries - 1
                        self.actual_menu.update()
                if event.key == pygame.K_z:
                    print("Button B pressed")
                    self.buttonB = True
                if event.key == pygame.K_x:
                    print("Button A pressed")
                    self.buttonA = True

    def choice_effects(self):
        if self.buttonA:
            print self.actual_menu.sprites()
            c = self.actual_menu.sprites()[self.actual_menu.actual_choice]
            if c.effect is not None:
                c.execute(c.effect, c.param)
            self.actual_menu.update()
        if self.buttonB:
            if self.actual_menu.parent is not None:
                self.actual_menu = self.actual_menu.parent
                self.actual_menu.update()

    def draw_images(self):
        #self.screen.fill(self.black)
        self.screen.blit(self.background, [0, 0])
        self.screen.blit(self.console, [self.width_adapt(10), self.height_adapt(10)])
        if self.actual_menu.actual_thumb is not None:
            self.screen.blit(self.actual_menu.actual_thumb, [self.width_adapt(150), self.height_adapt(250)])
        self.actual_menu.draw(self.screen)

    def mainloop(self):
        self.welcome_screen()

        while True:

            self.events_check()

            if self.needupdate:
                self.choice_effects()
                self.draw_images()
                # UPDATE SCREEN
                pygame.display.update()

            # wait time between frames
            self.clock.tick(30)

            # deactivate button pression
            self.buttonA = False
            self.buttonB = False
            self.buttonSTART = False
            self.buttonESCAPE = False
            self.needupdate = False


PYGB = Pygb()
PYGB.mainloop()
