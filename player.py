import pygame

class Player(pygame.sprite.Sprite):
	def __init__(self, game, pos, group):
		super().__init__(group)
		self.image = pygame.image.load('assets/graphics/Sheerduck_Bones-down-left.png').convert_alpha()
		self.image = pygame.transform.scale(self.image, (64, 64))
		self.game = game
		self.rect = self.image.get_rect(center = pos)
		self.direction = pygame.math.Vector2()
		self.speed = 12

	def input(self):
		if self.game.is_speeking:
			self.direction.x, self.direction.y = 0,0
		else:	
			if self.game.pressed.get(pygame.K_z):
				self.direction.y = -1
			elif self.game.pressed.get(pygame.K_s):
				self.direction.y = 1
			else:
				self.direction.y = 0

			if self.game.pressed.get(pygame.K_d):
				self.direction.x = 1
			elif self.game.pressed.get(pygame.K_q):
				self.direction.x = -1
			else:
				self.direction.x = 0

	def update(self):
		self.input()
		self.rect.center += self.direction * self.speed