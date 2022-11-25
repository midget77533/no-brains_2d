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
from fade_animation import *
from end_animation import *
import pyperclip

default_font = pg.font.Font('assets/fonts/poppins/Poppins-bold.ttf', int(15* settings.SCALE))
pop_up_font = pg.font.Font('assets/fonts/poppins/Poppins-bold.ttf', int(45* settings.SCALE))
coin_ui_font =  pg.font.Font('assets/fonts/poppins/Poppins-bold.ttf', int(35* settings.SCALE))
msg_font = pg.font.Font('assets/fonts/poppins/Poppins-bold.ttf', int(30* settings.SCALE))

chat_font = pg.font.Font('assets/fonts/poppins/Poppins-bold.ttf', int(20* settings.SCALE))

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
        self.mixer = pg.mixer
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
        self.client = Client("", 12345)
        self.chat_text = ""
        self.typing = False
        self.mouse_still_down = False
        self.play_type = "undecided"
        self.enough_players = False
        self.level = 0
        self.in_game_keys = []
        self.player_num = 255
        self.check_point = [64 * 4, 16 * 64]
        self.music = self.mixer.music.load('assets/audio/test_song.wav')
        settings.CAMERA_TARGET = self.player
        self.sn = 0
        self.tick_buffer = 0
        self.fg = [pg.image.load('assets/level_editor/images/foreground.png').convert_alpha(), pg.image.load('assets/level_editor/images/foreground.png').convert_alpha()]
        self.mg = [pg.image.load('assets/level_editor/images/midground.png').convert_alpha(), pg.image.load('assets/level_editor/images/midground.png').convert_alpha()]
        self.bg = [pg.image.load('assets/level_editor/images/background.png').convert_alpha(), pg.image.load('assets/level_editor/images/background.png').convert_alpha()]
        self.bgx = 0
        self.mgx = 0
        self.fgx = 0
        self.nxt_level_btn = Button(self, 200 * settings.SCALE, 730 * settings.SCALE, pg.image.load("assets/textures/next_level_btn.png"), "[NEXTLVL]", 1* settings.SCALE, 1* settings.SCALE)
        a = pg.image.load("assets/textures/restart_btn.png").get_width() * settings.SCALE
        self.restart_btn = Button(self, settings.WIDTH - a - (200 * settings.SCALE), 730 * settings.SCALE, pg.image.load("assets/textures/restart_btn.png"), "[NEXTLVL]", 1* settings.SCALE, 1* settings.SCALE)
        self.coin_icon = None
        self.collected_coins = []
        self.outro_fade = ScreenFade(self, (0,0,0), 5, 0)
        self.intro_fade = ScreenFade(self, (0,0,0), 5, 1)
        self.fo = False
        self.rnlm = False
        self.lt = 2
        self.fade_phase = 0
        self.finished_game = False
        self.end_anim = EndAnimation(self)
    def run(self):
        #self.MENU = MainMenu(self)
        #self.mixer.music.play(-1)
        self.load_level_data()
        self.SCREEN = pg.display.set_mode(RES)
        if FULL_SCREEN:
            self.SCREEN = pg.display.set_mode(RES, pg.FULLSCREEN)
        while self.running:
            self.CLOCK.tick(FPS)
            self.tick_buffer += (1 / 60) * self.delta_time
            if self.tick_buffer > 60:
                self.tick_buffer = 0
            kp = pg.key.get_pressed()
            
            if kp[pg.K_LCTRL] and kp[pg.K_v] and pyperclip.paste() != "None":
                if self.MENU.selected_box >= 0:
                    self.MENU.text_in_fields[self.MENU.selected_box] = pyperclip.paste()
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.running = False
                    self.client.running = False
                    pg.quit()
                    print("[QUIT GAME]")
                    if self.play_type == "online":
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
                if event.type == pg.KEYDOWN and event.key == pg.K_t and not settings.SHOW_MENU and self.play_type == "online":
                    self.typing = True
                if event.type == pg.KEYDOWN and event.key == pg.K_LEFT and not settings.SHOW_MENU and self.play_type == "online":
                    self.sn += 1
                    if self.sn >= len(self.players):
                        self.sn = 0
                if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT and not settings.SHOW_MENU and self.play_type == "online":
                    self.sn -= 1
                    if self.sn < 0:
                        self.sn = len(self.players) - 1
                if event.type == pg.KEYDOWN:
                    if self.MENU.selected_box >= 0:
                        if event.key == pg.K_BACKSPACE:
                            self.MENU.text_in_fields[self.MENU.selected_box] = self.MENU.text_in_fields[self.MENU.selected_box][:-1]
                        elif (len(self.MENU.text_in_fields[self.MENU.selected_box]) < 15 and self.MENU.selected_box == 0) or self.MENU.selected_box == 1:
                            self.MENU.text_in_fields[self.MENU.selected_box] += event.unicode
            self.set_delta_time()
            self.update()
            self.draw()
    def set_delta_time(self):
        now = time.time()
        self.delta_time = (now - self.prev_time) * FPS
        self.prev_time = now

    def update(self):
        if self.play_type == "online" and  len(self.client.players) > 1:
            self.enough_players = True
            self.player_num = self.client.num
        if settings.SHOW_MENU:
            if self.play_type == "online" and self.client.rsm:
                self.camera.pos[0] = 0
                self.level = self.client.lvl
                self.MENU.sop = True
            # if self.play_type == "online":
            #     self.client.send_msg("[GET_DATA]")
            self.MENU.update()
        else:
            if self.play_type == "online":
                if self.camera.spectating:
                    self.camera.tp = [self.players[self.sn][1], self.players[self.sn][2]]
                    self.camera.pos = [self.players[self.sn][1], self.players[self.sn][2]]
                change_in_keys = False
                for lmc in self.client.lmc:
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
                        if lmc[1] == "[3]":
                            self.level = lmc[2]
                            self.player.completed_level = True
                            self.rnlm = True
                            # self.load_level_data()
                            # self.check_point = [64 * 4, 16 * 64]
                            # self.player.respawn_animation()

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
            if self.MENU.sop:
                
                # if self.play_type == "offline":
                #         print('f')
                if self.outro_fade.fade():
                    self.fade_phase = 0
                    self.outro_fade = ScreenFade(self, (0,0,0), 5, 0)
                    self.load_level_data()
                    #self.play_type = "offline"
                    self.camera.pos[0] = 0
                    
                    settings.SHOW_MENU = False
                # else:
                #     if self.rnlm and not self.fo:
                #         if self.outro_fade.fade():
                #             self.fo = True
                #             self.outro_fade = ScreenFade(self, (0,0,0), 5, 0)
                #             self.load_level_data()
                #             self.check_point = [64 * 4, 16 * 64]
                #             self.player.respawn_animation()
            if self.end_anim.playing:
                if self.end_anim.update():
                    self.new_game()
        else:

            wo = []
            for go in self.game_objects:
                if go.type != 19:
                    go.update()
                    go.draw()
                else:
                    wo.append(go)
            self.player.draw()


            if self.play_type == "online":
                if self.MENU.sop:
                    if self.intro_fade.fade():
                        self.MENU.sop = False
                        self.intro_fade = ScreenFade(self, (0,0,0), 5, 1)
                #self.client.send_msg("[GET_DATA]")
                self.players = self.client.players
                p = self.player
                for op in self.players:
                    if op[0] != self.client.id and op[1] != "[QUIT]":
                        dx = (-self.camera.pos[0] + op[1] + self.camera.offset[0]) * settings.SCALE
                        dy = (-self.camera.pos[1] + op[2] + self.camera.offset[1]) * settings.SCALE
                        if op[3] == 0:
                            self.SCREEN.blit(self.player.left_sprites[int(op[4])], (dx, dy))
                        else:
                            self.SCREEN.blit(self.player.right_sprites[int(op[4])], (dx, dy))

                        self.text_to_screen(op[5], dx + 32 * settings.SCALE, dy - 20 * settings.SCALE, default_font, (0,0,0))
                        r1 = [p.pos[0], p.pos[1], p.coll_rect[2], p.coll_rect[3]]
                        r2 = [op[1], op[2], p.coll_rect[2], p.coll_rect[3]]
                        if r1[0] + r1[2] > r2[0] and r2[0] + r2[2] > r1[0] and r1[1] + r1[3] > r2[1] and r2[1] + r2[3] > r1[1]:
                            if r1[1] > r2[1]:
                                self.player.draw()
                    
                self.text_to_screen(self.name, self.player.draw_pos[0]* settings.SCALE + 32 * settings.SCALE, self.player.draw_pos[1] * settings.SCALE - 20 * settings.SCALE, default_font, (0,0,0))
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
                if self.camera.spectating:
                    self.text_to_screen("SPECTATING",self.SCREEN.get_width() / 2,30 ,pop_up_font, (0,0,0))
                    self.text_to_screen(str(self.players[self.sn][5]),self.SCREEN.get_width() / 2,70 ,pop_up_font, (0,0,0))
                if self.player.completed_level:
                    self.nxt_level_btn.draw()
                    self.restart_btn.draw()
                    if self.nxt_level_btn.check_click():
                        self.player.next_level()
                    if self.restart_btn.check_click():
                        self.player.respawn_animation()
            if self.coin_icon != None:
                self.SCREEN.blit(self.coin_icon, (20 * settings.SCALE, 20 * settings.SCALE))
                self.text_to_screen(str(self.player.collected_coins), 100 * settings.SCALE, 50 * settings.SCALE, coin_ui_font, (255,255,255))
            for go in wo:
                go.update()
                go.draw()
        if self.play_type == "offline":
            if self.player.completed_level and not self.fo:
                if self.level >= 8:
                    self.finished_game = True
                if self.outro_fade.fade():
                    self.fo = True
                    if self.finished_game:
                        self.MENU = MainMenu(self)
                        settings.SHOW_MENU = True
                        self.end_anim.playing = True
                    
                    self.outro_fade = ScreenFade(self, (0,0,0), 5, 0)
                    #if self.play_type == "offline":
                    self.player.next_level()

            if not self.player.completed_level and self.fo and not self.finished_game:
                if self.intro_fade.fade():
                    self.fo = False      
                    self.intro_fade = ScreenFade(self, (0,0,0), 5, 1) 
            if self.MENU.sop and not settings.SHOW_MENU:
                if self.intro_fade.fade():
                    self.MENU.sop = False
                    self.intro_fade = ScreenFade(self, (0,0,0), 5, 1) 
        else:
            if self.rnlm and not self.fo:
                if self.level >= 8:
                    self.finished_game = True
                if self.outro_fade.fade():
                    self.fo = True
                    if self.finished_game:
                        self.MENU = MainMenu(self)
                        settings.SHOW_MENU = True
                        self.end_anim.playing = True
                    if not self.finished_game:
                        self.outro_fade = ScreenFade(self, (0,0,0), 5, 0)
                        self.load_level_data()
                        self.check_point = [64 * 4, 16 * 64]
                        self.player.respawn_animation()

            if self.rnlm and self.fo and not self.finished_game:
                if self.intro_fade.fade():
                    self.fo = False    
                    self.rnlm = False  
                    self.intro_fade = ScreenFade(self, (0,0,0), 5, 1) 
            if self.MENU.sop and not settings.SHOW_MENU:
                if self.intro_fade.fade():
                    self.MENU.sop = False
                    self.intro_fade = ScreenFade(self, (0,0,0), 5, 1) 
        if self.play_type == "offline":
            if self.finished_game and self.end_anim.playing:
                if self.end_anim.update():
                    self.end_anim.playing = False

        pg.display.update()
    def load_level_data(self):
        if self.level < 9:
            img_list = []

            BLACK = (0,0,0)

            images = []
            tile_sheet = pg.image.load('assets/textures/brick_tile_sheet.png')
            w = tile_sheet.get_width()
            h = tile_sheet.get_height()
            tile_sheet = pg.transform.scale(tile_sheet, (w, h))
            TILE_SIZE = 64 
            t1 = get_image(tile_sheet,TILE_SIZE,TILE_SIZE,BLACK, 0, 0)
            t2 = get_image(tile_sheet,TILE_SIZE,TILE_SIZE,BLACK, 1, 0)
            t3 = get_image(tile_sheet,TILE_SIZE,TILE_SIZE,BLACK, 2, 0)
            t4 = get_image(tile_sheet,TILE_SIZE,TILE_SIZE,BLACK, 0, 1)
            t5 = get_image(tile_sheet,TILE_SIZE,TILE_SIZE,BLACK, 1, 1)
            t6 = get_image(tile_sheet,TILE_SIZE,TILE_SIZE,BLACK, 2, 1)
            t7 = get_image(tile_sheet,TILE_SIZE,TILE_SIZE,BLACK, 0, 2)
            t8 = get_image(tile_sheet,TILE_SIZE,TILE_SIZE,BLACK, 1, 2)
            t9 = get_image(tile_sheet,TILE_SIZE,TILE_SIZE,BLACK, 2, 2)

            t10 = get_image(tile_sheet,TILE_SIZE,TILE_SIZE,BLACK, 3, 0)
            t11 = get_image(tile_sheet,TILE_SIZE,TILE_SIZE,BLACK, 4, 0)
            t12 = get_image(tile_sheet,TILE_SIZE,TILE_SIZE,BLACK, 5, 0)
            t13 = get_image(tile_sheet,TILE_SIZE,TILE_SIZE,BLACK, 3, 1)
            t14 = get_image(tile_sheet,TILE_SIZE,TILE_SIZE,BLACK, 4, 1)
            t15 = get_image(tile_sheet,TILE_SIZE,TILE_SIZE,BLACK, 5, 1)
            t16 = get_image(tile_sheet,TILE_SIZE,TILE_SIZE,BLACK, 3, 2)
            t17 = get_image(tile_sheet,TILE_SIZE,TILE_SIZE,BLACK, 4, 2)
            t18 = get_image(tile_sheet,TILE_SIZE,TILE_SIZE,BLACK, 5, 2)
            t19 = get_image(tile_sheet,TILE_SIZE,TILE_SIZE,BLACK, 6, 0)
            t20 = get_image(tile_sheet,TILE_SIZE,TILE_SIZE,BLACK, 6, 1)
            t21 = get_image(tile_sheet,TILE_SIZE,TILE_SIZE,BLACK, 6, 2)

            t22 = get_image(tile_sheet,TILE_SIZE,TILE_SIZE,BLACK, 7, 0)
            t23 = pg.transform.rotate(t22, 90 % 360)
            t24 = pg.transform.rotate(t22, 180 % 360)
            t25 = pg.transform.rotate(t22, 270 % 360)
            t26 = get_image(tile_sheet,TILE_SIZE,TILE_SIZE,BLACK, 8, 0)
            self.coin_icon = pg.transform.scale(t26, (64 * settings.SCALE, 64 * settings.SCALE))
            t26 = pg.transform.scale(t26, (32 * settings.SCALE, 32 * settings.SCALE))
            t27 = get_image(tile_sheet,64,64,BLACK, 8, 1)
            t28 = get_image(tile_sheet,64,64,BLACK, 9, 0)
            t29 = get_image(tile_sheet,64,64,BLACK, 10, 0)
            t30 = get_image(tile_sheet,64,64,(255,255,255), 9, 2)
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
            images.append(t21)
            images.append(t22)
            images.append(t23)
            images.append(t24)
            images.append(t25)
            images.append(t26)
            images.append(t27)
            images.append(t28)
            images.append(t29)
            images.append(t30)
            for i in range(len(images)):
                if i == 25:
                    img = pg.transform.scale(images[i], (32 * settings.SCALE, 32 * settings.SCALE))
                    images[i] = img
                else:
                    img = pg.transform.scale(images[i], (64 * settings.SCALE, 64 * settings.SCALE))
                    images[i] = img
            self.game_objects = []

            TILE_SPACING = 64

            with open(os.path.join(f'levels_{self.lt}',f'level{self.level}_data.csv'), newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter = ',')
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        if int(tile) >= 0:
                            if int(tile) < 9:
                                if int(tile) < 6:
                                    self.game_objects.append(GameObject(self, [TILE_SPACING * y, TILE_SPACING * x], [images[int(tile)]], True, int(tile), True, [0,0]))
                                else:
                                    self.game_objects.append(GameObject(self, [TILE_SPACING * y, TILE_SPACING * x], [images[int(tile)]], True, int(tile), False, [0,0]))
                            elif int(tile) >= 9 and int(tile) < 19:
                                self.game_objects.append(GameObject(self, [TILE_SPACING * y, TILE_SPACING * x], [images[int(tile)]], False, int(tile), True, [0,0]))
                            if int(tile) >= 9 < 18:
                                self.in_game_keys.append([TILE_SPACING * y, TILE_SPACING * x, int(tile)])
                            if int(tile) == 19:
                                self.game_objects.append(GameObject(self, [TILE_SPACING * y, TILE_SPACING * x + 1], [images[0],images[1],images[2],images[3],images[4],images[5],images[6],images[7],images[8]], False, int(tile), True, [0,0]))
                            if int(tile) == 20:
                                self.game_objects.append(GameObject(self, [TILE_SPACING * y, TILE_SPACING * x], [images[int(tile)], get_image(tile_sheet,64,64,BLACK, 7, 2)], False, int(tile), True, [0,0]))
                            if int(tile) >= 21 and int(tile) < 25:

                                self.game_objects.append(GameObject(self, [TILE_SPACING * y, TILE_SPACING * x + 1], [images[int(tile)]], False, int(tile), True, [0,0]))
                            if int(tile) == 25:
                                ac = False
                                for i in self.collected_coins:
                                    if [TILE_SPACING * y,TILE_SPACING * x] == i:
                                        print("CLEARED COIN")
                                        ac = True
                                if not ac:
                                    self.game_objects.append(GameObject(self, [TILE_SPACING * y, TILE_SPACING * x], [images[int(tile)]], False, int(tile), True, [0,0]))
                            if int(tile) == 26:
                                self.game_objects.append(GameObject(self, [TILE_SPACING * y, TILE_SPACING * x], [images[int(tile)]], False, int(tile), True, [0,0]))
                            if int(tile) == 27:
                                self.game_objects.append(GameObject(self, [TILE_SPACING * y, TILE_SPACING * x], [images[int(tile)]], True, int(tile), True, [3,0]))
                            if int(tile) == 28:
                                self.game_objects.append(GameObject(self, [TILE_SPACING * y, TILE_SPACING * x], [images[int(tile)]], True, int(tile), True, [0,3]))
                            if int(tile) == 29:
                                self.game_objects.append(GameObject(self, [TILE_SPACING * y, TILE_SPACING * x], [images[int(tile)]], True, int(tile), True, [0,0]))
        else:
            self.finished_game = True

    def text_objects(self, txt, f, c):
        txt_surf = f.render(txt, True, c)
        return txt_surf, txt_surf.get_rect()
    def text_to_screen(self, txt, cx, cy, f, c):
        text_surf, text_rect = self.text_objects(txt, f, c)
        text_rect.center = (cx), (cy)
        self.SCREEN.blit(text_surf, text_rect)
    def clear_screen(self):
        WHITE = (255,255,255)
        if settings.SHOW_MENU:
            self.camera.pos[0] += 2
        if True:
            self.bgx = -self.camera.pos[0] * 0.1
            self.mgx = -self.camera.pos[0] * 0.2
            self.fgx = -self.camera.pos[0] * 0.4
            self.SCREEN.fill((197, 239, 250))
            for i in range(len(self.bg)):
                bgi = self.bg[i]
                w = bgi.get_width()
                x = self.bgx + w * i
                y = self.SCREEN.get_height() - bgi.get_height() - 100
                if x + w > 0:
                    self.SCREEN.blit(bgi, (x, y))
            for i in range(len(self.mg)):
                w = bgi.get_width()
                bgi = self.mg[i]
                x = self.mgx + w * i 
                y = self.SCREEN.get_height() - bgi.get_height() - 0
                if x + w > 0:
                    self.SCREEN.blit(bgi, (x, y))
            for i in range(len(self.fg)):
                w = bgi.get_width()
                bgi = self.fg[i]
                x = self.fgx + w * i
                y = self.SCREEN.get_height() - bgi.get_height()
                if x + w > 0:
                    self.SCREEN.blit(bgi, (x, y))
            if self.bgx + self.bg[0].get_width() * len(self.bg) < self.SCREEN.get_width():
                self.bg.append(self.bg[0])
            if self.mgx + self.mg[0].get_width() * len(self.mg) < self.SCREEN.get_width():
                self.mg.append(self.mg[0])
            if self.fgx + self.fg[0].get_width() * len(self.fg) < self.SCREEN.get_width():
                self.fg.append(self.fg[0])
    def check_buttons(self):
        pass