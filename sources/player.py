import pygame, os
from settings import ImportFolder
from speech_bubble import Dialogues
from hint import Hint

#On récupère le path absolu du fichier pour que les chemins relatifs marchent toujours (qu'on lance le programme depuis le fichier lui-même ou depuis le dosisier du projet)
FILE_PATH = os.path.dirname(os.path.abspath(__file__))

class Player(pygame.sprite.Sprite):
	def __init__(self, game, pos):
		super().__init__()
		self.images = ImportFolder(f"{FILE_PATH}/assets/graphics/player")			#Les images du joueur
		self.image = self.images.get("front_stand")									#On définie l'image actuelle du joueur
		self.game = game
		self.rect = self.image.get_rect(topleft = pos).inflate(-4,-4)				#Le rect du joueur
		self.direction = pygame.math.Vector2()										#Un vecteur pour gérer les mouvements du joueur
		self.speed = 12																#La vitesse du joueur
		self.status = "front_stand"													#Le statut actuel du joueur
		self.animation_counter = 0
		self.current_speech = None													#Le dialogue actuel
		self.hints = []																#La liste des indices du joueur
		self.current_hint = None													#L'indice actuellement utilisé
  
	#On actualise les coordonnées du joueur
	def update(self):
		#On détecte les touches activées
		self.input()
		#On déplace le joueur
		self.move()
		#On crée l'animation du joueur
		self.animate()
		
		#Si on est en train d'intéragir avec un indice, on le fait suivre la souris
		if self.current_hint != None:
			if not self.current_hint.is_linking:
				self.current_hint.track_mouse()
   
	#On déplace le joueur si aucune boîte de dialoque n'est ouverte
	def input(self):
		#Si on parle, on défini le joueur comme statique
		if self.game.is_speeking:
			self.direction.x, self.direction.y = 0,0
			if not "_stand" in self.status:
				self.status += "_stand"
		
  		#Si on est en train de se déplacer sur la carte, on détecte les touches appuyées
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

	#Déplace le joueur et vérifie les collisions
	def move(self):
		self.rect.centerx += self.direction.x * self.speed
		self.check_collisions("horizontal")
		self.rect.centery += self.direction.y * self.speed
		self.check_collisions("vertical")

	#On vérifie les collisions
	def check_collisions(self, direction):
		#On récupère les sprites en collisison avec le joueur
		sprites = self.game.check_collisions(self, self.game.maps.get(self.game.current_map_name).get("obstacles"))
		
		#Si le joueur est en collisison avec d'autres sprites, on le replace le façon à ce qu'il ne traverse pas l'obstacle
		if len(sprites) != 0:
			
			#On vérifie les collisison horizontales
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

			#On vérifie les collisison verticales
			if direction == "vertical":
				if (self.status == "front" or self.status == "back") and not "_stand" in self.status:
					self.status += "_stand"
				for sprite in sprites:
					if self.direction.y > 0:
						self.rect.bottom = sprite.rect.top
					elif self.direction.y < 0:
						self.rect.top = sprite.rect.bottom

	#On actualise l'animation du personnage
	def animate(self):
		self.animation_counter += 0.15
		if self.animation_counter > 2:
			self.animation_counter = 0
		
		if "_stand" in self.status:
			self.image = self.images.get(self.status)
		else:
			self.image = self.images.get(self.status+str(int(self.animation_counter)))

	#On vérifie si le joueur intéragie avec l'environnement
	def check_interact(self):
		#On récupère les zones d'interaction en collision avec le joueur
		sprites = self.game.check_collisions(self, self.game.maps.get(self.game.current_map_name).get("interact"))
		
		#Si des zones d'interraction sont concernées et si on appuie sur "e"
		if len(sprites) != 0 and self.game.pressed.get(pygame.K_e):
			
			#Si le bloc mène à une autre carte, on change la carte explorée et on enregistre les dernières coordonnées sur la dernière carte
			if sprites[0].map_path != None:
				self.game.maps.get(self.game.current_map_name)['last_coord'] = (self.rect.x, self.rect.y)
				self.game.current_map_name = sprites[0].map_path + ".txt"
				
				coord = self.game.maps.get(self.game.current_map_name).get("last_coord")
				if coord != None:
					self.rect.x, self.rect.y = coord[0], coord[1]

			#Si le bloc est un personnage et possède des lignes de dialogues, on lance le dialogue correspondant à l'étape et au lieu actuels
			if sprites[0].speech != []:
				#Si on n'est pas déjà en train de parler on crée la boîte de dialogues
				if not self.game.is_speeking:
					for speech in sprites[0].speech:
						if ((speech.place == None) and (speech.step == None)) or ((speech.place == None) and (self.game.current_step in speech.step)) or ((self.game.current_map_name[:-4] == speech.place) and (speech.step == None)) or ((self.game.current_map_name[:-4] == speech.place) and (self.game.current_step in speech.step)):
							self.current_speech = speech
							self.game.say(speech.text[speech.current_dial_num])
							speech.update()
							break
					if self.current_speech == None:
						self.current_speech = Dialogues(None, None, [[(None, "...")]], None, None, self.game)
						self.game.say(self.current_speech.text[self.current_speech.current_dial_num])
				#Sinon on actualise la boîte de dialogue déjà ouverte
				else:
					self.game.say(self.current_speech.text[self.current_speech.current_dial_num])

	#On vérifie si le joueur est en train d'intéragir avec un des indices du tableau d'indices
	def check_document_interact(self, pos):
		#Pour chaque indice du joueur
		for hint in self.hints[::-1]:
			#Si on touche la punaise de l'indice, on commence à créer un lien
			if hint.touch_dot_link(pos):
				hint.is_linking = True
				self.current_hint = hint
				break
			#Si on touche simplement l'indice, on le fait suivre la souris
			elif hint.is_caught(pos):
				hint.set_offset(pos)
				self.current_hint = hint
				self.hints.append(hint)
				self.hints.remove(hint)
				break
			#Sinon on supprime un lien potentiellement cliqué
			else:
				hint.clear_touched_link(pos)

	#On arrête d'intéragir avec l'indice actuel
	def stop_document_interact(self, pos):
		if self.current_hint != None:
			for hint in self.hints[::-1]:
				#Si un autre indice est touché lorsqu'on lache la souris, on crée un lien entre les deux indices
				if hint.is_caught(pos) and self.current_hint.is_linking:
					if (not self.current_hint in hint.links) and (self.current_hint != hint):
						hint.links.append(self.current_hint)
						self.current_hint.links.append(hint)
			self.current_hint.is_linking = False

		self.current_hint = None