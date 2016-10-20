import pygame
from OS import Menu, Choice

pygame.init()

screen = pygame.display.set_mode([800, 600])

#font = pygame.font.SysFont("Liberation Serif", 32, False, True)


credits_scroll = Menu(fontname="MV Boli", size=32, color=[0, 255, 0])

cred = open("/home/pi/PYGB_OS/CREDITS.txt")
lines = cred.readlines()
for line in lines:
    credits_scroll.create_choice(lines.index(line), text=line)
