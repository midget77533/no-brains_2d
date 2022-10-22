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

class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption(TITLE)
    def new_game(self):
        self.name = input("username: ")
        print(self.name)
        self.running = True
        self.SCREEN = pg.display.set_mode(RES) 
        self.MENU = MainMenu(self)
        self.CLOCK = pg.time.Clock()
        self.buttons = []
        self.player = Player(self, [0, 0])
        self.delta_time = 1
        self.prev_time = 0
        self.camera = Camera(self, self.player)
        self.game_objects = [] #[GameObject(self,[500, 400], [pg.image.load("assets/textures/start_btn.png")], True)]
        self.players = []
        self.client = self.client = Client('10.0.0.10', 12345)
        settings.CAMERA_TARGET = self.player
    def run(self):
        self.SCREEN = pg.display.set_mode(RES)
        if FULL_SCREEN:
            self.SCREEN = pg.display.set_mode(RES, pg.FULLSCREEN)
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.running = False
                    pg.quit()
                    print("[QUIT GAME]")
                    self.client.send_msg([self.client.id, "[QUIT]"])
                    sys.exit()
                    

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