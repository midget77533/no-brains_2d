import pygame as pg
from settings import *
from game import *

class GameEngine:
    def __init__(self):
        self.GAME = Game()
    def start(self):
        self.GAME.new_game()
        self.GAME.run()

