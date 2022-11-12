import settings
from os import fspath


class Camera:
    def __init__(self, game, target):
        self.target = target
        self.GAME = game
        self.fs = 8#settings.PLAYER_X_SPEED
        self.pos = [self.target.pos[0], self.target.pos[1]]
        self.offset = [self.GAME.SCREEN.get_width() / 2,self.GAME.SCREEN.get_height() / 2]
    def update(self):
        #self.pos[0] = self.target.pos[0]
        if self.target != None:
            if self.pos[0] < self.target.pos[0] - 300:
                self.pos[0] += self.fs
            if self.pos[0] > self.target.pos[0] + 300:
                self.pos[0] -= self.fs
            if self.pos[1] < self.target.pos[1]:
                self.pos[1] += self.fs
            if self.pos[1] > self.target.pos[1]:
                self.pos[1] -= self.fs
            if self.pos[0] > 137 * 64 + 32:
                self.pos[0] = 137 * 64 + 32
            if self.pos[0] < 64 * 12 + 32:
                self.pos[0] = 64 * 12 + 32
            if self.pos[1] > 13 * 64 - 2:
                self.pos[1] = 13 * 64 - 2
            if self.pos[1] < 64 * 7:
                self.pos[1] = 64 * 7
