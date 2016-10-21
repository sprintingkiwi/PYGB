import pygame
import time
import os
import subprocess
from choice import Choice



# class for menus
class Menu(pygame.sprite.OrderedUpdates):

    def __init__(self,
                 pygb,
                 fontname="Liberation Serif",
                 size=32,
                 bold=True,
                 italic=False,
                 color=[255, 255, 255],
                 selection_color=[255, 0, 0],
                 selection_zoom=0.125,
                 parent = None,
                 *args):
        super(Menu, self).__init__()
        self.pygb = pygb
        self.fontname = fontname
        self.size = (size * self.pygb.height) / 720
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
        self.add(Choice(self.pygb,
                        ID,
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