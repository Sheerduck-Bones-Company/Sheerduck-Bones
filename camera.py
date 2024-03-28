import pygame

class Camera(pygame.sprite.Group):
	def __init__(self, game):
		super().__init__()

		self.game = game
  
		#On récupère la surface de l'écran
		self.display_surface = pygame.display.get_surface()

		#On crée les décalages qu'il faudra appliquer aux images affichées
		self.offset = pygame.math.Vector2()
		self.half_w = self.display_surface.get_size()[0] // 2
		self.half_h = self.display_surface.get_size()[1] // 2

		#On crée les varaibles utiles pour le zoom de la caméra
		self.zoom_scale = 1
		self.last_zoom_scale = 0
		self.internal_surf_size = game.screen.get_size()
		self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
		self.internal_rect = self.internal_surf.get_rect(center = (self.half_w,self.half_h))
		self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
		self.internal_offset = pygame.math.Vector2()
		self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
		self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h
		self.new_scale = 0
		self.dest = pygame.Surface((0,0))
		
		#On crée la petite image de la touche E lorsque qu'on peut intéragir avec l'environnement
		self.interact_img = pygame.image.load("assets/graphics/buttons/E.png")
		self.interact_img = pygame.transform.scale(self.interact_img, (30, 30))

	#On centre la caméra sur une cible
	def center_target_camera(self,target):
		self.offset.x = target.rect.centerx - self.half_w
		self.offset.y = target.rect.centery - self.half_h

	#On actualise l'écran
	def custom_draw(self,target):
		#On centre la cible
		self.center_target_camera(target)
		
		#Si la carte correspond à la carte de la ville, on affiche un fond bleu, sinon on affiche un fond noir
		if self.game.current_map_name == "ville.txt":
			self.internal_surf.fill('#71ddee')
		else:
			self.internal_surf.fill('#000000')

		#On récupère les coordonnées du joueur sur sur grille ou 1 unité = 64 px (soit 1 bloc)
		player_pos = ((self.game.player.rect.centerx)//64, (self.game.player.rect.centery)//64)
		
		#On récupère la liste des blocs de la 1e couche qu'il faut afficher (c'est à dire ceux qui apparaissent à l'écran), pour améliorer les performances
		if player_pos[0] < 9:	#Si le joueur est tout à gauche de la carte
			left_col, right_col = 0, player_pos[0]+10
		else:
			left_col, right_col = player_pos[0]-9, player_pos[0]+10
   
		if player_pos[1] < 6:	#Si le joueur est tout en haut de la carte
			top_lin, bot_lin = 0, player_pos[1]+7
		else:
			top_lin, bot_lin = player_pos[1]-6, player_pos[1]+7
  
		#On affiche les blocs de la 1e couche que l'on vient de récupérer
		for ligne in self.game.maps.get(self.game.current_map_name).get("ground")[0][top_lin:bot_lin]:
			for bloc in ligne[left_col:right_col]:
				if bloc != 0:
					#On calcule le décalage à appliquer aux coordonées du bloc lors de son affiche
					offset_pos = bloc.get('rect').topleft - self.offset + self.internal_offset
					self.internal_surf.blit(bloc.get('image'), offset_pos)

		#On affiche les éléments par ordonnée croissante
		for sprite in sorted(self.game.maps.get(self.game.current_map_name).get("visible") ,key = lambda sprite: (sprite.rect.centery+sprite.rect.height/4)):
			#On calcule le décalage à appliquer aux coordonées du bloc lors de son affiche
			offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
			self.internal_surf.blit(sprite.image, offset_pos)
   
		sprites = self.game.check_collisions(self.game.player, self.game.maps.get(self.game.current_map_name).get("interact"))
		if len(sprites) != 0:
			self.internal_surf.blit(self.interact_img, self.game.player.rect.topleft + pygame.Vector2(64, -10) - self.offset + self.internal_offset)

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