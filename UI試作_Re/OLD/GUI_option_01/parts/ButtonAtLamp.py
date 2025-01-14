import pygame
from parts.Button import Button
from parts.Lamp   import Lamp

LAMPSIZE  = {
               "x" : 40,
               "y" : 40
            }
XDISTANCE = 30 + LAMPSIZE["x"]
YDISTANCE = LAMPSIZE["y"] // 2

COLOR = {
    "GRAY"  : ((210, 210, 210)),
    "YEROW" : ((255,255,0)),
    "GREEN" : ((0,255,0)),
}

class ButtonAtLamp(Button):
    def __init__(self, screen, x, y, width, height, image_path, action):
        self.lamp = Lamp(screen, ((x + width) - XDISTANCE), ((height + y)) - LAMPSIZE["y"], LAMPSIZE["x"], LAMPSIZE["y"], COLOR["GRAY"])
        super().__init__(screen, x, y, width, height, image_path, action)

    def draw(self):
        self.hover_button()
        self.screen.blit(self.image, self.rect) #   テキストを描画
        self.lamp.draw()
        print("button draw")
    
    def expansion_button(self):
        x = self.x - (self.width * (self.hover_scale - 1)) // 2
        y = self.y - (self.height * (self.hover_scale - 1)) // 2
        width = self.width * self.hover_scale
        height = self.height * self.hover_scale
        self.image = pygame.transform.scale(self.base_image,(width, height))
        rect = self.image.get_rect()
        rect.topleft = (x, y)
        self.rect = rect
        lamp_x = (x + width) - XDISTANCE*self.hover_scale
        lamp_y = y + (height // 2) - YDISTANCE*self.hover_scale
        self.lamp.update_coordinate(lamp_x, lamp_y, LAMPSIZE["x"] * self.hover_scale, LAMPSIZE["y"] * self.hover_scale)
    
    def default_button(self):
        self.image = pygame.transform.scale(self.base_image,(self.width, self.height))
        self.base_rect = self.image.get_rect()
        self.base_rect.topleft = (self.x, self.y)
        self.rect = self.base_rect
        lamp_x = ((self.x + self.width) - XDISTANCE)
        lamp_y = self.y + (self.height // 2) - YDISTANCE
        self.lamp.update_coordinate(lamp_x, lamp_y, LAMPSIZE["x"], LAMPSIZE["y"])

    def update_lamp_color(self, color):
        self.lamp.update_color(color)
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True