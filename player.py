import pygame, os
from settings import ImportFolder

class Player(pygame.sprite.Sprite):
	def __init__(self, game, pos):
		super().__init__()
		self.images = ImportFolder("assets/graphics/player")
		self.image = self.images.get("front_stand")
		self.game = game
		self.rect = self.image.get_rect(center = pos).inflate(-4,-4)
		self.direction = pygame.math.Vector2()
		self.speed = 12
		self.status = "front_stand"
		self.animation_counter = 0

	#On déplace le joueur si aucune boîte de dialoque n'est ouverte
	def input(self):
		if self.game.is_speeking:
			self.direction.x, self.direction.y = 0,0
			if not "_stand" in self.status:
				self.status += "_stand"
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

	def move(self):
		self.rect.centerx += self.direction.x * self.speed
		self.check_collisions("horizontal")
		self.rect.centery += self.direction.y * self.speed
		self.check_collisions("vertical")

	#On actualise les coordonnées du joueur
	def update(self):
		self.input()
		self.move()
		self.animate()
  
	def animate(self):
		self.animation_counter += 0.15
		if self.animation_counter > 2:
			self.animation_counter = 0
		
		if "_stand" in self.status:
			self.image = self.images.get(self.status)
		else:
			self.image = self.images.get(self.status+str(int(self.animation_counter)))
   
	def check_collisions(self, direction):
		sprites = self.game.check_collisions(self, self.game.maps.get(self.game.current_map_name).get("obstacles"))
		if len(sprites) != 0:    
			if direction == "horizontal":
				
				if self.direction.y > 0:
					self.status = "front"
				elif self.direction.y < 0:
					self.status = "back"
				elif not "_stand" in self.status:
					self.status += "_stand"
				for sprite in sprites:
					if self.direction.x > 0:
						self.rect.right = sprite.rect.left
					elif self.direction.x < 0:
						self.rect.left = sprite.rect.right

			if direction == "vertical":
				if (self.status == "front" or self.status == "back") and not "_stand" in self.status:
					self.status += "_stand"
				for sprite in sprites:
					if self.direction.y > 0:
						self.rect.bottom = sprite.rect.top
					elif self.direction.y < 0:
						self.rect.top = sprite.rect.bottom

	def check_interact(self):
		sprites = self.game.check_collisions(self, self.game.maps.get(self.game.current_map_name).get("interact"))
		if len(sprites) != 0 and self.game.pressed.get(pygame.K_e):
			self.game.maps.get(self.game.current_map_name)['last_coord'] = (self.rect.x, self.rect.y)
			self.game.current_map_name = sprites[0].map_path + ".txt"
			
			coord = self.game.maps.get(self.game.current_map_name).get("last_coord")
			if coord != None:
				self.rect.x, self.rect.y = coord[0], coord[1]