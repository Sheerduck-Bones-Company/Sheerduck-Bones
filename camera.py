import pygame

class Camera(pygame.sprite.Group):
	def __init__(self, game):
		super().__init__()

		self.game = game
  
		#On récupère la surface de l'écran
		self.display_surface = pygame.display.get_surface()

		self.visible_group = game.maps.get("test.txt")[1]

		#On crée les décalages qu'il faudra appliquer aux images affichées
		self.offset = pygame.math.Vector2()
		self.half_w = self.display_surface.get_size()[0] // 2
		self.half_h = self.display_surface.get_size()[1] // 2

		#On crée notre ground
		self.ground_surf = pygame.image.load('assets/graphics/ground.png').convert_alpha()
		self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

		#On crée les varaibles utiles pour le zoom de la caméra
		self.zoom_scale = 1
		self.last_zoom_scale = 0
		self.internal_surf_size = (2500,2500)
		self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
		self.internal_rect = self.internal_surf.get_rect(center = (self.half_w,self.half_h))
		self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
		self.internal_offset = pygame.math.Vector2()
		self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
		self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h
		self.new_scale = 0
		self.dest = pygame.Surface((0,0))

	#On centre la caméra sur une cible
	def center_target_camera(self,target):
		self.offset.x = target.rect.centerx - self.half_w
		self.offset.y = target.rect.centery - self.half_h

	#On actualise l'écran
	def custom_draw(self,target):
		#On centre la cible
		self.center_target_camera(target)
		
		self.internal_surf.fill('#71ddee')

		player_pos = ((self.game.player.rect.centerx)//64, (self.game.player.rect.centery)//64)
		if player_pos[0] < 9:
			left_col, right_col = 0, player_pos[0]+10
		else:
			left_col, right_col = player_pos[0]-9, player_pos[0]+10
   
		if player_pos[1] < 6:
			top_lin, bot_lin = 0, player_pos[1]+7
		else:
			top_lin, bot_lin = player_pos[1]-6, player_pos[1]+7
  
		#On affiche le ground
		for ligne in self.game.maps.get('test.txt')[0][0][top_lin:bot_lin]:
			for bloc in ligne[left_col:right_col]:
				if bloc != 0:
					offset_pos = bloc.get('rect').topleft - self.offset + self.internal_offset
					self.internal_surf.blit(bloc.get('image'), offset_pos)

		#On affiche les éléments par ordonnée croissante
		for sprite in sorted(self.visible_group,key = lambda sprite: sprite.rect.bottom):
			offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
			self.internal_surf.blit(sprite.image, offset_pos)


		#Si le zoom de la caméra a changé, on change l'affichage de l'écran
		if self.last_zoom_scale != self.zoom_scale:
			self.last_zoom_scale = self.zoom_scale
			self.new_scale = self.internal_surface_size_vector * self.zoom_scale
			self.dest = pygame.Surface(self.new_scale)

		#On crée l'écran zoomé
		scaled_surf = pygame.transform.scale(self.internal_surf, self.new_scale, self.dest)
		scaled_rect = scaled_surf.get_rect(center = (self.half_w,self.half_h))

		#On affiche l'écran zoomé
		self.display_surface.blit(scaled_surf,scaled_rect)