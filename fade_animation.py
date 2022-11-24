import pygame as pg
import settings
screen = 0
SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0
# class Screenfade():
# 	def __init__(self, direction, colour, speed):
# 		self.direction = direction
# 		self.colour = colour
# 		self.speed = speed
# 		self.fade_counter = 0


# 	def fade(self):
# 		fade_complete = False
# 		self.fade_counter += self.speed
# 		if self.direction == 1:#whole screen fade
# 			pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
# 			pygame.draw.rect(screen, self.colour, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
# 			pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
# 			pygame.draw.rect(screen, self.colour, (0, SCREEN_HEIGHT // 2 +self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
# 		if self.direction == 2:#vertical screen fade down
# 			pygame.draw.rect(screen, self.colour, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
# 		if self.fade_counter >= SCREEN_WIDTH:
# 			fade_complete = True

# 		return fade_complete
class ScreenFade:
    def __init__(self, game, colour, speed, num):
        self.GAME = game
        self.colour = colour
        self.speed = speed * settings.SCALE
        self.fc = 0
        self.num = num

        if self.num == 0:
            self.fc = settings.WIDTH / 2
        
    def fade(self):
        fade_complete = False
        if self.num == 0:
            #print(self.fc)
            self.fc -= self.speed * self.GAME.delta_time
        else:
            self.fc += self.speed * self.GAME.delta_time
        pg.draw.rect(self.GAME.SCREEN, self.colour, (0 - self.fc, 0, settings.WIDTH // 2, settings.HEIGHT))
        pg.draw.rect(self.GAME.SCREEN, self.colour, (settings.WIDTH // 2 + self.fc, 0, settings.WIDTH, settings.HEIGHT))
        pg.draw.rect(self.GAME.SCREEN, self.colour, (0, 0 - self.fc, settings.WIDTH, settings.HEIGHT // 2))
        pg.draw.rect(self.GAME.SCREEN, self.colour, (0, settings.HEIGHT // 2 + self.fc, settings.WIDTH, settings.HEIGHT))
        pg.display.update()
        if self.fc >= settings.WIDTH or self.fc < 0:
            fade_complete = True
        return fade_complete