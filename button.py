import pygame

class Button():
    def __init__(self, screen : pygame.Surface, name:str, perc_border_x:int, perc_border_y:int, perc_width:int):
        self.screen = screen
        self.image = pygame.image.load(f'assets/graphics/{name}_button.png').convert_alpha()
        self.size_vector = pygame.Vector2(self.image.get_size()) / self.image.get_width()
        self.rect = pygame.Rect((0,0,0,0))
        self.perc_border_x = perc_border_x/100
        self.perc_border_y = perc_border_y/100
        self.perc_width = perc_width/100
    
    #Afficher le bouton (le calcul des dimensions et des coordonnées se font en permanence au cas où si la taille de l'écran change)
    def draw(self):
        #On récupère les dimensions de l'écran
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        #On change la taille de l'image pour qu'elle fasse perc_width pourcents de la largeur de l'écran
        self.image = pygame.transform.scale(self.image, self.size_vector*screen_width*self.perc_width)
        self.rect = self.image.get_rect()
        
        #On crée les coordonnées du boutons en fonction des bordures données
        if self.perc_border_x >= 0:
            self.rect.left = screen_width*self.perc_border_x
        else:
            self.rect.right = screen_width*(1+self.perc_border_x)
            
        if self.perc_border_y >= 0:
            self.rect.top = screen_height*self.perc_border_y
        else:
            self.rect.bottom = screen_height*(1+self.perc_border_y)
        
        #On affiche le bouton
        self.screen.blit(self.image, self.rect)


        
