import pygame as pg
from camera import Camera
from settings import *
class GameObject:
    def __init__(self, game, pos, images, collidable):
        self.GAME = game
        self.images = images
        self.animation_frame = 0
        self.frame_speed = 1
        self.pos = [0,0]
        self.velocity = [0,0]
        self.draw_pos = pos
        self.collidable = collidable
        self.rect = self.images[0].get_rect()
    def draw(self):
        self.GAME.SCREEN.blit(self.images[0], self.draw_pos)
    def update(self):
        # self.pos[0] += self.velocity[0] * self.GAME.delta_time
        # self.pos[1] += self.velocity[1] * self.GAME.delta_time

        self.draw_pos[0] = -self.GAME.camera.pos[0] + self.pos[0] + self.GAME.camera.offset[0]
        self.draw_pos[1] = -self.GAME.camera.pos[1] + self.pos[1] +  self.GAME.camera.offset[1]

