from tkinter import S
import pygame as pg
from settings import *
import time
import settings
import threading
from buttons import *
pg.init()

default_font = pg.font.Font('assets/fonts/poppins/Poppins-bold.ttf', 100)

class MainMenu:
    def __init__(self, game):
        self.GAME = game
        self.title = {"text": "Z-RUSH", "x": 0, "y": 0, "color":(0,0,0),"font": default_font}
        self.buttons = [
            Button(self.GAME, 0, 250, pg.image.load("assets/textures/start_btn.png"), "[START]", .5), 
            Button(self.GAME, 0, 450, pg.image.load("assets/textures/start_btn.png"), "[SETTINGS]", .5),
            Button(self.GAME, 0, 650, pg.image.load("assets/textures/start_btn.png"), "[QUIT]", .5)
        ]
        for btn in self.buttons:
            btn = self.center_button_x(btn, self.GAME.SCREEN.get_width() / 2)
    def update(self):
        for btn in self.buttons:
            if btn.check_click():
                if btn.name == '[START]':
                    self.start_game()
                    break
                if btn.name == '[QUIT]':
                    self.GAME.running = False
                    break
    def draw(self):
        self.text_to_screen()
        for btn in self.buttons:
            btn.draw()
    def text_objects(self):
        txt_surf = self.title["font"].render(self.title["text"], True, self.title["color"])
        return txt_surf, txt_surf.get_rect()
    def text_to_screen(self):
        text_surf, text_rect = self.text_objects()
        text_rect.center = (self.GAME.SCREEN.get_width() / 2), (100)
        self.GAME.SCREEN.blit(text_surf, text_rect)
    def start_game(self):
        settings.SHOW_MENU = False
        t = threading.Thread(target=self.GAME.client.run(), args=())
        t.start()
        self.GAME.client.send_msg(["[INIT]", self.GAME.name])
        self.GAME.client_made = True
        print("[START]")
    def on_mouse_press(self):
        self.start_game()
    def center_button_x(self, button ,csx):
        cx = int(csx - button.rect[2] / 2)
        button.rect.x = cx
        return button