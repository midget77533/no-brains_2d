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
import pickle, os, csv

default_font = pg.font.Font('assets/fonts/poppins/Poppins-bold.ttf', 15)
msg_font = pg.font.Font('assets/fonts/poppins/Poppins-bold.ttf', 30)

chat_font = pg.font.Font('assets/fonts/poppins/Poppins-bold.ttf', 20)

def get_image(sheet, width, height,color, col, row):
    img = pg.Surface((width, height))
    img.blit(sheet, (0,0), ((col * width),(row * height),width,height))
    img.set_colorkey(color)
    return img

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
        self.player = Player(self, [64 * 4, 16 * 64])
        self.delta_time = 1
        self.prev_time = 0
        self.camera = Camera(self, self.player)
        self.game_objects = []
        self.players = []
        self.client = Client(socket.gethostbyname(socket.gethostname()), 12345)
        self.chat_text = ""
        self.typing = False
        self.mouse_still_down = False
        self.play_type = "undecided"
        self.enough_players = False
        self.level = 1
        self.in_game_keys = []
        settings.CAMERA_TARGET = self.player
    def run(self):
        #self.MENU = MainMenu(self)
        self.load_level_data()
        self.SCREEN = pg.display.set_mode(RES)
        if FULL_SCREEN:
            self.SCREEN = pg.display.set_mode(RES, pg.FULLSCREEN)
        while self.running:
            self.CLOCK.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.running = False
                    self.client.running = False
                    pg.quit()
                    print("[QUIT GAME]")
                    
                    self.client.send_msg([self.client.id, "[QUIT]", self.name])
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if self.typing:
                        if event.key == pg.K_RETURN:
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
        if self.play_type == "online" and  len(self.client.players) > 0:
            self.enough_players = True
        if settings.SHOW_MENU:
            if self.play_type == "online" and self.client.rsm:
                settings.SHOW_MENU = False
            self.MENU.update()
        else:
            if self.play_type == "online":
                
                lmc = self.client.lmc
                change_in_keys = False
                if lmc != []:
                    if lmc[1] == "[0]":
                        num = lmc[2].replace("[", "")
                        num = num.replace("]", "")
                        num = int(num)
                        for obj in self.game_objects:
                            if obj.type == num:
                                obj.active = lmc[3]
                    if lmc[1] == "[1]":
                        self.player.reset_pos()
                    if lmc[1] == "[2]":
                        obj_pos = lmc[2]
                        for go in self.game_objects:
                            if go.pos == obj_pos:
                                self.game_objects.remove(go)
                                print('obj_destroyed')
                    if lmc[1] == "[3]":
                        self.level = lmc[2]
                        self.player.reset_pos()
                    self.client.lmc = []
            self.player.update()          
        self.camera.update()

    def draw(self):
        self.clear_screen()
        if settings.SHOW_MENU:
            if self.play_type == "online" and self.client.running:
                self.players = self.client.players
                self.client.send_msg("[GET_DATA]")
            self.MENU.draw()
        else:
            wo = []
            for go in self.game_objects:
                if go.type != 19:
                    go.update()
                    go.draw()
                else:
                    wo.append(go)
            self.player.draw()

            for go in wo:
                go.update()
                go.draw()
            if self.play_type == "online":
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

                        self.text_to_screen(op[5], dx + 32, dy - 20)
                        r1 = [p.pos[0], p.pos[1], p.coll_rect[2], p.coll_rect[3]]
                        r2 = [op[1], op[2], p.coll_rect[2], p.coll_rect[3]]
                        if r1[0] + r1[2] > r2[0] and r2[0] + r2[2] > r1[0] and r1[1] + r1[3] > r2[1] and r2[1] + r2[3] > r1[1]:
                            if r1[1] > r2[1]:
                                self.player.draw()
                    
                self.text_to_screen(self.name, self.player.draw_pos[0] + 32, self.player.draw_pos[1] - 20)
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
    def load_level_data(self):
        img_list = []

        BLACK = (0,0,0)

        images = []
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

        t10 = get_image(tile_sheet,64,64,BLACK, 3, 0)
        t11 = get_image(tile_sheet,64,64,BLACK, 4, 0)
        t12 = get_image(tile_sheet,64,64,BLACK, 5, 0)
        t13 = get_image(tile_sheet,64,64,BLACK, 3, 1)
        t14 = get_image(tile_sheet,64,64,BLACK, 4, 1)
        t15 = get_image(tile_sheet,64,64,BLACK, 5, 1)
        t16 = get_image(tile_sheet,64,64,BLACK, 3, 2)
        t17 = get_image(tile_sheet,64,64,BLACK, 4, 2)
        t18 = get_image(tile_sheet,64,64,BLACK, 5, 2)
        t19 = get_image(tile_sheet,64,64,BLACK, 6, 0)
        t20 = get_image(tile_sheet,64,64,BLACK, 6, 1)
        images.append(t1)
        images.append(t2)
        images.append(t3)
        images.append(t4)
        images.append(t5)
        images.append(t6)
        images.append(t7)
        images.append(t8)
        images.append(t9)

        images.append(t10)
        images.append(t11)
        images.append(t12)
        images.append(t13)
        images.append(t14)
        images.append(t15)
        images.append(t16)
        images.append(t17)
        images.append(t18)
        images.append(t19)
        images.append(t20)

        self.game_objects = []

        TILE_SPACING = 64
        with open(os.path.join('levels',f'level{self.level}_data.csv'), newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    if int(tile) >= 0:
                        if int(tile) < 9:
                            self.game_objects.append(GameObject(self, [TILE_SPACING * y, TILE_SPACING * x], [images[int(tile)]], True, int(tile)))
                        elif int(tile) >= 9:
                            self.game_objects.append(GameObject(self, [TILE_SPACING * y, TILE_SPACING * x], [images[int(tile)]], False, int(tile)))
                        if int(tile) >= 9 < 18:
                            self.in_game_keys.append([TILE_SPACING * x, TILE_SPACING * y, int(tile)])
    def text_objects(self, txt):
        txt_surf = default_font.render(txt, True, (0,0,0))
        return txt_surf, txt_surf.get_rect()
    def text_to_screen(self, txt, cx, cy):
        text_surf, text_rect = self.text_objects(txt)
        text_rect.center = (cx), (cy)
        self.SCREEN.blit(text_surf, text_rect)
    def clear_screen(self):
        WHITE = (255,255,255)
        if settings.SHOW_MENU:
            self.SCREEN.fill(WHITE)
        else:
            self.SCREEN.fill((50,50,50))
    def check_buttons(self):
        pass