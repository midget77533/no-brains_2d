
from os import fspath


class Camera:
    def __init__(self, game, target):
        self.target = target
        self.GAME = game
        self.fs = 2
        self.pos = [0,0]
        self.offset = [self.GAME.SCREEN.get_width() / 2,self.GAME.SCREEN.get_height() / 2]
    def update(self):
        self.pos = self.target.pos
        # if self.target != None:
        #     if self.pos[0] < self.target.pos[0]:
        #         self.pos[0] += self.fs
        #     if self.pos[0] > self.target.pos[0]:
        #         self.pos[0] -= self.fs
        #     if self.pos[1] < self.target.pos[1]:
        #         self.pos[1] += self.fs
        #     if self.pos[1] > self.target.pos[1]:
        #         self.pos[1] -= self.fs
