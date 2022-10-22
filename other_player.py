import socket, os
import pygame as pg
class OtherPlayer:
    def __init__(self, game, x, y):
        self.GAME = game
        self.pos = [x,y]
        self.image = pg.image.load(os.path.join('assets/sprites/player/right/1.png'))
        self.draw_pos = [0, 0]
    def draw(self):
        self.GAME.SCREEN.blit(self.image, (self.draw_pos[0], self.draw_pos[1]))
    def update(self):
        self.draw_pos[0] = -self.GAME.camera.pos[0] + self.pos[0] + self.GAME.camera.offset[0]
        self.draw_pos[1] = -self.GAME.camera.pos[1] + self.pos[1] +  self.GAME.camera.offset[1]