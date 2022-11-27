import pygame as pg
import settings
class EndAnimation:
    def __init__(self, game):
        self.GAME = game
        self.r = 255
        self.g = 0
        self.b = 0
        self.shift_speed = 5
        self.speed = 5
        self.colour = (self.r, self.g, self.b)
        self.fc = settings.WIDTH
        self.playing = False
        self.mc = 0
    def update(self):
        if self.mc == 0:
            self.g += self.shift_speed
        if self.mc == 1:
            self.r -= self.shift_speed
        if self.mc == 2:
            self.b += self.shift_speed
        if self.mc == 3:
            self.g -= self.shift_speed
        if self.mc == 4:
            self.r += self.shift_speed
        if self.mc == 5:
            self.b -= self.shift_speed
        if self.r >= 255 and self.g <= 0 and self.b <= 0:
            self.mc = 0
        if self.r >= 255 and self.g >= 255:
            self.mc = 1
        if self.g >= 255 and self.r <= 0:
            self.mc = 2
        if self.g >= 255 and self.b >= 255:
            self.mc = 3
        if self.b >= 255 and self.r <= 0 and self.g <= 0:
            self.mc = 4
        if self.r >= 255 and self.b >= 255:
            self.mc = 5
        if self.r < 0:
            self.r = 0
        if self.g < 0:
            self.g = 0
        if self.b < 0:
            self.b = 0
        if self.r > 255:
            self.r = 255
        if self.g > 255:
            self.g = 255
        if self.b > 255:
            self.b = 255
        self.colour = (self.r, self.g, self.b)


        self.fc -= self.speed
        print(self.fc)
        x = (settings.WIDTH / 2 - (self.fc / 2 * settings.SCALE)) 
        y = (settings.HEIGHT / 2 - (self.fc / 2 * settings.SCALE))
        pg.draw.rect(self.GAME.SCREEN, self.colour, [x, y, self.fc, self.fc])
        anim_complete = False
        if self.fc <= 2:
            anim_complete = True
        return anim_complete