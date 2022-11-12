import pygame as pg
from camera import Camera
from settings import *

def get_image(sheet, width, height,color, col, row):
    img = pg.Surface((width, height))
    img.blit(sheet, (0,0), ((col * width),(row * height),width,height))
    img.set_colorkey(color)
    return img

class GameObject:
    def __init__(self, game, pos, images, collidable, t, a):
        self.GAME = game
        self.images = images
        self.animation_frame = 0
        self.frame_speed = 1
        self.pos = pos
        self.velocity = [0,0]
        self.draw_pos = [0,0]
        self.collidable = collidable
        self.rect = self.images[0].get_rect()
        self.type = t
        self.active = a
        self.stage = 0
        if self.type == 20:
            print(self.images)
    def draw(self):
        if self.active and self.type != 20:
            i = self.images[0]
            i.set_alpha(255)
            self.images.append(i)
            self.GAME.SCREEN.blit(i, self.draw_pos)
        elif self.type != 20:
            i = self.images[0]
            i.set_alpha(100)
            self.images.append(i)
            self.GAME.SCREEN.blit(i, self.draw_pos)
        if self.type == 20:
  
            self.GAME.SCREEN.blit(self.images[self.stage], self.draw_pos)
    def update(self):
        # self.pos[0] += self.velocity[0] * self.GAME.delta_time
        # self.pos[1] += self.velocity[1] * self.GAME.delta_time 
        self.draw_pos[0] = -self.GAME.camera.pos[0] + self.pos[0] + self.GAME.camera.offset[0]
        self.draw_pos[1] = -self.GAME.camera.pos[1] + self.pos[1] + self.GAME.camera.offset[1]

