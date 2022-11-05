import pygame as pg

class Button:
    def __init__(self, game, x, y, image, name, x_scale, y_scale):
        self.GAME = game
        width = image.get_width()
        height = image.get_height()
        self.image = image
        self.x = x
        self.y = y
        self.image = pg.transform.scale(image, (int(width * x_scale), int(height * y_scale)))
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
            if pg.mouse.get_pressed()[0] == 1 and not self.clicked and not self.GAME.mouse_still_down:
                self.clicked = True
                self.GAME.mouse_still_down = True
                action = True
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False
            self.GAME.mouse_still_down = False
        return action