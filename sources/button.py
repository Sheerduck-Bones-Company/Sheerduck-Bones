import pygame, os

#On récupère le path absolu du fichier pour que les chemins relatifs marchent toujours (qu'on lance le programme depuis le fichier lui-même ou depuis le dosisier du projet)
FILE_PATH = os.path.dirname(os.path.abspath(__file__))

#On crée une classe pour créer des boutons
class Button():
    def __init__(self, screen : pygame.Surface, name:str, perc_border_x:int, perc_border_y:int, perc_width:int=-1, perc_height:int=-1):
        self.screen = screen                                                                                        #L'écran sur lequel est afficher le bouton
        self.image = pygame.image.load(f'{FILE_PATH}/assets/graphics/buttons/{name}_button.png').convert_alpha()    #L'image du bouton en fonction du nom donné
        if perc_width != -1:                                                                                        #La taille de l'image en fonction de la largeur donnée
            self.size_vector = pygame.Vector2(self.image.get_size()) / self.image.get_width()
            self.perc_width, self.perc_height = perc_width/100, -1
        elif perc_height != -1:                                                                                     #La taille de l'image en fonction de la hauteur donnée
            self.size_vector = pygame.Vector2(self.image.get_size()) / self.image.get_height()
            self.perc_width, self.perc_height = -1, perc_height/100
        else:
            self.perc_width, self.perc_height = -1, -1
        self.rect = pygame.Rect((0,0,0,0))
        self.perc_border_x = perc_border_x/100                                                                      #La bordure x du bouton en fonction de la valeur donnée
        self.perc_border_y = perc_border_y/100                                                                      #La bordure y du bouton en fonction de la valeur donnée
    
    #Afficher le bouton (le calcul des dimensions et des coordonnées se font en permanence au cas où si la taille de l'écran change)
    def draw(self):
        #On récupère les dimensions de l'écran
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        if self.perc_width != -1:
            #On change la taille de l'image pour qu'elle fasse perc_width pourcents de la largeur de l'écran
            self.image = pygame.transform.scale(self.image, self.size_vector*screen_width*self.perc_width)
        elif self.perc_height != -1:
            #On change la taille de l'image pour qu'elle fasse perc_height pourcents de la hauteur de l'écran
            self.image = pygame.transform.scale(self.image, self.size_vector*screen_height*self.perc_height)
        self.rect = self.image.get_rect()
        
        #On crée les coordonnées du boutons en fonction des bordures données
        if self.perc_border_x >= 0:     #Calcul de la bordure x
            self.rect.left = screen_width*self.perc_border_x
        else:
            self.rect.right = screen_width*(1+self.perc_border_x)
            
        if self.perc_border_y >= 0:     #Calcul de la bordure y
            self.rect.top = screen_height*self.perc_border_y
        else:
            self.rect.bottom = screen_height*(1+self.perc_border_y)
        
        #On affiche le bouton à l'endroit souhaité
        self.screen.blit(self.image, self.rect)


        
