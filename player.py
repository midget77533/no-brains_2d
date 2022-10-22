import pygame as pg
from settings import *
import os, math
from networking import *

class Player:
    def __init__(self, GAME,pos=[0,0]):
        self.GAME = GAME
        self.pos = pos
        self.velocity = [0,0]
        self.right_sprites = [
        pg.image.load(os.path.join('assets/sprites/player/right/1.png')), 
        pg.image.load(os.path.join('assets/sprites/player/right/2.png'))]
        self.left_sprites = [
        pg.image.load(os.path.join('assets/sprites/player/left/1.png')), 
        pg.image.load(os.path.join('assets/sprites/player/left/2.png'))]
        for s in range(len(self.right_sprites)):
            i = pg.transform.scale(self.right_sprites[s], (24 * 4, 35 * 4))
            self.right_sprites[s] = i
            i = pg.transform.scale(self.left_sprites[s], (24 * 4, 35 * 4))
            self.left_sprites[s] = i
        self.draw_pos = [0,0]
        self.anim_frame = 0
        self.direction = 1
        self.coll_rect = self.right_sprites[0].get_rect()
        
    def draw(self):
        if self.direction == 1:
            self.GAME.SCREEN.blit(self.right_sprites[int(self.anim_frame)], (self.draw_pos[0], self.draw_pos[1]))
        if self.direction == 0:
            self.GAME.SCREEN.blit(self.left_sprites[int(self.anim_frame)], (self.draw_pos[0], self.draw_pos[1]))
    def update(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1] 
        if self.velocity[0] != 0 or self.velocity[1] != 0:
            self.GAME.client.send_msg([self.GAME.client.id, self.pos[0], self.pos[1], self.direction, self.anim_frame])
        self.move()
        self.draw_pos[0] = -self.GAME.camera.pos[0] + self.pos[0] + self.GAME.camera.offset[0]
        self.draw_pos[1] = -self.GAME.camera.pos[1] + self.pos[1] + self.GAME.camera.offset[1]

    def check_x_collision(self, pos):
        for go in self.GAME.game_objects:
            if go.collidable:
                if (pos + self.coll_rect[2] > go.pos[0]) and (pos < go.pos[0] + go.rect[2]):
                    return True
    def check_y_collision(self, pos):
        for go in self.GAME.game_objects:
            if go.collidable:
                if pos + self.coll_rect[3] > go.pos[1] and pos < go.pos[1] + go.rect[3]:
                    return True
    def move(self):
        keys_pressed = pg.key.get_pressed()
        mx, my = pg.mouse.get_pos()
        dx = mx - self.draw_pos[0]
        dy = my - self.draw_pos[1]
        angle = math.atan2(dx, dy)
        mvx = math.sin(angle)
        mvy = math.cos(angle)
        if keys_pressed[pg.K_w]:
            self.velocity[0] = mvx * PLAYER_X_SPEED * self.GAME.delta_time
            self.velocity[1] = mvy * PLAYER_Y_SPEED *self.GAME.delta_time
        elif keys_pressed[pg.K_s]:
            self.velocity[0] = -(mvx * PLAYER_X_SPEED * self.GAME.delta_time)
            self.velocity[1] = -(mvy * PLAYER_Y_SPEED *self.GAME.delta_time)
        else:
            self.velocity[0] = 0
            self.velocity[1] = 0
        if self.check_x_collision(self.pos[0] + self.velocity[0]) and self.check_y_collision(self.pos[1] + self.velocity[1]):
            self.velocity[0] = 0
            self.velocity[1] = 0
        if  self.velocity[0] > 0:
            self.direction = 1
            self.anim_frame += 0.1
            if self.anim_frame >= len(self.right_sprites):
                self.anim_frame = 0
        elif  self.velocity[0] < 0:
            self.direction = 0
            self.anim_frame += 0.1
            if self.anim_frame >= len(self.left_sprites):
                self.anim_frame = 0
        elif self.velocity[1] != 0:
            self.anim_frame += 0.1
            if self.anim_frame >= len(self.left_sprites):
                self.anim_frame = 0
        
