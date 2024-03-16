import os, pygame, re
from pygame.sprite import Group
from speech_bubble import Dialogues

def ImportFolder(path:str):
    folder = {}
    for elem in os.listdir(path):
        surface = pygame.image.load(path+'/'+elem)
        surface = pygame.transform.scale(surface, (64,64))
        folder[elem[:-4]] = surface
    return folder

def ImportSpeech(name_character):
    try:
        with open(f"assets/speechs/{name_character}.txt", 'r') as fichier:
            txt = fichier.read()
            speechs = re.findall("[^{}\n]+{[^{}]+}", txt)
            speech_bubbles = []
            
            for speech in speechs:
                
                place_match = re.search(r"place\s*:\s*(?P<place>[^,{ ]+)", speech)
                if place_match != None:
                    place = place_match.group('place')
                else:
                    place = None
                        
                step_match = re.search(r"step\s*:\s*(?P<step>[^,{ ]+)", speech)
                if step_match != None:
                    step = step_match.group('step')
                        
                    if "-" in step:
                        step = [num for num in range(step.split('-')[0], step.split('-')[1]+1, 1)]
                    elif '/' in step:
                        step = [int(num) for num in step.split('/')]
                    else:
                        step = int(step)
                else:
                    step = None
                    
                bubble_text = []
                    
                dialogues = re.findall(r"\[([^\[\]]+)\]", speech)
                for dial_ind, dialogue in enumerate(dialogues):
                    bubble_text.append([])
                    for ligne in dialogue.split('\n'):
                        m = re.search(r"(?P<name>[^: ]+)\s*:\s*(?P<text>.+)", ligne)
                        bubble_text[dial_ind].append((m.group('name'), m.group('text')))
                            
                speech_bubbles.append(Dialogues(place, step, bubble_text))
                    
        return speech_bubbles
    except:
        return [Dialogues(None, None, [[(None, "...")]])]

def loadMap(player):
    maps = {}
    for map_name in os.listdir("assets/map"):
        mape = []
        last_coord = (0,0)
        obstacles_group = pygame.sprite.Group()
        visible_group = pygame.sprite.Group(player)
        interact_group = pygame.sprite.Group()
        with open(f'assets/map/{map_name}', 'r') as fichier:
            map_text = fichier.read()
            for lay_index, layer in enumerate(map_text.split('$')):
                mape.append([])
                
                for lin_index, ligne in enumerate(layer.split('|')):
                    mape[lay_index].append([])
                    
                    for bloc_index, bloc in enumerate(ligne.split('/')):
                        if bloc == '0':
                            mape[lay_index][lin_index].append(0)
                        else:
                            crt_attributes = bloc.split(',')
                            #On récupère les caractéristiques du bloc
                            
                            crt_type = crt_attributes[0]
                            if "_" in crt_type:
                                if crt_type.split('_')[1] == "0-0":
                                    crt_type = crt_type.split('_')[0]
                                    crt_img = pygame.image.load(f"assets/graphics/group_blocs/{crt_type}.png").convert_alpha()
                                    crt_img = pygame.transform.scale(crt_img, (crt_img.get_size()[0]*4,crt_img.get_size()[1]*4))
                                    crt_rect = crt_img.get_rect(bottomleft=(bloc_index*64, (lin_index+1)*64))
                                else:
                                    crt_img = pygame.image.load(f"assets/graphics/blocs/invisible-barrier.png").convert_alpha()
                                    crt_img = pygame.transform.scale(crt_img, (64,64))
                                    crt_rect = pygame.Rect(bloc_index*64, lin_index*64, 64, 64)
                            else:
                                crt_img = pygame.image.load(f"assets/graphics/blocs/{crt_type}.png").convert_alpha()
                                crt_img = pygame.transform.scale(crt_img, (64,64))
                                crt_rect = pygame.Rect(bloc_index*64, lin_index*64, 64, 64)
                            
                            if lay_index != 0:
                                visible_group.add(Tile(crt_img, crt_rect))
                            
                            if int(crt_attributes[1]) == 1:
                                crt_is_above_player = True
                            else:
                                crt_is_above_player = False
                                
                            #On ajoute les caractéristiques du bloc
                            mape[lay_index][lin_index].append({"image": crt_img, "rect": crt_rect, "is_above": crt_is_above_player})
                            
                            for col_index, collision in enumerate(crt_attributes[3]):
                                if int(collision)==1:
                                    obstacles_group.add(Obstacle(pygame.Rect((bloc_index*2+col_index%2)*32, (lin_index*2+col_index//2)*32, 32, 32)))
                                        
                            if crt_attributes[4] != '':
                                last_coord = (bloc_index*64-16, lin_index*64)
                                interact_group.add(InteractTile(crt_rect.inflate(28,28), map_path=crt_attributes[4]))
                            
                            if crt_type+'.png' in os.listdir("assets/graphics/characters"):
                                crt_speech = ImportSpeech(crt_type)
                                interact_group.add(InteractTile(crt_rect.inflate(28,28), speech=crt_speech))

        maps[map_name] = {"ground" : mape, "visible" : visible_group, "obstacles" : obstacles_group, "interact" : interact_group, "last_coord" : last_coord, "group_list" : [visible_group, obstacles_group, interact_group]}
                           
    return maps

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.rect = rect
        
class Tile(pygame.sprite.Sprite):
    def __init__(self, img, rect):
        super().__init__()
        self.image = img
        self.rect = rect
        
class InteractTile(pygame.sprite.Sprite):
    def __init__(self, rect, map_path=None, speech:list=[]):
        super().__init__()
        self.rect = rect
        self.map_path = map_path
        self.speech = [elem for elem in speech]