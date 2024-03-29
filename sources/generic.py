import pygame, os

#On récupère le path absolu du fichier pour que les chemins relatifs marchent toujours (qu'on lance le programme depuis le fichier lui-même ou depuis le dosisier du projet)
FILE_PATH = os.path.dirname(os.path.abspath(__file__))

#Une classe pour gérer les génériques
class Generic():
    def __init__(self, screen, text:list, size:int, txtcolor=(0,0,0), bgcolor=(255,255,255), speed = 2.5, bgimg=None, is_centered=False):
        self.screen = screen                                                                #L'écran sur lequel on affiche le générique
        self.size = size                                                                    #La taille de police
        self.font = pygame.font.SysFont(None, size=size)                                    #La police d'écriture
        self.generic = text                                                                 #Le texte
        self.generic = [self.font.render(elem, False, txtcolor) for elem in self.generic]   #On crée toutes les lignes du générique
        self.bgcolor = bgcolor                                                              #La couleur de fond d'écran
        self.img = None
        if bgimg != None:                                                                   #Si une image est donnée, on la crée et on la met à la bonne taille
            self.img = pygame.image.load(f'{FILE_PATH}/assets/graphics/screens/{bgimg}')
            size_vect = pygame.Vector2(self.img.get_size())
            if self.img.get_size()[0]/1800 >= self.img.get_size()[1]/720:
                rapport = 1080/self.img.get_size()[0]
            else:
                rapport = 720/self.img.get_size()[1]
            self.img = pygame.transform.scale(self.img, size_vect*rapport)
        self.speed = speed                                                                  #La vitesse de défilement
        self.finish = False                                                                 #Si le générique est fini
        self.is_centered = is_centered                                                      #Si le texte doit être centré
        self.ligney = 300                                                                   #La position initiale de la 1e ligne
    
    #On relance  le générique
    def reinitialize(self):
        self.finish = False
    
    #On ferme le générique
    def quit(self):
        self.finish = True
    
    #On actualise le générique
    def update(self):
        self.screen.fill(self.bgcolor)
        if self.img != None:
            self.screen.blit(self.img, self.img.get_rect(center=(540,360)))
        
        #On affiche chaque ligne à la bonne position
        for i, ligne in enumerate(self.generic):
            if self.is_centered: #On centre le texte s'il le faut
                rect = ligne.get_rect(midtop = (540, self.ligney+self.size*i))
            else:
                rect = ligne.get_rect(topleft = (50, self.ligney+self.size*i))
            self.screen.blit(ligne, rect)
            last_rect = rect
        
        #Si la dernière ligne sort de l'écran, on dit que le générique est terminé
        if last_rect.bottom < 0:
            self.finish = True
        
        #On monte toutes les lignes d'un certain nombre de pixels
        self.ligney -= self.speed