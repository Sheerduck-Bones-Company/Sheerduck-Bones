import pygame
class AnimateCharacter(pygame.sprite.Sprite):
  def __init__(self, sprite_name):
    super().__init__()
    self.image = pygame.image.load('graphics/' + sprite_name + '.png')                    #à modifier si besoin

#charge les images des personnages :
def chargement_img_sprite(sprite_name):
  img = []
  path = f"graphics/{sprite_name}/{sprite_name}"                                           #Le premier sprite name correspond au dossier et le deuxieme au nom du fichier
  for nombre in range(a,b):                                                                 #a est l'indice de la premiere image et b la derniere
    img_path = path + nombre +'.png'
    pygame.image.load(img_path)
    img.append(pygame.image.load(img_path))
return img
#creer dico qui contient toutes les animations des personnages
dico{sheerduck : chargement_img_sprite('sheerduck')}                                        #modifier le dico pour les autres persos
