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
        self.mc = 0
        self.r = 255
        self.g = 0
        self.b = 0
        self.shift_speed = 5
        if self.num == 0:
            self.fc = settings.WIDTH / 2
        
    def fade(self):
        if self.GAME.finished_game:
            if self.mc == 0:
                self.g += self.shift_speed
            if self.mc == 1:
                self.r -= self.shift_speed
            if self.mc == 2:
                self.b += self.shift_speed
            if self.mc == 3:
                self.g -= self.shift_speed
            if self.mc == 4:
                self.r += self.shift_speed
            if self.mc == 5:
                self.b -= self.shift_speed
            if self.r >= 255 and self.g <= 0 and self.b <= 0:
                self.mc = 0
            if self.r >= 255 and self.g >= 255:
                self.mc = 1
            if self.g >= 255 and self.r <= 0:
                self.mc = 2
            if self.g >= 255 and self.b >= 255:
                self.mc = 3
            if self.b >= 255 and self.r <= 0 and self.g <= 0:
                self.mc = 4
            if self.r >= 255 and self.b >= 255:
                self.mc = 5
            if self.r < 0:
                self.r = 0
            if self.g < 0:
                self.g = 0
            if self.b < 0:
                self.b = 0
            if self.r > 255:
                self.r = 255
            if self.g > 255:
                self.g = 255
            if self.b > 255:
                self.b = 255
            self.colour = (self.r, self.g, self.b)
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