import pygame
class AnimateCharacter(pygame.sprite.Sprite):
  def __init__(self, sprite_name):
    super().__init__()
    self.image = pygame.image.load('graphics/' + sprite_name + '.png')                    #à modifier si besoin
    self.current_image = 0 #on commence par la premiere image
    self.imgs = animations.get(sprite_name)                                                    #à modifier

def animate(self):
  self.current_image += 1
  if self.current_image >= len(self.images):
    self.current_image = 0
    self.image = self.imgs[self.current_image]

#charge les images des personnages :
def chargement_img_sprite(sprite_name):
  imgs = []
  path = f"graphics/{sprite_name}/{sprite_name}"                                           #Le premier sprite name correspond au dossier et le deuxieme au nom du fichier
  for nombre in range(a,b):                                                                 #a est l'indice de la premiere image et b la derniere
    imgs_path = path + str(nombre) +'.png'
    pygame.image.load(imgs_path)
    imgs.append(pygame.image.load(imgs_path))
return imgs
#creer dico qui contient toutes les animations des personnages
dico={sheerduck : chargement_imgs_sprite('sheerduck')}                                        #modifier le dico pour les autres persos

#Apres il faut rajouter des trucs dans le fichier player
#Ressources : https://www.youtube.com/watch?v=70OAR-DCxKc&t=0s
#Ajouter aussi tous les persos dans le dico
#/!\ Mettre les persos dans des dossiers à leur nom et ajouter leur numéro pour l'ordre d'animation
