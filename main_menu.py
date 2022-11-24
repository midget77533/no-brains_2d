from tkinter import S
import pygame as pg
from settings import *
import time
import settings
import threading
from buttons import *
from networking import *
pg.init()

default_font = pg.font.Font('assets/fonts/poppins/Poppins-bold.ttf', int(100 * settings.SCALE))
lable_font = pg.font.Font('assets/fonts/poppins/Poppins-bold.ttf', int(50 * settings.SCALE))
txt_field_font = pg.font.Font('assets/fonts/poppins/Poppins-bold.ttf', int(25 * settings.SCALE))
caption_font = pg.font.Font('assets/fonts/poppins/Poppins-bold.ttf', int(15 * settings.SCALE))
lvl_select_font = pg.font.Font('assets/fonts/poppins/Poppins-bold.ttf', int(80 * settings.SCALE))
class MainMenu:
    def __init__(self, game):
        self.GAME = game
        self.title = {"text": settings.TITLE, "x": 0, "y": 0, "color":(0,0,0),"font": default_font}
        self.buttons = [
            Button(self.GAME, 0, 250 * settings.SCALE, pg.image.load("assets/textures/start_btn.png"), "[START]", 1 * settings.SCALE,1 * settings.SCALE), 
            Button(self.GAME, 0, 450 * settings.SCALE, pg.image.load("assets/textures/options_btn.png"), "[SETTINGS]", 1* settings.SCALE,1* settings.SCALE),
            Button(self.GAME, 0, 650 * settings.SCALE, pg.image.load("assets/textures/quit_btn.png"), "[QUIT]",1* settings.SCALE, 1* settings.SCALE)
        ]
        self.lobby_btns = [
            Button(self.GAME, 750 * settings.SCALE, 610 * settings.SCALE, pg.image.load("assets/textures/create_room_btn.png"), "[CREATE]", 1* settings.SCALE, 1* settings.SCALE), 
            Button(self.GAME, 1050 * settings.SCALE, 610 * settings.SCALE, pg.image.load("assets/textures/join_room_btn.png"), "[JOIN]", 1* settings.SCALE, 1* settings.SCALE),
        ]
        self.back_btn = Button(self.GAME, 15 * settings.SCALE, 10 * settings.SCALE, pg.image.load("assets/textures/back_btn.png"), "[BACK]", 1* settings.SCALE, 1* settings.SCALE)
        for btn in self.buttons:
            btn = self.center_button_x(btn, self.GAME.SCREEN.get_width() / 2)
        self.spb = Button(self.GAME, 370 * settings.SCALE , 300 * settings.SCALE, pg.image.load("assets/textures/single_player_btn.png"), "[SINGLE_PLAYER]", 1* settings.SCALE, 1* settings.SCALE)
        self.mpb = Button(self.GAME, 870 * settings.SCALE, 300 * settings.SCALE, pg.image.load("assets/textures/multi_player_btn.png"), "[MULTI_PLAYER]", 1* settings.SCALE, 1* settings.SCALE)
        self.play_btn = Button(self.GAME, 1050 * settings.SCALE, 610 * settings.SCALE, pg.image.load("assets/textures/play_btn.png"), "[PLAY]", 1* settings.SCALE, 1* settings.SCALE)
        self.page = "main_menu"
        self.text_fields = [pg.Rect(330 * settings.SCALE, 300 * settings.SCALE, 410 * settings.SCALE, 60 * settings.SCALE), pg.Rect(330 * settings.SCALE, 550 * settings.SCALE, 410 * settings.SCALE, 60 * settings.SCALE)]
        self.text_in_fields = ['', socket.gethostbyname(socket.gethostname())]
        self.selected_box = -1
        self.bbtn_destination = "main_menu"
        self.players = []
        x = 550
        y = 250 
        self.lvl_buttons = [
            Button(self.GAME, x * settings.SCALE, y * settings.SCALE, pg.image.load("assets/textures/lvl_buttons/lvl_button_1.png"), "[LVL|1]", 1 * settings.SCALE,1 * settings.SCALE),
            Button(self.GAME, (x + 128 * 1.5) * settings.SCALE, y * settings.SCALE, pg.image.load("assets/textures/lvl_buttons/lvl_button_2.png"), "[LVL|2]", 1 * settings.SCALE,1 * settings.SCALE),
            Button(self.GAME, (x + 128 * 3) * settings.SCALE, y * settings.SCALE, pg.image.load("assets/textures/lvl_buttons/lvl_button_3.png"), "[LVL|3]", 1 * settings.SCALE,1 * settings.SCALE),
            Button(self.GAME,  x * settings.SCALE, (y + 128 * 1.5) * settings.SCALE, pg.image.load("assets/textures/lvl_buttons/lvl_button_4.png"), "[LVL|4]", 1 * settings.SCALE,1 * settings.SCALE),
            Button(self.GAME, (x + 128 * 1.5) * settings.SCALE, (y + 128 * 1.5) * settings.SCALE, pg.image.load("assets/textures/lvl_buttons/lvl_button_5.png"), "[LVL|5]", 1 * settings.SCALE,1 * settings.SCALE),
            Button(self.GAME, (x + 128 * 3) * settings.SCALE, (y + 128 * 1.5) * settings.SCALE, pg.image.load("assets/textures/lvl_buttons/lvl_button_6.png"), "[LVL|6]", 1 * settings.SCALE,1 * settings.SCALE),
            Button(self.GAME, x * settings.SCALE, (y + 128 * 3) * settings.SCALE, pg.image.load("assets/textures/lvl_buttons/lvl_button_7.png"), "[LVL|7]", 1 * settings.SCALE,1 * settings.SCALE),
            Button(self.GAME, (x + 128 * 1.5) * settings.SCALE, (y + 128 * 3) * settings.SCALE, pg.image.load("assets/textures/lvl_buttons/lvl_button_8.png"), "[LVL|8]", 1 * settings.SCALE,1 * settings.SCALE),
            Button(self.GAME, (x + 128 * 3) * settings.SCALE, (y + 128 * 3) * settings.SCALE, pg.image.load("assets/textures/lvl_buttons/lvl_button_9.png"), "[LVL|9]", 1 * settings.SCALE,1 * settings.SCALE),
        ]
        self.sop = False
        self.SERVER = None
    def update(self):
        mouse_pressed = pg.mouse.get_pressed()
        self.players = self.GAME.players
        if mouse_pressed[0]:
            x,y = pg.mouse.get_pos()
            if self.text_fields[0].collidepoint(x,y):
                self.selected_box = 0
            elif self.text_fields[1].collidepoint(x,y):
                self.selected_box = 1
            else:
                self.selected_box = -1
        # for event in pg.event.get():
        #     if event.type == pg.KEYDOWN:
        if self.page == "main_menu":
            for btn in self.buttons:
                if btn.check_click():
                    if btn.name == '[START]':
                        self.bbtn_destination = self.page
                        self.page = "choice_menu"
                        break
                    if btn.name == '[QUIT]':
                        self.GAME.running = False
                        break
        if self.page == "choice_menu":
            self.bbtn_destination = "main_menu"
            if self.mpb.check_click():
                self.bbtn_destination = self.page
                self.page = "server_menu"
                
            if self.spb.check_click():
                self.bbtn_destination = self.page
                self.page = "single_player_options"
                # settings.SHOW_MENU = False
                # self.bbtn_destination = self.page
                # self.GAME.play_type = "offline"
                # self.GAME.camera.pos[0] = 0
        if self.page == "lobby_menu":
            #if len(self.players) > 0:
            self.GAME.enough_players
            if self.GAME.enough_players and self.SERVER != None:
                if self.play_btn.check_click():
                    self.bbtn_destination = self.page
                    self.page = "multi_player_options"
        if self.page == "server_menu":
            self.bbtn_destination = "choice_menu"
            for btn in self.lobby_btns:
                if btn.check_click():

                    if btn.name == '[CREATE]':
                        self.create_game()
                        break
                    if btn.name == '[JOIN]':
                        self.join_game()
                        break
        if self.page == "single_player_options":
            for btn in self.lvl_buttons:
                if btn.check_click():
                    lvl = btn.name.split("|")
                    lvl = lvl[1].split("]")
                    lvl = int(lvl[0]) - 1
                    self.GAME.play_type = "offline"
                    
                    self.bbtn_destination = self.page
                    self.GAME.level = lvl
                    self.GAME.lt = 1
                    self.sop = True
        if self.page == "multi_player_options":
            for btn in self.lvl_buttons:
                if btn.check_click():
                    lvl = btn.name.split("|")
                    lvl = lvl[1].split("]")
                    lvl = int(lvl[0]) - 1
                    
                    self.bbtn_destination = self.page
                    self.GAME.level = lvl
                    self.SERVER.current_level = lvl
                    self.sop = True
                    self.GAME.client.send_msg(["[PLAY]", lvl])
                    self.GAME.camera.pos[0] = 0
                    self.GAME.lt = len(self.GAME.players)
                    print(self.SERVER.current_level)


    def draw(self):
        if self.page == "main_menu":
            self.text_to_screen()
            for btn in self.buttons:
                btn.draw()
        elif self.page != "lobby_menu":
            self.back_btn.draw()
            if self.back_btn.check_click():
                self.page = self.bbtn_destination

        if self.page == "server_menu":
            a = self.GAME.SCREEN.get_width() 
            b = self.GAME.SCREEN.get_height()
            pg.draw.rect(self.GAME.SCREEN, (90,90,90), [(a / 2 - (a / 1.5) / 2) , (b / 2 - (b / 1.5) / 2) , (a / 1.5) , (b / 1.5) ])
            self.render_text("NAME:", 320 * settings.SCALE, 200 * settings.SCALE, False, lable_font)
            self.render_text("SERVER:", 320 * settings.SCALE, 450 * settings.SCALE, False, lable_font)
            self.render_text("*maximum 15 characters", 350 * settings.SCALE, 270 * settings.SCALE, False, caption_font)
            self.render_text("*only required if joining server", 350 * settings.SCALE, 520 * settings.SCALE, False, caption_font)
            pg.draw.rect(self.GAME.SCREEN, (50,50,50), self.text_fields[0])
            pg.draw.rect(self.GAME.SCREEN, (50,50,50), self.text_fields[1])
            s1 = txt_field_font.render(self.text_in_fields[0], True, (0,0,0))
            s2 = txt_field_font.render(self.text_in_fields[1], True, (0,0,0))
            self.GAME.SCREEN.blit(s1, (self.text_fields[0].x + 10 * settings.SCALE, self.text_fields[0].y + 15 * settings.SCALE))
            self.GAME.SCREEN.blit(s2, (self.text_fields[1].x + 10 * settings.SCALE, self.text_fields[1].y + 15 * settings.SCALE))
            for btn in self.lobby_btns:
                btn.draw()
        if self.page == "lobby_menu":
            a = self.GAME.SCREEN.get_width() 
            b = self.GAME.SCREEN.get_height()
            pg.draw.rect(self.GAME.SCREEN, (90,90,90), [(a / 2 - (a / 1.5) / 2) , (b / 2 - (b / 1.5) / 2) , (a / 1.5) , (b / 1.5)])
            self.render_text("PLAYERS", 320 * settings.SCALE, 200 * settings.SCALE, False, lable_font)
            for i in range(len(self.players)):
                pn = self.players[i][5]
                pg.draw.rect(self.GAME.SCREEN, (30,30,30), [340 * settings.SCALE, (290 + i * 120) * settings.SCALE, 500 * settings.SCALE, 70 * settings.SCALE])
                self.render_text(pn, 350 * settings.SCALE, (310 + i * 120) * settings.SCALE, False, txt_field_font)
            if self.GAME.enough_players and self.SERVER != None:
                self.play_btn.draw()
        if self.page == "choice_menu":
            self.spb.draw()
            self.mpb.draw()
        if self.page == "single_player_options":
            self.render_text("LEVEL SELECT", self.GAME.SCREEN.get_width() / 2, 80, True, lvl_select_font, (0,0,0))
            for btn in self.lvl_buttons:
                btn.draw()
        if self.page == "multi_player_options":
            self.render_text("LEVEL SELECT", self.GAME.SCREEN.get_width() / 2, 80, True, lvl_select_font, (0,0,0))
            for btn in self.lvl_buttons:
                btn.draw()
    def text_objects(self):
        txt_surf = self.title["font"].render(self.title["text"], True, self.title["color"])
        return txt_surf, txt_surf.get_rect()
    def text_to_screen(self):
        text_surf, text_rect = self.text_objects()
        text_rect.center = (self.GAME.SCREEN.get_width() / 2), (100 * settings.SCALE)
        self.GAME.SCREEN.blit(text_surf, text_rect)
    def get_txt_obj(self, text, fnt, col):
        txt_surf = fnt.render(text, True, col)
        return txt_surf, txt_surf.get_rect()
    def render_text(self,txt, x, y, c, fnt, col=(255,255,255)):
        if c:
            text_surf, text_rect = self.get_txt_obj(txt, fnt, col)
            text_rect.center = (x), (y)
            self.GAME.SCREEN.blit(text_surf, text_rect)
        else:
            text_surf, text_rect = self.get_txt_obj(txt, fnt, col)
            text_rect.x = x
            text_rect.y = y
            self.GAME.SCREEN.blit(text_surf, text_rect)
    def create_game(self):
        self.bbtn_destination = self.page
        self.page = "lobby_menu"
        SERVER = socket.gethostbyname(socket.gethostname())
        PORT = 12345
        self.GAME.client = Client(SERVER, PORT)
        self.SERVER  = Server(SERVER, PORT, self.GAME)
        s = threading.Thread(target=self.SERVER.start)
        s.start()
        self.GAME.client.run()
        self.GAME.name = self.text_in_fields[0]
        self.GAME.client.send_msg(["[INIT]", self.GAME.name])
        self.GAME.play_type = "online"
        
        print("[START]")
    def join_game(self):
        self.page = "lobby_menu"
        SERVER = self.text_in_fields[1]
        PORT = 12345
        self.GAME.client = Client(SERVER, PORT)
        self.GAME.client.run()
        self.GAME.name = self.text_in_fields[0]
        self.GAME.client.send_msg(["[INIT]", self.GAME.name])
        self.GAME.play_type = "online"
        print("[START]")
    def on_mouse_press(self):
        self.start_game()
    def center_button_x(self, button ,csx):
        cx = int(csx - button.rect[2] / 2)
        button.rect.x = cx
        return button