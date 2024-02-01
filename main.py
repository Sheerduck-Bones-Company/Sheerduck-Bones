import pygame, sys
from random import 
import game

pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
pygame.event.set_grab(True)

# setup 
camera_group = CameraGroup()
game = game.Game()
player = Player((640,360),camera_group)

for i in range(20):
	random_x = randint(1000,2000)
	random_y = randint(1000,2000)
	Tree((random_x,random_y),camera_group)

while game.is_playing:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()

		if event.type == pygame.MOUSEWHEEL:
			camera_group.zoom_scale += event.y * 0.03

	screen.fill('#71ddee')

	camera_group.update()
	camera_group.custom_draw(player)

	pygame.display.update()
	clock.tick(60)
