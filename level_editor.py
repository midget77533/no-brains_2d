import pygame
from assets.level_editor import button
import csv
import pickle
import os

pygame.init()

clock = pygame.time.Clock()
FPS = 60

#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')


#define game variables
ROWS = 20
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 30
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1


#load images
pine1_img = pygame.image.load('assets/level_editor/images/pine1.png').convert_alpha()
pine2_img = pygame.image.load('assets/level_editor/images/pine2.png').convert_alpha()
mountain_img = pygame.image.load('assets/level_editor/images/mountain.png').convert_alpha()
mountain_img.set_colorkey((0,0,0))
sky_img = pygame.image.load('assets/level_editor/images/sky_cloud.png').convert_alpha()

img_list = []

BLACK = (0,0,0)

def get_image(sheet, width, height,color, col, row):
    img = pygame.Surface((width, height))
    img.blit(sheet, (0,0), ((col * width),(row * height),width,height))
    img.set_colorkey(color)
    return img

images = []
tile_sheet = pygame.image.load('assets/textures/brick_tile_sheet.png').convert_alpha()


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
images.append(t18)
images.append(t19)

for x in range(len(images)):
	img = pygame.transform.scale(images[x], (TILE_SIZE, TILE_SIZE))
	img_list.append(img)



save_img = pygame.image.load('assets/level_editor/images/save_btn.png').convert_alpha()
load_img = pygame.image.load('assets/level_editor/images/load_btn.png').convert_alpha()


GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

font = pygame.font.SysFont('Futura', 30)

world_data = []
for row in range(ROWS):
	r = [-1] * MAX_COLS
	world_data.append(r)


def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


def draw_bg():
	screen.fill(GREEN)
	width = sky_img.get_width()
	for x in range(4):
		screen.blit(sky_img, ((x * width) - scroll * 0.5, 0))
		screen.blit(mountain_img, ((x * width) - scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
		screen.blit(pine1_img, ((x * width) - scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
		screen.blit(pine2_img, ((x * width) - scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

def draw_grid():
	for c in range(MAX_COLS + 1):
		pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
	for c in range(ROWS + 1):
		pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))

def draw_world():
	global gt26, gt27, gt28, gt29, gt30
	for y, row in enumerate(world_data):
		for x, tile in enumerate(row):
			if tile >= 0:
				screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))
def auto_make():
	for y, row in enumerate(world_data):
		for x, tile in enumerate(row):
			if tile == 7 and y != 0 and x != 0 and y < 19 and x < 150:
				if world_data[y - 1][x] == -1:
					world_data[y][x] = 1
				if world_data[y - 1][x] == -1 and world_data[y][x - 1] == -1:
					world_data[y][x] = 0
				if world_data[y - 1][x] == -1 and world_data[y][x + 1] == -1:
					world_data[y][x] = 2
				if world_data[y][x - 1] == -1 and world_data[y - 1][x] != -1:
					world_data[y][x] = 3
				if world_data[y][x + 1] == -1 and world_data[y - 1][x] != -1:
					world_data[y][x] = 5
				if (world_data[y - 1][x] == 3 or world_data[y - 1][x] == 7) and world_data[y + 1][x] == -1 and world_data[y][x - 1] == -1:
					world_data[y][x] = 6
				if (world_data[y - 1][x] == 2 or world_data[y - 1][x] == 7) and world_data[y + 1][x] == -1 and world_data[y][x + 1] == -1:
					world_data[y][x] = 8
				



save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)

button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
	tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
	button_list.append(tile_button)
	button_col += 1
	if button_col == 3:
		button_row += 1
		button_col = 0


run = True
while run:

	clock.tick(FPS)

	draw_bg()
	draw_grid()
	draw_world()
	kp = pygame.key.get_pressed()
	if kp[pygame.K_p]:
		auto_make()

	draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
	
	if save_button.draw(screen):
		with open(os.path.join('levels',f'level{level}_data.csv'), 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			for row in world_data:
				writer.writerow(row)
	if load_button.draw(screen):
		scroll = 0
		with open(os.path.join('levels',f'level{level}_data.csv'), newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					world_data[x][y] = int(tile)
				

	#draw tile panel and tiles
	pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

	#choose a tile
	button_count = 0
	for button_count, i in enumerate(button_list):
		if i.draw(screen):
			current_tile = button_count

	#highlight the selected tile
	pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

	#scroll the map
	if scroll_left == True and scroll > 0:
		scroll -= 5 * scroll_speed
	if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
		scroll += 5 * scroll_speed

	#add new tiles to the screen
	#get mouse position
	pos = pygame.mouse.get_pos()
	x = (pos[0] + scroll) // TILE_SIZE
	y = pos[1] // TILE_SIZE

	#check that the coordinates are within the tile area
	if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
		#update tile value
		if pygame.mouse.get_pressed()[0] == 1:
			if world_data[y][x] != current_tile:
				world_data[y][x] = current_tile
		if pygame.mouse.get_pressed()[2] == 1:
			world_data[y][x] = -1


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		#keyboard presses
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			if event.key == pygame.K_DOWN and level > 0:
				level -= 1
			if event.key == pygame.K_LEFT:
				scroll_left = True
			if event.key == pygame.K_RIGHT:
				scroll_right = True
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 5


		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				scroll_left = False
			if event.key == pygame.K_RIGHT:
				scroll_right = False
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 1


	pygame.display.update()

pygame.quit()