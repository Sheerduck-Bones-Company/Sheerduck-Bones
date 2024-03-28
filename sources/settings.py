import os, pygame, re
from pygame.sprite import Group
from speech_bubble import Dialogues

#On récupère le path absolu du fichier pour que les chemins relatifs marchent toujours (qu'on lance le programme depuis le fichier lui-même ou depuis le dosisier du projet)
FILE_PATH = os.path.dirname(os.path.abspath(__file__))

#On importe un dossier d'images
def ImportFolder(path:str):
    folder = {}
    for elem in os.listdir(path):
        surface = pygame.image.load(path+'/'+elem)
        surface = pygame.transform.scale(surface, (64,64))
        folder[elem[:-4]] = surface
    return folder

#On importe tous les dialogues avec des Regex
def ImportSpeech(name_character, game):
    #Si le personnage possède des boîtes de dialogues, on les apporte à partir de son fichier texte
    if name_character+'.txt' in os.listdir(f"{FILE_PATH}/assets/speechs"):
        with open(f"{FILE_PATH}/assets/speechs/{name_character}.txt", 'r', encoding='utf-8') as fichier:
            #On lie le fichier texte
            txt = fichier.read()
            #On récupère tout les groupes de dialogues présents dans le fichier texte
            speechs = re.findall("[^{}\n]+{[^{}]+}", txt)
            speech_bubbles = []
            
            #Pour chaque groupe de dialogues récupéré
            for speech in speechs:
                
                #On récupère le lieu dans lequel on veut que le groupe de dialogues soit dit
                place_match = re.search(r"place\s*:\s*(?P<place>[^,{ ]+)", speech)
                if place_match != None:
                    place = place_match.group('place')
                else:
                    place = None
                
                #On récupère l'étape durant laquelle on veut que le groupe de dialogues soit dit
                step_match = re.search(r"step\s*:\s*(?P<step>[^,{ ]+)", speech)
                if step_match != None:
                    step = step_match.group('step')
                    
                    #Si un tiret est présent, on affiche le dialogue entre les deux nombres précisés
                    if "-" in step:
                        step = [num for num in range(int(step.split('-')[0]), int(step.split('-')[1])+1, 1)]
                    #Si des "/" sont présents, on récupère toutes les étapes précisées
                    elif '/' in step:
                        step = [int(num) for num in step.split('/')]
                    #Sinon on rajoute l'unique étape
                    else:
                        step = [int(step)]
                else:
                    step = None
                    
                bubble_text = []
                
                #On récupère tout les dialogues du groupe 
                dialogues = re.findall(r"\[([^\[\]]+)\]", speech)
                for dial_ind, dialogue in enumerate(dialogues):
                    current_name = None
                    bubble_text.append([])
                    for ligne in dialogue.split('\n'):
                        #Pour chaque ligne, on récupère le nom de la personne qui parle et ce qu'elle dit
                        name_match = re.search(r"(?P<name>[^: ]+)\s*::", ligne)
                        if name_match != None:
                            current_name = name_match.group("name")
                            text_match = re.search(r"[^: ]+\s*::\s*(?P<text>.+)", ligne)
                            bubble_text[dial_ind].append((current_name, text_match.group('text')))
                        else:
                            bubble_text[dial_ind].append((current_name, ligne))
                    
                #On vérifie si on veut avancer dans l'histoire
                add_step_match = re.search(r"add_step\s*:\s*(?P<add_step>[^ ,{}\[\]\n]+)", speech)
                if add_step_match != None:
                    add_step = int(add_step_match.group('add_step'))
                else:
                    add_step = None
                
                #On vérifie si l'on veut rajouter un indice au joueur
                add_hint_match = re.search(r"add_hint\s*:\s*(?P<add_hint>[^ ,{}\[\]\n]+)", speech)
                if add_hint_match != None:
                    add_hint = add_hint_match.group('add_hint')
                else:
                    add_hint = None
                
                #On crée un groupe de dialogues avec toutes les caractéristiques récupérées
                speech_bubbles.append(Dialogues(place, step, bubble_text, add_step, add_hint, game))
                    
        return speech_bubbles
    
    #Si le personnage ne possède pas de fichier texte pour ses dialogues, on lui rajoute un dialogue par défaut
    else:
        return [Dialogues(None, None, [[(None, "...")]], None, None, game)]

#On importe les cartes du jeu
def loadMap(player, game):
    maps = {}
    for map_name in os.listdir(f"{FILE_PATH}/assets/map"):
        #On initialise les données de la carte à importer (carte / dernières coords du joueur sur la carte / groupe de bloc visile / groupe d'obstacles / groupe de blocs intéractifs)
        mape = []
        last_coord = (0,0)
        obstacles_group = pygame.sprite.Group()
        visible_group = pygame.sprite.Group(player)
        interact_group = pygame.sprite.Group()
        
        #On ouvre le fichier texte de la carte
        with open(f'{FILE_PATH}/assets/map/{map_name}', 'r', encoding='utf-8') as fichier:
            map_text = fichier.read()
            #Pour chaque couche, chaque ligne, chaque bloc, on récupère les information du bloc
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
                            
                            #On récupèr le nom du bloc
                            crt_type = crt_attributes[0]
                            
                            #Si le bloc appartient à une image composée de plusieurs blocs, on affiche l'image entière pour gagner en performances
                            if "_" in crt_type:
                                #Si le bloc concerné est celui tout en bas à gauche de l'image, on affiche l'image entière
                                if crt_type.split('_')[1] == "0-0":
                                    crt_type = crt_type.split('_')[0]
                                    crt_img = pygame.image.load(f"{FILE_PATH}/assets/graphics/group_blocs/{crt_type}.png").convert_alpha()
                                    crt_img = pygame.transform.scale(crt_img, (crt_img.get_size()[0]*4,crt_img.get_size()[1]*4))
                                    crt_rect = crt_img.get_rect(bottomleft=(bloc_index*64, (lin_index+1)*64))
                                
                                #Sinon on met un bloc invisible
                                else:
                                    crt_img = pygame.image.load(f"{FILE_PATH}/assets/graphics/blocs/invisible-barrier.png").convert_alpha()
                                    crt_img = pygame.transform.scale(crt_img, (64,64))
                                    crt_rect = pygame.Rect(bloc_index*64, lin_index*64, 64, 64)
                            
                            #Sinon, récupère simplement l'image du bloc
                            else:
                                crt_img = pygame.image.load(f"{FILE_PATH}/assets/graphics/blocs/{crt_type}.png").convert_alpha()
                                crt_img = pygame.transform.scale(crt_img, (64,64))
                                crt_rect = pygame.Rect(bloc_index*64, lin_index*64, 64, 64)
                            
                            #Si la couche interprêtée est différente de la 1e, on ajoute le bloc au élément visibles
                            if lay_index != 0:
                                visible_group.add(Tile(crt_img, crt_rect))
                            
                            #On vérifie si le bloc doit être afficher devant le joueur
                            if int(crt_attributes[1]) == 1:
                                crt_is_above_player = True
                            else:
                                crt_is_above_player = False
                                
                            #On ajoute les caractéristiques du bloc
                            mape[lay_index][lin_index].append({"image": crt_img, "rect": crt_rect, "is_above": crt_is_above_player})
                            
                            #On ajoute les collisions du bloc au groupe d'obstacles
                            for col_index, collision in enumerate(crt_attributes[3]):
                                if int(collision)==1:
                                    obstacles_group.add(Obstacle(pygame.Rect((bloc_index*2+col_index%2)*32, (lin_index*2+col_index//2)*32, 32, 32)))
                            
                            #Si le bloc mène à une autre carte, on définie les dernières coords du joueur sur la carte comme étant les coords du bloc en question
                            if crt_attributes[4] != '':
                                last_coord = (bloc_index*64-16, lin_index*64)
                                interact_group.add(InteractTile(crt_rect.inflate(28,28), map_path=crt_attributes[4]))
                            
                            #Si le bloc est un joueur, on importe ses dialogues
                            if crt_type+'.png' in os.listdir(f"{FILE_PATH}/assets/graphics/characters"):
                                crt_speech = ImportSpeech(crt_type, game)
                                interact_group.add(InteractTile(crt_rect.inflate(28,28), speech=crt_speech))

        maps[map_name] = {"ground" : mape, "visible" : visible_group, "obstacles" : obstacles_group, "interact" : interact_group, "last_coord" : last_coord, "group_list" : [visible_group, obstacles_group, interact_group]}
                           
    return maps

#On crée une classe pour les obstacles
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.rect = rect

#On crée une classe pour les blocs
class Tile(pygame.sprite.Sprite):
    def __init__(self, img, rect):
        super().__init__()
        self.image = img
        self.rect = rect

#On crée une classe pour les blocs intéractifs
class InteractTile(pygame.sprite.Sprite):
    def __init__(self, rect, map_path=None, speech:list=[]):
        super().__init__()
        self.rect = rect
        self.map_path = map_path
        self.speech = [elem for elem in speech]