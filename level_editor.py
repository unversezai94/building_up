import pygame
import pickle
from os import path


pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
tile_size = 40
cols = 20
margin = 100
screen_width = tile_size * cols
screen_height = (tile_size * cols) + margin

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Level Editor')


#load images
toprak = pygame.image.load('resimler/toprak.png')
toprak_resim = pygame.transform.smoothscale(toprak, (tile_size, tile_size))
yer_orta = pygame.image.load('resimler/yer_orta.png')
yer_orta = pygame.transform.smoothscale(yer_orta, (screen_width, screen_height - margin))
yer_sol = pygame.image.load('resimler/yer_sol.png')
yer_sol = pygame.transform.smoothscale(yer_sol, (screen_width, screen_height - margin))
yer_sag = pygame.image.load('resimler/yer_sag.png')
yer_sag = pygame.transform.smoothscale(yer_sag, (screen_width, screen_height - margin))
yer_tek = pygame.image.load('resimler/yer_tek.png')
yer_tek = pygame.transform.smoothscale(yer_tek, (screen_width, screen_height - margin))
dusman_resim = pygame.image.load('resimler/dusman_0.png')
diken_resim = pygame.image.load('resimler/diken_0.png')
cikis_resim = pygame.image.load('resimler/cikis_kapisi.png')
kaydet_resim = pygame.image.load('resimler/kaydet.png')
yukle_resim = pygame.image.load('resimler/yukle.png')
arkaplan = pygame.image.load('resimler/arkaplan.png')
disket_resim = pygame.image.load('resimler/disket_0.png')
klavye_resim = pygame.image.load('resimler/klavye_0.png')
gitar_resim = pygame.image.load('resimler/gitar_0.png')
bateri_resim = pygame.image.load('resimler/bateri_0.png')


#define game variables
clicked = False
level = 1

#define colours
white = (255, 255, 255)
green = (144, 201, 120)

font = pygame.font.SysFont('Futura', 24)

#create empty tile list
world_data = []
for row in range(20):
	r = [0] * 20
	world_data.append(r)

#create boundary
for tile in range(0, 20):
	world_data[19][tile] = 2
	world_data[0][tile] = 1
	world_data[tile][0] = 1
	world_data[tile][19] = 1

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_grid():
	for c in range(21):
		#vertical lines
		pygame.draw.line(screen, white, (c * tile_size, 0), (c * tile_size, screen_height - margin))
		#horizontal lines
		pygame.draw.line(screen, white, (0, c * tile_size), (screen_width, c * tile_size))


def draw_world():
	for row in range(20):
		for col in range(20):
			if world_data[row][col] > 0:
				if world_data[row][col] == 1:
					#dirt blocks
					img = pygame.transform.smoothscale(toprak_resim, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))

				if world_data[row][col] == 2:
					#grass blocks
					img = pygame.transform.smoothscale(yer_orta, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 3:
					#grass blocks
					img = pygame.transform.smoothscale(yer_sol, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 4:
					#grass blocks
					img = pygame.transform.smoothscale(yer_sag, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 5:
					#grass blocks
					img = pygame.transform.smoothscale(yer_tek, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
                
				if world_data[row][col] == 6:
					#enemy blocks
					img = pygame.transform.smoothscale(dusman_resim, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size ))
				
				if world_data[row][col] == 7:
					
					img = pygame.transform.smoothscale(diken_resim, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))
				
				if world_data[row][col] == 8:
					#exit
					img = pygame.transform.smoothscale(cikis_resim, (int(tile_size* 1.6), int(tile_size * 1.6)))
					screen.blit(img, (col * tile_size + 8, row * tile_size - (tile_size // 2) - 4 ))

				if world_data[row][col] == 9:
					img = pygame.transform.smoothscale(disket_resim, ((25 , 25)))
					screen.blit(img, (col * tile_size + (tile_size // 2) - 12 , row * tile_size + (tile_size // 2) - 12))
				if world_data[row][col] == 10:
					img = pygame.transform.smoothscale(klavye_resim, ((40 , 40)))
					screen.blit(img, (col * tile_size, row * tile_size ))
				if world_data[row][col] == 11:
					img = pygame.transform.smoothscale(gitar_resim, ((40 , 40)))
					screen.blit(img, (col * tile_size, row * tile_size ))
				if world_data[row][col] == 12:
					img = pygame.transform.smoothscale(bateri_resim, ((40 , 40)))
					screen.blit(img, (col * tile_size, row * tile_size ))



class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action

#create load and save buttons
save_button = Button(screen_width // 2 - 150, screen_height - 80, kaydet_resim)
load_button = Button(screen_width // 2 + 50, screen_height - 80, yukle_resim)

#main game loop
run = True
while run:

	clock.tick(fps)

	#draw background
	screen.fill(green)
	screen.blit(arkaplan, (0, 0))


	#load and save level
	if save_button.draw():
		#save level data
		pickle_out = open(f'level{level}_data', 'wb')
		pickle.dump(world_data, pickle_out)
		pickle_out.close()
	if load_button.draw():
		#load in level data
		if path.exists(f'level{level}_data'):
			pickle_in = open(f'level{level}_data', 'rb')
			world_data = pickle.load(pickle_in)


	#show the grid and draw the level tiles
	draw_grid()
	draw_world()


	#text showing current level
	draw_text(f'Level: {level}', font, white, tile_size, screen_height - 60)
	draw_text('Press UP or DOWN to change level', font, white, tile_size, screen_height - 40)

	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False
		#mouseclicks to change tiles
		if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
			clicked = True
			pos = pygame.mouse.get_pos()
			x = pos[0] // tile_size
			y = pos[1] // tile_size
			#check that the coordinates are within the tile area
			if x < 20 and y < 20:
				#update tile value
				if pygame.mouse.get_pressed()[0] == 1:
					world_data[y][x] += 1
					if world_data[y][x] > 12:
						world_data[y][x] = 0
				elif pygame.mouse.get_pressed()[2] == 1:
					world_data[y][x] -= 1
					if world_data[y][x] < 0:
						world_data[y][x] = 12
		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False
		#up and down key presses to change level number
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			elif event.key == pygame.K_DOWN and level > 1:
				level -= 1

	#update game display window
	pygame.display.update()

pygame.quit()