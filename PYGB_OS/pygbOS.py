import pygame
import time
import os
import subprocess

# INIT
pygame.init()
width = 800
height = 480
screen = pygame.display.set_mode([width, height])
#screen = pygame.display.set_mode([width, height], pygame.FULLSCREEN)

clock = pygame.time.Clock()

# Define some colors
white = [255, 255, 255]
red = [255, 0, 0]
blue = [0, 0, 255]
green = [0, 255, 0]
black = [0, 0, 0]

GAMES_list = os.listdir("/home/pi/PYGB_GAMES/")
GAMES_list.remove(".git")
GAMES_list.remove("README.md")
GAMES_list.remove("CREDITS.txt")
GAMES_list.remove("LICENSE")
print("Available Games:")
for game in GAMES_list:
    print("*  " + game)


def width_adapt(number):
    global width
    return (number * width) / 1280


def height_adapt(number):
    global height
    return (number * height) / 720


# Class for menu choices
class Choice(pygame.sprite.Sprite):

    def __init__(self,
                 ID,
                 fontname,
                 size,
                 bold,
                 italic,
                 text,
                 color,
                 thumb,
                 effect,
                 param):
        super(Choice, self).__init__()
        self.ID = ID
        self.fontname = fontname
        self.size = size
        self.bold = bold
        self.italic = italic
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont(self.fontname, self.size, self.bold, self.italic)
        self.image = self.font.render(self.text, False, self.color)
        self.place = self.ID
        self.rect = self.image.get_rect()
        self.rect.x = width_adapt(800)
        self.rect.y = height_adapt(250) + ((2 * self.size) + (0.3 * self.size)) * self.place
        #if self.rect.y > height:
            #self.rect.y = 50
        try:
            self.thumb = pygame.image.load(thumb)
            h = height_adapt(500)
            #rect = self.thumb.get_rect()
            #w = (rect.width * h) / rect.height
            self.thumb = pygame.transform.scale(self.thumb, [h, h])
        except:
            self.thumb = None
        self.effect = effect
        self.param = param

    def execute(self, effect, *args):
        effect(*args)

    def update(self):
        self.font = pygame.font.SysFont(self.fontname, self.size, self.bold, self.italic)
        self.image = self.font.render(self.text, False, self.color)


# class for menus
class Menu(pygame.sprite.OrderedUpdates):

    def __init__(self,
                 fontname="Liberation Serif",
                 size=32,
                 bold=True,
                 italic=False,
                 color=white,
                 selection_color=red,
                 selection_zoom=0.125,
                 parent = None,
                 *args):
        super(Menu, self).__init__()
        self.fontname = fontname
        self.size = (size * height) / 720
        self.bold = bold
        self.italic = italic
        self.color = color
        # Actual Choice ID
        self.actual_choice = 0
        self.actual_thumb = None
        self.selection_color = selection_color
        self.selection_zoom = selection_zoom
        self.parent = parent

    def create_choice(self, ID, text, thumb="", effect=None, param=None):
        self.add(Choice(ID,
                        self.fontname,
                        self.size,
                        self.bold,
                        self.italic,
                        text,
                        self.color,
                        thumb,
                        effect,
                        param))

    def update(self):
        for choice in self.sprites():
            if choice.ID == self.actual_choice:
                choice.size = int(self.size + self.size * self.selection_zoom)
                choice.color = self.selection_color
                choice.update()
            else:
                choice.size = self.size
                choice.color = self.color
                choice.update()
        print(str(self.actual_choice) + " - " + self.sprites()[self.actual_choice].text)
        self.actual_thumb = self.sprites()[self.actual_choice].thumb
        super(Menu, self).update()


actual_menu = Menu()


def change_menu(newmenu):
    global actual_menu
    actual_menu = newmenu


def playgame(*args):
    newdir = "/home/pi/PYGB_GAMES/" + str(GAMES_list[actual_menu.actual_choice])
    print(newdir)
    subprocess.Popen(["python", "main.py"], cwd=newdir)
    pygame.quit()
    quit()


def update_games(*args):
    subprocess.Popen(["git", "pull"], cwd="/home/pi/PYGB_GAMES/")


def show_credits(*args):
    global actual_menu, buttonB
    credits_scroll = Menu(fontname="MV Boli",
                          size=32,
                          color=green,
                          selection_color=green,
                          selection_zoom=1,
                          parent=optionsmenu)
    cred = open("/home/pi/PYGB_GAMES/CREDITS.txt")
    lines = cred.readlines()
    for line in lines:
        credits_scroll.create_choice(lines.index(line), text=line)
    actual_menu = credits_scroll


def openbox(*args):
    pygame.quit()
    quit()


def quit_pygb(*args):
    os.system("sudo poweroff")


# CREATE MAIN MENU
mainmenu = Menu(fontname="MV Boli", size=64, color=white)
# CREATE GAMES MENU
gamesmenu = Menu(fontname="MV Boli", size=48, color=white, parent=mainmenu)
# CREATE OPTIONS MENU
optionsmenu = Menu(fontname="MV Boli", size=48, color=blue, parent=mainmenu)

# Add Games Menu choices
for game in GAMES_list:
    gamesmenu.create_choice(GAMES_list.index(game),
                            text=str(game),
                            effect=playgame,
                            thumb="/home/pi/PYGB_GAMES/" + str(game) + "/thumb.png")

# Add Options Menu chioces
optionsmenu.create_choice(0, text="Update Games", effect=update_games)
optionsmenu.create_choice(1, text="Add Games")
optionsmenu.create_choice(2, text="go to openbox", effect=openbox)
optionsmenu.create_choice(3, text="CREDITS", effect=show_credits)

# Add Main Menu choices
mainmenu.create_choice(0, text="PLAY", thumb="/home/pi/PYGB_OS/play.png", effect=change_menu, param=gamesmenu)
mainmenu.create_choice(1, text="Options", thumb="/home/pi/PYGB_OS/addgames.png", effect=change_menu, param=optionsmenu)
mainmenu.create_choice(2, text="QUIT", thumb="/home/pi/PYGB_OS/quit.png", effect=quit_pygb)

# Actual Menu
actual_menu = mainmenu
actual_menu.update()


while True:

    # deactivate button pression
    buttonA = False
    buttonB = False

    # EVENTS CHECK
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            openbox()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                openbox()
            if event.key == pygame.K_DOWN:
                menuentries = len(actual_menu.sprites())
                if menuentries > 1:
                    if actual_menu.actual_choice < menuentries - 1:
                        actual_menu.actual_choice += 1
                    else:
                        actual_menu.actual_choice = 0
                    actual_menu.update()
            if event.key == pygame.K_UP:
                menuentries = len(actual_menu.sprites())
                if menuentries > 1:
                    if actual_menu.actual_choice > 0:
                        actual_menu.actual_choice -= 1
                    else:
                        actual_menu.actual_choice = menuentries - 1
                    actual_menu.update()
            if event.key == pygame.K_z:
                print("Button B pressed")
                buttonB = True
            if event.key == pygame.K_x:
                print("Button A pressed")
                buttonA = True

    # Choices Effects
    if buttonA:
        c = actual_menu.sprites()[actual_menu.actual_choice]
        c.execute(c.effect, c.param)
        actual_menu.update()
    if buttonB:
        if actual_menu.parent is not None:
            actual_menu = actual_menu.parent
            actual_menu.update()


    # DRAW IMAGES
    screen.fill(black)
    if actual_menu.actual_thumb is not None:
        screen.blit(actual_menu.actual_thumb, [height_adapt(100), height_adapt(200)])
    actual_menu.draw(screen)

    # UPDATE SCREEN
    pygame.display.update()
    clock.tick(30)
