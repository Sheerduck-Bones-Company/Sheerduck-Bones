import pygame
from hint import Hint

#Une classe pour créer des boîtes de dialogues
class Dialogues():
    def __init__(self, place, step, text, add_step, add_hint, game):
        self.game = game
        self.place = place              #Le lieu où doit être dits les dialogues
        self.step = step                #Etape où doit être dits
        self.text = text                #Les différents dialogues du groupe de dialogues
        self.add_step = add_step        #Le nombre d'étape à rajouter au jeu lors d'un dialogue
        self.is_step_added = False      #Si l'étape a déjà été ajoutée
        self.add_hint = add_hint        #L'indice à rajouter au joueur lors d'un dialogue
        self.is_hint_added = False      #Si l'indice a déjà été ajouté
        self.current_dial_num = 0       #L'indice actuel du dialogue
    
    #Actualise le groupe de dialogues en passant au dialogue suivant
    def update(self):
        self.current_dial_num += 1
        #Si on atteint le dernier dialogue, on ajoute l'étape ou l'indice désiré
        if self.current_dial_num == len(self.text):
            self.current_dial_num = 0
            self.AddStep()
            self.AddHint()
    
    #Ajouter des étapes au jeu
    def AddStep(self):
        if self.add_step != None and not self.is_step_added:
            self.game.current_step += self.add_step
            self.is_step_added = True

    #Ajouter un indice au joueur
    def AddHint(self):
        if self.add_hint != None and not self.is_hint_added:
            self.game.player.hints.append(Hint(self.add_hint))
            self.is_hint_added = True
            
#Une classe pour gérer l'affichage des dialogues
class SpeechBubble():
    def __init__(self, game, text:list = []):
        self.game = game
        #La liste des personnages qui parlent
        self.list_char = [elem[0] for elem in text]
        #La liste des répliques
        self.list_text = [elem[1] for elem in text]
        self.splited_text = []
        
        #Les différentes surfaces et images
        self.lignes_surface = (pygame.Surface((0,0)), pygame.Surface((0,0)), pygame.Surface((0,0)))
        self.lignes_rect = (pygame.Rect((0,0,0,0)), pygame.Rect((0,0,0,0)), pygame.Rect((0,0,0,0)))
        self.frame_rect = pygame.Rect((0,0,0,0))
        self.bg_rect = pygame.Rect((0,0,0,0))
        
        #L'image du personnage qui parle
        self.character_surf = pygame.Surface((128,128))
        self.character_rect = self.character_surf.get_rect(left=0, bottom=3*(self.game.screen.get_height())/4)
        
        #Les indices de la réplique et de la boîte de dialogues
        self.index_sentence = 0
        self.index_box = 0
        
        #Les dimensions de l'écran
        self.last_screen_dimension = (1080,720)
        self.size = 50
        self.max_width = 720
        
        #La police d'écriture du texte
        self.font = pygame.font.SysFont(None, self.size)

    #On initialise le dialogue
    def initialize(self):
        #On crée les dimensions du cadre de la boîte de dialogue
        screen_dimension = (self.game.screen.get_width(), self.game.screen.get_height())
        l = 0
        t = screen_dimension[1] - screen_dimension[1] / 4
        w = screen_dimension[0]
        h = screen_dimension[1] / 4
        border = 0.5/100
        
        #On crée les Rect du cadre / du fond / des lignes par rapport aux dimensions du cadre
        self.frame_rect = pygame.Rect(l, t, w, h)
        self.bg_rect = pygame.Rect(w*border, t + w*border, w*(1-2*border), h - w*2*border)
        self.lignes_rect = (pygame.Rect(w*2*border, t + w*2*border, w*(1-4*border), h - w*4*border),
                            pygame.Rect(w*2*border, t + w*2*border + self.size, w*(1-4*border), h - w*4*border),
                            pygame.Rect(w*2*border, t + w*2*border + 2*self.size, w*(1-4*border), h - w*4*border))
        
        #On définie la taille de l'écriture et la longeur de ligne à ne pas dépasser
        self.size = round(self.lignes_rect[0].height/3)
        self.max_width = self.lignes_rect[0].width
        
        #On reset les indices utilisé dans le découpage
        self.index_sentence = 0
        self.index_box = 0
        
        #On crée notre police
        self.create_font()
        
        #On découpe le dialogue en boîtes de dialogue et en lignes
        self.splited_text = []
        self.split(self.list_text)
        
        #On écrit la première ligne
        self.create_text(self.splited_text[0][0])
        self.index_box += 1
        
        #On crée l'image du personnage qui parle
        self.create_face(self.list_char[self.index_sentence])
    
    #On actualise la boîte de dialogue dans l'ordre
    def update(self):
        #Si on arrive à la dernière boîte de dialogue de la réplique
        if self.index_box == len(self.splited_text[self.index_sentence]):
            #Si on est à la dernière réplique, on ferme le dialogue
            if self.index_sentence == len(self.splited_text) - 1:
                self.game.is_speeking = False
                self.game.player.current_speech = None
                return False
            #Sinon on passe à la réplique suivante
            else:
                self.index_box = 0
                self.index_sentence += 1
                self.create_face(self.list_char[self.index_sentence])
        
        #On affiche la boîte de dialogue
        self.create_text(self.splited_text[self.index_sentence][self.index_box])
        
        #On passe à la boîte de dialogue suivante
        self.index_box += 1
    
    #Créer une police
    def create_font(self):
        self.font = pygame.font.SysFont(None, self.size)
    
    #Découper le texte en boîtes de dialogues elles-mêmes découpées en lignes selon les dimensions de l'écran
    def split(self, text : list):
        for sentIndex, sentence in enumerate(text):
            self.splited_text.append([])
            split_sentence = sentence.split(' ')
            boxIndex = 0
            wordIndex = 0
            
            #Tant qu'il reste des mots dans la réplique
            while wordIndex < len(split_sentence):
                self.splited_text[sentIndex].append([])
                #Pour chaque ligne (3)
                for i in range(3):
                    ligne = []
                    #Tant que le mot ne dépasse pas de l'écran, on l'ajoute à la ligne
                    while (wordIndex < len(split_sentence)) and (self.font.size(' '.join(ligne) + ' ' + split_sentence[wordIndex])[0] < self.max_width):
                        ligne.append(split_sentence[wordIndex])
                        wordIndex += 1
                    #On ajoute la ligne
                    self.splited_text[sentIndex][boxIndex].append(' '.join(ligne))
                boxIndex += 1
    
    #Afficher la boîte de dialogue (c'est à dire ses trois lignes)
    def create_text(self, text : list):
        self.lignes_surface = (self.font.render(text[0], True, (0,0,0)),
                               self.font.render(text[1], True, (0,0,0)),
                               self.font.render(text[2], True, (0,0,0)))
    
    #On affiche le tout sur l'écran
    def draw(self):
        #Si la taille de l'écran a changé, on réinitialise le dialogue
        screen_dimension = (self.game.screen.get_width(), self.game.screen.get_height())
        if screen_dimension != self.last_screen_dimension:
            self.last_screen_dimension = screen_dimension
            self.initialize()
        
        self.game.screen.blit(self.character_surf, self.character_rect)
        pygame.draw.rect(self.game.screen, (0,0,0), self.frame_rect)
        pygame.draw.rect(self.game.screen, (255,255,255), self.bg_rect)
        self.game.screen.blit(self.lignes_surface[0], self.lignes_rect[0])
        self.game.screen.blit(self.lignes_surface[1], self.lignes_rect[1])
        self.game.screen.blit(self.lignes_surface[2], self.lignes_rect[2])
    
    #On crée l'image du personnage qui parle
    def create_face(self, name):
        #Si le nom est donné, on crée l'image
        if name != None:
            self.character_surf = pygame.image.load(f"assets/graphics/characters/{name}.png").convert_alpha()
            self.character_surf = pygame.transform.scale(self.character_surf, (128,128))
        else:
            self.character_surf = pygame.Surface((0,0))