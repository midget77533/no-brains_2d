import pygame as pg
from settings import *
import os, math, time
from networking import *
from buttons import *

def get_image(sheet, width, height,color, col, row):
    img = pg.Surface((width, height))
    img.blit(sheet, (0,0), ((col * width),(row * height),width,height))
    img.set_colorkey(color)
    return img

class Player:
    def __init__(self, GAME,pos):
        self.GAME = GAME
        self.pos = pos
        self.og_pos = pos
        self.velocity = [0,0]
        self.right_sprites = [
        pg.image.load(os.path.join('assets/sprites/player/right/1.png')), 
        ]
        self.left_sprites = [
        pg.image.load(os.path.join('assets/sprites/player/left/1.png')), 
        ]
        for s in range(len(self.right_sprites)):
            i = pg.transform.scale(self.right_sprites[s], (64, 64))
            self.right_sprites[s] = i
            i = pg.transform.scale(self.left_sprites[s], (64, 64))
            self.left_sprites[s] = i
        self.draw_pos = [0,0]
        self.anim_frame = 0
        self.direction = 1
        self.coll_rect = self.right_sprites[0].get_rect()
        self.gravity_scale = 1
        self.terminal_velocity = 35
        self.jump_power = 16
        self.grounded = False
        self.completed_level = False
        self.tb1 = Button(self.GAME, 20, 100, pg.image.load("assets/textures/multi_player_btn.png"), "[T|-1]", 1, 1)
        self.tb2 = Button(self.GAME, 20, 170, pg.image.load("assets/textures/multi_player_btn.png"), "[T|-1]", 1, 1)
        self.tb3 = Button(self.GAME, 20, 240, pg.image.load("assets/textures/multi_player_btn.png"), "[T|-1]", 1, 1)
        self.pos_locked = False
        self.spawn_point = [64 * 4, 16 * 64]
        self.alive = True
        self.pop_sound = self.GAME.mixer.Sound('assets/audio/pop.wav')
        images = []
        BLACK = (0,0,0)
        tile_sheet = pg.image.load('assets/textures/brick_tile_sheet.png')
        t1 = get_image(tile_sheet,64,64,BLACK, 0, 0)
        t2 = get_image(tile_sheet,64,64,BLACK, 1, 0)
        t3 = get_image(tile_sheet,64,64,BLACK, 2, 0)
        t4 = get_image(tile_sheet,64,64,BLACK, 0, 1)
        t5 = get_image(tile_sheet,64,64,BLACK, 1, 1)
        t6 = get_image(tile_sheet,64,64,BLACK, 2, 1)
        t7 = get_image(tile_sheet,64,64,BLACK, 0, 2)
        t8 = get_image(tile_sheet,64,64,BLACK, 1, 2)
        t9 = get_image(tile_sheet,64,64,BLACK, 2, 2)

        images.append(t1)
        images.append(t2)
        images.append(t3)
        images.append(t4)
        images.append(t5)
        images.append(t6)
        images.append(t7)
        images.append(t8)
        images.append(t9)
        self.button_target_sprites = images
    def draw(self):
        self.draw_pos[0] = -self.GAME.camera.pos[0] + self.pos[0] + self.GAME.camera.offset[0]
        self.draw_pos[1] = -self.GAME.camera.pos[1] + self.pos[1] + self.GAME.camera.offset[1]
        if self.tb1.name != "[T|-1]":
            self.tb1.draw()
        if self.tb2.name != "[T|-1]":
            self.tb2.draw()
        if self.tb3.name != "[T|-1]":
            self.tb3.draw()
        if self.direction == 1 and self.alive:
            self.GAME.SCREEN.blit(self.right_sprites[int(self.anim_frame)], (self.draw_pos[0], self.draw_pos[1]))
        if self.direction == 0 and self.alive:
            self.GAME.SCREEN.blit(self.left_sprites[int(self.anim_frame)], (self.draw_pos[0], self.draw_pos[1]))
        if not self.alive:
            if type(self.anim_frame / 2) == int:
                self.GAME.SCREEN.blit(self.left_sprites[int(self.anim_frame)], (self.draw_pos[0], self.draw_pos[1]))
    def update(self):
        keys_pressed = pg.key.get_pressed()
        mx, my = pg.mouse.get_pos()
        if not self.pos_locked:
            self.pos[0] += self.velocity[0] * self.GAME.delta_time
            self.pos[1] += self.velocity[1] * self.GAME.delta_time
        if abs(self.velocity[0]) > 2 or abs(self.velocity[1]) > 2:
            if self.GAME.play_type == "online":
                self.GAME.client.send_msg([self.GAME.client.id, self.pos[0], self.pos[1], self.direction, self.anim_frame])
        if keys_pressed[pg.K_p]:
            self.GAME.client.send_msg("/tp")
        if self.tb1.check_click():
            num = self.tb1.name.replace("]", "")
            num = num.split("|")
            num = int(num[1])
            active = False
            for obj in self.GAME.game_objects:
                if obj.type == num:
                    obj.active = not obj.active
                    if obj.active:
                        active = True
            if self.GAME.play_type == "online":
                self.GAME.client.send_msg(["[MAP_CHANGE]", "[0]", f"[{num}]", active])
        if self.tb2.check_click():
            num = self.tb2.name.replace("]", "")
            num = num.split("|")
            num = int(num[1])
            active = False
            for obj in self.GAME.game_objects:
                if obj.type == num:
                    obj.active = not obj.active
                    if obj.active:
                        active = True
            if self.GAME.play_type == "online":
                self.GAME.client.send_msg(["[MAP_CHANGE]", "[0]", f"[{num}]", active])
        if self.tb3.check_click():
            num = self.tb3.name.replace("]", "")
            num = num.split("|")
            num = int(num[1])
            active = False
            for obj in self.GAME.game_objects:
                if obj.type == num:
                    obj.active = not obj.active
                    if obj.active:
                        active = True
            if self.GAME.play_type == "online":
                self.GAME.client.send_msg(["[MAP_CHANGE]", "[0]", f"[{num}]", active])
        self.move()
    def check_collision(self, pos):
        for go in self.GAME.game_objects:
            if go.collidable and go.active:
                if (pos[0] + self.coll_rect[2] - 5 > go.pos[0] and pos[0] + 5 < go.pos[0] + go.rect[2]) and (pos[1] + self.coll_rect[3] + 1> go.pos[1] and pos[1] < go.pos[1]) and go.type != 18:
                    self.grounded = True
                    self.pos[1] = go.pos[1] - self.coll_rect[3]
                    if self.velocity[1] > 1:
                        if self.GAME.play_type == "online":
                            self.GAME.client.send_msg([self.GAME.client.id, self.pos[0], self.pos[1], self.direction, self.anim_frame])
                    self.velocity[1] = 0
                    break
                else:
                    self.grounded = False
        for go in self.GAME.game_objects:
            if go.collidable and go.active:
                if (pos[0] + self.coll_rect[2] - 5 > go.pos[0] and pos[0] + 5 < go.pos[0] + go.rect[2]) and (pos[1] < go.pos[1] + go.rect[3] and pos[1] > go.pos[1]):
                    self.pos[1] = go.pos[1] + go.rect[3] + 1
                    self.velocity[1] = 2
                    break
                if (pos[0] + self.coll_rect[2] + self.velocity[0] > go.pos[0] and pos[0] < go.pos[0]) and (pos[1] + self.coll_rect[3] - 1> go.pos[1] and pos[1] < go.pos[1] + go.rect[3]) and go.type != 18:
                    self.pos[0] = go.pos[0] - self.coll_rect[3] - 1
                    self.velocity[0] = 0
                if (pos[0] > go.pos[0] and pos[0] + self.velocity[0] < go.pos[0] + go.rect[3]) and (pos[1] + self.coll_rect[3] - 1> go.pos[1] and pos[1] < go.pos[1] + go.rect[3]) and go.type != 18:
                    self.pos[0] = go.pos[0] + go.rect[3] + 1
                    self.velocity[0] = 0    

            #launch pad
            if (pos[0] + self.coll_rect[2] - 5 > go.pos[0] and pos[0] + 5 < go.pos[0] + go.rect[2] and pos[1] + self.coll_rect[3] > go.pos[1] and pos[1] < go.pos[1] + go.rect[3]) and go.type == 18:
                self.velocity[1] = -40
            #check_point
            if (pos[0] + self.coll_rect[2] - 5 > go.pos[0] and pos[0] + 5 < go.pos[0] + go.rect[2] and pos[1] + self.coll_rect[3] > go.pos[1] and pos[1] < go.pos[1] + go.rect[3]) and go.type == 20 and go.stage == 0:
                self.GAME.check_point = go.pos
                # if self.GAME.play_type == "online":
                #     self.GAME.client.send_msg(["[MAP_CHANGE]", "[3]", go.pos])
                go.stage = 1
            #die
            if (pos[0] + self.coll_rect[2] - 10 > go.pos[0] and pos[0] + 10 < go.pos[0] + go.rect[2] and pos[1] + self.coll_rect[3] > go.pos[1] and pos[1] < go.pos[1] + go.rect[3]) and go.type == 21:
                self.pop_sound.play()
                self.death_animation()
            #keys
            if (pos[0] + self.coll_rect[2] > go.pos[0] and pos[0] < go.pos[0] + go.rect[2] and pos[1] + self.coll_rect[3] > go.pos[1] and pos[1] < go.pos[1] + go.rect[3]) and go.type < 18 and go.type > 8:
                if self.tb1.name == "[T|-1]":
                    self.tb1.name = f"[T|{go.type - 9}]" 
                    self.tb1.image = self.button_target_sprites[go.type - 9]
                    self.tb1.rect = self.tb1.image.get_rect()
                    self.tb1.rect.topleft = (self.tb1.x, self.tb1.y)
                    if self.GAME.play_type == "online":
                        self.GAME.client.send_msg(["[MAP_CHANGE]", "[2]", go.pos])
                    self.GAME.game_objects.remove(go)
                elif self.tb2.name == "[T|-1]":
                    self.tb2.name = f"[T|{go.type - 9}]" 
                    self.tb2.image = self.button_target_sprites[go.type - 9]
                    self.tb2.rect = self.tb2.image.get_rect()
                    self.tb2.rect.topleft = (self.tb2.x, self.tb2.y)
                    if self.GAME.play_type == "online":
                        self.GAME.client.send_msg(["[MAP_CHANGE]", "[2]", go.pos])
                    self.GAME.game_objects.remove(go)
                elif self.tb3.name == "[T|-1]":
                    self.tb3.name = f"[T|{go.type - 9}]" 
                    self.tb3.image = self.button_target_sprites[go.type - 9]
                    self.tb3.rect = self.tb3.image.get_rect()
                    self.tb3.rect.topleft = (self.tb3.x, self.tb3.y)
                    if self.GAME.play_type == "online":
                        self.GAME.client.send_msg(["[MAP_CHANGE]", "[2]", go.pos])
                    self.GAME.game_objects.remove(go)
            if (pos[0] + self.coll_rect[2] - 5 > go.pos[0] and pos[0] + 5 < go.pos[0] + go.rect[2] and pos[1] + self.coll_rect[3] > go.pos[1] and pos[1] < go.pos[1] + go.rect[3]) and not self.completed_level and go.type == 19:
                self.completed_level = True
                self.pos_locked = True
                self.pos[1] = 64 * 24
                if self.GAME.play_type == "online":
                    self.GAME.client.send_msg(["[MAP_CHANGE]", "[3]", 0])
                    self.GAME.camera.spectating = True
                else:
                    self.GAME.level += 1
                    self.reset_pos()
                break
            else:
                self.completed_level = False
        if self.GAME.play_type == "online":
            for p in self.GAME.client.players:
                x = p[1]
                y = p[2]
                if (pos[0] + self.coll_rect[2] - 5 > x and pos[0] + 5 < x + 64) and (pos[1] + self.coll_rect[3] > y and pos[1] + 10< y) and p[0] != self.GAME.client.id:
                    self.velocity[1] = 0
                    self.grounded = True
                    self.pos[1] = y - self.coll_rect[3]
                    break
    def death_animation(self):
        self.alive = False
        self.respawn_animation()
    def respawn_animation(self):
        self.reset_pos()
        if self.GAME.play_type == "online":
            self.GAME.client.send_msg(["[MAP_CHANGE]", "[1]", 0])

        self.anim_frame = 0
        self.alive = True
    def reset_pos(self):
        self.GAME.camera.spectating = False
        self.pos = self.GAME.check_point
        self.velocity = [0,-5]
        #self.GAME.camera.pos = self.pos
        self.tb1 = Button(self.GAME, 20, 100, pg.image.load("assets/textures/multi_player_btn.png"), "[T|-1]", 1, 1)
        self.tb2 = Button(self.GAME, 20, 170, pg.image.load("assets/textures/multi_player_btn.png"), "[T|-1]", 1, 1)
        self.tb3 = Button(self.GAME, 20, 240, pg.image.load("assets/textures/multi_player_btn.png"), "[T|-1]", 1, 1)
        self.GAME.load_level_data()
        self.completed_level = False
        self.pos_locked = False
        self.grounded = False       
    def move(self):
        if not self.grounded and self.velocity[1] <= self.terminal_velocity:
            self.velocity[1] += self.gravity_scale * self.GAME.delta_time
        keys_pressed = pg.key.get_pressed()
        if keys_pressed[pg.K_r] and not self.GAME.typing:
            self.respawn_animation()
            # if self.GAME.play_type == "online":
            #     self.GAME.client.send_msg(["[MAP_CHANGE]", "[1]", f"[]"])
        if keys_pressed[pg.K_SPACE] and self.grounded and not self.GAME.typing:
            self.pos[1] -= 5
            self.velocity[1] = -self.jump_power 
            self.grounded = False
        if keys_pressed[pg.K_a] and not self.GAME.typing:
            self.velocity[0] = -PLAYER_X_SPEED 
        elif keys_pressed[pg.K_d] and not self.GAME.typing:
            self.velocity[0] = PLAYER_X_SPEED 
        else:
            self.velocity[0] = 0
        
        self.check_collision(self.pos)

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
        
