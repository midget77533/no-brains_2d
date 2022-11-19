import pygame as pg
from camera import Camera
from settings import *
import settings
def get_image(sheet, width, height,color, col, row):
    img = pg.Surface((width, height))
    img.blit(sheet, (0,0), ((col * width),(row * height),width,height))
    img.set_colorkey(color)
    return img

class GameObject:
    def __init__(self, game, pos, images, collidable, t, a, v):
        self.GAME = game
        self.images = images
        self.animation_frame = 0
        self.frame_speed = 1
        self.pos = pos
        self.velocity = v
        self.og_vel = v
        self.draw_pos = [0,0]
        self.collidable = collidable
        self.rect = self.images[0].get_rect()
        self.rect = [self.rect[0], self.rect[1], 64, 64]
        self.type = t
        self.active = a
        self.stage = 0
        self.mc = 0
        self.color = (255,0,0)
        self.r = 255
        self.g = 0
        self.b = 0
        self.shift_speed = 5
        self.draw_pos = [self.draw_pos[0] * settings.SCALE, self.draw_pos[1] * settings.SCALE]
        self.moving = False
        if self.velocity[0] != 0 or self.velocity[1] != 0:
            self.moving = True
    def draw(self):
        if self.type != 29:
            if self.active and (self.type != 20 and self.type != 19 and self.type != 26):
                i = self.images[0]
                i.set_alpha(255)
                self.images.append(i)
                self.GAME.SCREEN.blit(i, (self.draw_pos[0] * settings.SCALE, self.draw_pos[1] * settings.SCALE))
            elif (self.type != 20 and self.type != 19):
                i = self.images[0]
                i.set_alpha(100)
                self.images.append(i)
                self.GAME.SCREEN.blit(i, (self.draw_pos[0] * settings.SCALE, self.draw_pos[1] * settings.SCALE))
            if self.type == 20:
                self.GAME.SCREEN.blit(self.images[self.stage], (self.draw_pos[0] * settings.SCALE, self.draw_pos[1] * settings.SCALE))
            if self.type == 26:
                i = self.images[0]
                i.set_alpha(100)
                #self.images.append(i)
                self.GAME.SCREEN.blit(i, (self.draw_pos[0] * settings.SCALE, self.draw_pos[1] * settings.SCALE))
        #pg.draw.rect(self.GAME.SCREEN, (255,255,0), [self.pos[0]* settings.SCALE, self.draw_pos[1]* settings.SCALE, 64 * settings.SCALE, 64 * settings.SCALE])
        if self.type == 19:
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
            self.color = (self.r, self.g, self.b)
            #print(self.color)
            pg.draw.rect(self.GAME.SCREEN, self.color, [self.draw_pos[0] * settings.SCALE, self.draw_pos[1] * settings.SCALE, 64 * settings.SCALE, 64 * settings.SCALE])
    def update(self):
        if self.moving:
            self.pos[0] += self.velocity[0] * self.GAME.delta_time
            self.pos[1] += self.velocity[1] * self.GAME.delta_time 
            for go in self.GAME.game_objects:
                x = self.pos[0]
                y = self.pos[1]
                x1 = go.pos[0]
                y1 = go.pos[1]
                if go != self and go.active and go.type != 25:
                    if x < x1+ 64 and x > x1 and y + 64 > y1 and y < y1 + 64:
                        self.pos[0] -= -2
                        self.velocity[0] *= -1
                        
                    if x + 64 > x1 and x < x1 and y + 64 > y1 and y < y1 + 64:
                        self.pos[0] -= 2
                        self.velocity[0] *= -1
                    if x + 64 > x1 and x < x1 + 64 and y + 64 > y1 and y < y1:
                        self.pos[1] -= 2
                        self.velocity[1] *= -1
                    if x + 64 > x1 and x < x1 + 64 and y < y1 + 64 and y > y1:
                        self.pos[1] -= -2
                        self.velocity[1] *= -1 
                        

        self.draw_pos[0] = -self.GAME.camera.pos[0] + self.pos[0] + self.GAME.camera.offset[0]
        self.draw_pos[1] = -self.GAME.camera.pos[1] + self.pos[1] + self.GAME.camera.offset[1]

