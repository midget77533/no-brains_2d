from os import error
import pygame as pg
from settings import *
from main_menu import *
from player import Player
import time
import sys
import settings
from camera import *
from game_object import *
from networking import *
import pickle

default_font = pg.font.Font('assets/fonts/poppins/Poppins-bold.ttf', 15)
msg_font = pg.font.Font('assets/fonts/poppins/Poppins-bold.ttf', 30)
chat_font = pg.font.Font('assets/fonts/poppins/Poppins-bold.ttf', 20)

class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption(TITLE)
    def new_game(self):
        self.name = "player" #input("username: ")

        self.running = True
        self.SCREEN = pg.display.set_mode(RES) 
        self.MENU = MainMenu(self)
        self.CLOCK = pg.time.Clock()
        self.buttons = []
        self.player = Player(self, [-400, 0])
        self.delta_time = 1
        self.prev_time = 0
        self.camera = Camera(self, self.player)
        self.game_objects = [GameObject(self, [200, 200], [pg.image.load('assets/textures/start_btn.png')], False)]
        self.players = []
        self.client = self.client = Client('10.0.0.10', 12345)
        self.chat_text = ""
        self.typing = False
        settings.CAMERA_TARGET = self.player
    def run(self):
        #self.MENU = MainMenu(self)
        self.SCREEN = pg.display.set_mode(RES)
        if FULL_SCREEN:
            self.SCREEN = pg.display.set_mode(RES, pg.FULLSCREEN)
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.running = False
                    pg.quit()
                    print("[QUIT GAME]")
                    self.client.send_msg([self.client.id, "[QUIT]", self.name])
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if self.typing:
                        if event.key == pg.K_RETURN:
                            # if self.chat_text[0] == "/":
                            #     self.client.send_msg(["[MSG]", f"{self.chat_text)}"])
                            #     print(self.chat_text)
                            #     self.chat_text = ""
                            #     self.typing = False
                            # else:
                            self.client.send_msg(["[MSG]", f"<{self.name}> {self.chat_text}"])
                            self.chat_text = ""
                            self.typing = False
                                
                        if event.key == pg.K_BACKSPACE and len(self.chat_text) > 0:
                            self.chat_text = self.chat_text[:-1]
                        else:
                            self.chat_text += event.unicode
                if event.type == pg.KEYDOWN and event.key == pg.K_t and not settings.SHOW_MENU:
                    self.typing = True
                if event.type == pg.KEYDOWN:
                    if self.MENU.selected_box >= 0:
                        if event.key == pg.K_BACKSPACE:
                            self.MENU.text_in_fields[self.MENU.selected_box] = self.MENU.text_in_fields[self.MENU.selected_box][:-1]
                        elif len(self.MENU.text_in_fields[self.MENU.selected_box]) < 15:
                            self.MENU.text_in_fields[self.MENU.selected_box] += event.unicode
            self.set_delta_time()
            self.update()
            self.draw()
    def set_delta_time(self):
        now = time.time()
        self.delta_time = (now - self.prev_time) * FPS
        self.prev_time = now
    def update(self):
        if settings.SHOW_MENU:
            self.MENU.update()
        else:
            self.player.update()            
        self.camera.update()
    def draw(self):
        self.clear_screen()
        if settings.SHOW_MENU:
            self.MENU.draw()
        else:
            for go in self.game_objects:
                go.update()
                go.draw()
            self.player.draw()
            self.client.send_msg("[GET_DATA]")
            self.players = self.client.players
            p = self.player
            for op in self.players:
                if op[0] != self.client.id and op[1] != "[QUIT]":
                    dx = -self.camera.pos[0] + op[1] + self.camera.offset[0]
                    dy = -self.camera.pos[1] + op[2] + self.camera.offset[1]
                    if op[3] == 0:
                        self.SCREEN.blit(self.player.left_sprites[int(op[4])], (dx, dy))
                    else:
                        self.SCREEN.blit(self.player.right_sprites[int(op[4])], (dx, dy))

                    self.text_to_screen(op[5], dx + 48, dy - 20)
                    r1 = [p.pos[0], p.pos[1], p.coll_rect[2], p.coll_rect[3]]
                    r2 = [op[1], op[2], p.coll_rect[2], p.coll_rect[3]]
                    if r1[0] + r1[2] > r2[0] and r2[0] + r2[2] > r1[0] and r1[1] + r1[3] > r2[1] and r2[1] + r2[3] > r1[1]:
                        if r1[1] > r2[1]:
                            self.player.draw()
                
            self.text_to_screen(self.name, self.player.draw_pos[0] + 48, self.player.draw_pos[1] - 20)
            if self.typing:
                s = pg.Surface((self.SCREEN.get_width(), 100))
                s.fill((0,0,0))
                s.set_alpha(80)
                surf = msg_font.render(self.chat_text, True, (0,0,0))
                self.SCREEN.blit(s, (0,self.SCREEN.get_height() - 40))
                self.SCREEN.blit(surf, (0, self.SCREEN.get_height() - 40))
            for m in range(len(self.client.visible_messages)):
                msg = self.client.visible_messages[m]
                if msg[1] > 0:
                    color = (0,0,0)
                    if msg[0].split(":")[0] == "[SERVER]":
                        color = (201, 60, 79)
                    surf = msg_font.render(msg[0], True, color)
                    s = pg.Surface((surf.get_width() + 10, surf.get_height()))
                    s.fill((0,0,0))
                    s.set_alpha(30)
                    a = surf.get_height()
                    p = (len(self.client.visible_messages) * a)
                    self.SCREEN.blit(s, (0, self.SCREEN.get_height() - p + (m * a) - 150))
                    self.SCREEN.blit(surf, (0, self.SCREEN.get_height() - p + (m * a) - 150))
                    msg[1] -= 1 / 60 * self.delta_time
        pg.display.update()
    def text_objects(self, txt):
        txt_surf = default_font.render(txt, True, (0,0,0))
        return txt_surf, txt_surf.get_rect()
    def text_to_screen(self, txt, cx, cy):
        text_surf, text_rect = self.text_objects(txt)
        text_rect.center = (cx), (cy)
        self.SCREEN.blit(text_surf, text_rect)
    def clear_screen(self):
        self.SCREEN.fill((255,255,255))
    def check_buttons(self):
        pass