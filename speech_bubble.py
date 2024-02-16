import pygame

class SpeechBubble():
    def __init__(self, game, text:list = []):
        self.game = game
        self.list_text = text
        self.splited_text = []
        
        self.lignes_surface = (pygame.Surface((0,0)), pygame.Surface((0,0)), pygame.Surface((0,0)))
        self.lignes_rect = (pygame.Rect((0,0,0,0)), pygame.Rect((0,0,0,0)), pygame.Rect((0,0,0,0)))
        self.frame_rect = pygame.Rect((0,0,0,0))
        self.bg_rect = pygame.Rect((0,0,0,0))
        
        self.index_sentence = 0
        self.index_box = 0
        
        self.last_screen_dimension = (1080,720)
        self.size = 50
        self.max_width = 720
        
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
    
    #On actualise la boîte de dialogue dans l'ordre
    def update(self):
        if self.index_box == len(self.splited_text[self.index_sentence]):
            if self.index_sentence == len(self.splited_text) - 1:
                self.game.is_speeking = False
                return False
            else:
                self.index_box = 0
                self.index_sentence += 1
        
        #On affiche la boîte de dialogue
        self.create_text(self.splited_text[self.index_sentence][self.index_box])
        self.index_box += 1
    
    #Créer une police
    def create_font(self):        
        #self.font = pygame.font.Font('assets/font/minecraft.ttf', self.size)
        self.font = pygame.font.SysFont(None, self.size)
    
    #Découper le texte en boîtes de dialogues elles-mêmes découpées en lignes
    def split(self, text : list):
        for sentIndex, sentence in enumerate(text):
            self.splited_text.append([])
            split_sentence = sentence.split(' ')
            boxIndex = 0
            wordIndex = 0
            while wordIndex < len(split_sentence):
                self.splited_text[sentIndex].append([])
                for i in range(3):
                    ligne = []
                    while (wordIndex < len(split_sentence)) and (self.font.size(' '.join(ligne) + ' ' + split_sentence[wordIndex])[0] < self.max_width):
                        ligne.append(split_sentence[wordIndex])
                        wordIndex += 1
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
        
        pygame.draw.rect(self.game.screen, (0,0,0), self.frame_rect)
        pygame.draw.rect(self.game.screen, (255,255,255), self.bg_rect)
        self.game.screen.blit(self.lignes_surface[0], self.lignes_rect[0])
        self.game.screen.blit(self.lignes_surface[1], self.lignes_rect[1])
        self.game.screen.blit(self.lignes_surface[2], self.lignes_rect[2])