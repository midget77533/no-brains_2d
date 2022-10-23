import pygame as pg

class Button:
    def __init__(self, game, x, y, image, name, scale):
        self.GAME = game
        width = image.get_width()
        height = image.get_height()
        self.image = image
        self.image = pg.transform.scale(image, (int(width * scale * 2), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.name = name
    def draw(self):
        self.GAME.SCREEN.blit(self.image, (self.rect.x, self.rect.y))
    def check_click(self):
        action = False
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return action