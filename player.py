import pygame, os
from settings import ImportFolder

class Player(pygame.sprite.Sprite):
	def __init__(self, game, pos, group):
		super().__init__(group)
		self.images = ImportFolder("assets/graphics/player")
		self.image = self.images.get("front_stand")
		self.game = game
		self.rect = self.image.get_rect(center = pos)
		self.direction = pygame.math.Vector2()
		self.speed = 12
		self.status = "front_stand"
		self.animation_counter = 0

	#On déplace le joueur si aucune boîte de dialoque n'est ouverte
	def input(self):
		if self.game.is_speeking:
			self.direction.x, self.direction.y = 0,0
		elif self.game.is_playing:	
			if self.game.pressed.get(pygame.K_z):
				self.direction.y = -1
				self.status = "back"
			elif self.game.pressed.get(pygame.K_s):
				self.direction.y = 1
				self.status = "front"
			else:
				self.direction.y = 0

			if self.game.pressed.get(pygame.K_d):
				self.direction.x = 1
				self.status = "right"
			elif self.game.pressed.get(pygame.K_q):
				self.direction.x = -1
				self.status = "left"
			else:
				self.direction.x = 0

			if self.direction.length() > 0:
				self.direction = self.direction.normalize()
			elif not "_stand" in self.status:
				self.status += "_stand"

	#On actualise les coordonnées du joueur
	def update(self):
		self.input()
		self.rect.center += self.direction * self.speed
		self.animate()
  
	def animate(self):
		self.animation_counter += 0.15
		if self.animation_counter > 2:
			self.animation_counter = 0
		
		if "_stand" in self.status:
			self.image = self.images.get(self.status)
		else:
			self.image = self.images.get(self.status+str(int(self.animation_counter)))