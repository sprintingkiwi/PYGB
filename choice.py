import pygame

# Class for menu choices
class Choice(pygame.sprite.Sprite):

    def __init__(self,
                 pygb,
                 ID,
                 fontname,
                 size,
                 location,
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
        self.rect.x = pygb.width_adapt(location[0])
        self.rect.y = pygb.height_adapt(location[1]) + ((2 * self.size) + (0.3 * self.size)) * self.place
        #if self.rect.y > height:
            #self.rect.y = 50
        try:
            self.thumb = pygame.image.load(thumb).convert_alpha()
            self.thumb = pygame.transform.scale(self.thumb, [int(pygb.width*0.35), int(pygb.height*0.35)])
        except:
            #self.thumb = None
            self.thumb = pygame.image.load('images/logo.png').convert_alpha()
            self.thumb = pygame.transform.scale(self.thumb, [int(pygb.width*0.35), int(pygb.height*0.35)])
        self.effect = effect
        self.param = param

    def execute(self, effect, *args):
        effect(*args)

    def update(self):
        self.font = pygame.font.SysFont(self.fontname, self.size, self.bold, self.italic)
        self.image = self.font.render(self.text, False, self.color)
