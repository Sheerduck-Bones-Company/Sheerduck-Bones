import pygame
class AnimateCharacter(pygame.sprite.Sprite):
  def __init__(self, sprite_name):
    super().__init__()
    self.image = pygame.image.load('graphics/' + sprite_name + '.png')                    #à modifier si besoin

#charge les images des personnages :
def chargement_img_sprite(sprite_name):
  img = []
  path = f"graphics/{sprite_name}/{sprite_name}"                                          #Le premier sprite name correspond au dossier et le deuxieme au nom du fichier
