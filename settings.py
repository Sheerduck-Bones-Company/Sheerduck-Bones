import os, pygame
from pygame.sprite import Group

def ImportFolder(path:str):
    folder = {}
    for elem in os.listdir(path):
        surface = pygame.image.load(path+'/'+elem)
        surface = pygame.transform.scale(surface, (64,64))
        folder[elem[:-4]] = surface
    return folder

def loadMap():
    maps = {}
    for map_name in os.listdir("assets/map"):
        mape = []
        obstacles = []
        obstacles_group = pygame.sprite.Group()
        with open(f'assets/map/{map_name}', 'r') as fichier:
            map_text = fichier.read()
            for lay_index, layer in enumerate(map_text.split('$')):
                mape.append([])
                
                for lin_index, ligne in enumerate(layer.split('|')):
                    mape[lay_index].append([])
                    if lay_index == 0:
                        obstacles.append([])
                        obstacles.append([])
                    
                    for bloc_index, bloc in enumerate(ligne.split('/')):
                        if bloc == '0':
                            mape[lay_index][lin_index].append(0)
                            if lay_index == 0:
                                obstacles[lin_index*2].append(0)
                                obstacles[lin_index*2].append(0)
                                obstacles[lin_index*2+1].append(0)
                                obstacles[lin_index*2+1].append(0)
                        else:
                            crt_attributes = bloc.split(',')
                            #On récupère les caractéristiques du bloc
                            crt_img = pygame.image.load(f"assets/graphics/blocs/{crt_attributes[0]}.png").convert_alpha()
                            crt_img = pygame.transform.scale(crt_img, (64,64))
                            
                            crt_rect = pygame.Rect(bloc_index*64, lin_index*64, 64, 64)
                            
                            if int(crt_attributes[1]) == 1:
                                crt_is_above_player = True
                            else:
                                crt_is_above_player = False
                                
                            #On ajoute les caractéristiques du bloc
                            mape[lay_index][lin_index].append({"image": crt_img, "rect": crt_rect, "is_above": crt_is_above_player})
                            
                            for col_index, collision in enumerate(crt_attributes[3]):
                                if lay_index == 0:
                                    if int(collision)==1:
                                        obstacles[lin_index*2+col_index//2].append(pygame.Rect((bloc_index*2+col_index%2)*32, (lin_index*2+col_index//2)*32, 32, 32))
                                        obstacles_group.add(Tile(pygame.Rect((bloc_index*2+col_index%2)*32, (lin_index*2+col_index//2)*32, 32, 32)))
                                    else:
                                        obstacles[lin_index*2+col_index//2].append(0)
                                else:
                                    if int(collision)==1:
                                        obstacles[lin_index*2+col_index//2][bloc_index*2+col_index%2] = pygame.Rect((bloc_index*2+col_index%2)*32, (lin_index*2+col_index//2)*32, 32, 32)
                                        obstacles_group.add(Tile(pygame.Rect((bloc_index*2+col_index%2)*32, (lin_index*2+col_index//2)*32, 32, 32)))

        maps[map_name] = (mape, obstacles, obstacles_group)
                           
    return maps

class Tile(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.rect = rect