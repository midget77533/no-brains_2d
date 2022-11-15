import settings
from os import fspath
import math, pygame as pg

class Camera:
    def __init__(self, game, target):
        self.target = target
        self.tp = [500,0]
        self.GAME = game
        self.fs = 8#settings.PLAYER_X_SPEED
        self.pos = [0, -self.GAME.SCREEN.get_height()]
        self.offset = [self.GAME.SCREEN.get_width() / 2,self.GAME.SCREEN.get_height() / 2]
        self.spectating = False
        self.velocity = [0,0]
    def update(self):
        # a = self.offset[1] + (64 * settings.SCALE * 11)
        # self.pos[1] = a
        a = (1 - settings.SCALE) * 10

        if not settings.SHOW_MENU:
            if not self.spectating:
                if self.target != None:
                    if self.pos[0] < self.target.pos[0] - 300:
                        self.pos[0] += self.fs
                    if self.pos[0] > self.target.pos[0] + 300:
                        self.pos[0] -= self.fs
                    if self.pos[1] < self.target.pos[1]:
                        self.pos[1] += self.fs
                    if self.pos[1] > self.target.pos[1]:
                        self.pos[1] -= self.fs
                    if self.pos[0] - self.offset[0] < 0:
                        self.pos[0] = 0 + self.offset[0]
                    if self.pos[1] + settings.HEIGHT - self.offset[1] > (64 * 20) * settings.SCALE + (32 * a):
                        self.pos[1] = (64 * 20) * settings.SCALE + (32 * a) - self.offset[1]
            else:
                if self.target != None:
                    if self.pos[0] < self.tp[0] - 300:
                        self.pos[0] += self.fs
                    if self.pos[0] > self.tp[0] + 300:
                        self.pos[0] -= self.fs
                    if self.pos[1] < self.tp[1]:
                        self.pos[1] += self.fs
                    if self.pos[1] > self.tp[1]:
                        self.pos[1] -= self.fs
                    if self.pos[0] - self.offset[0] < 0:
                        self.pos[0] = 0 + self.offset[0]
                    if self.pos[1] + settings.HEIGHT - self.offset[1] > (64 * 20) * settings.SCALE + (32 * a):
                        self.pos[1] = (64 * 20) * settings.SCALE + (32 * a) - self.offset[1]
