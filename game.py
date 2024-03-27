import player, camera, speech_bubble, pygame
from settings import loadMap

class Game():
    def __init__(self, screen):
        #On définie les différents états du jeu
        self.is_playing = False
        self.is_speeking = False
        self.is_thinking = False
<<<<<<< HEAD
        self.screen = screen                            #On récupère l'écran
        self.pressed = {}                               #On crée une liste pour les touches pressées
        self.player = player.Player(self, (2338,1136))    #On crée un joueur
        self.maps = loadMap(self.player, self)          #On récupère les cartes du jeu
        self.current_map_name = "ville.txt"             #On définie la carte actuelle comme étant celle de la ville
        self.camera_group = camera.Camera(self)         #On crée une caméra
        self.current_step = 0                           #On définie l'étape actuelle comme étant la première
=======
        self.screen = screen
        self.pressed = {}
        self.player = player.Player(self, (2338,1136))
        self.maps = loadMap(self.player, self)
        self.current_map_name = "ville.txt"
        self.camera_group = camera.Camera(self)
        self.current_step = 0
>>>>>>> edf370d83504322eff55ad810ee3c6530e1513ab
    
    #Lancer la partie    
    def start(self):
        self.is_playing = True

    #Arrêter la partie
    def stop(self):
        self.is_playing = False
    
    #Lancer une boîte de dialogue
    def say(self, text:list):
        #Si un dialogue est déjà lancé, on l'actualise
        if self.is_speeking:
            self.speech_bubble.update()
        #Sinon on lance le dialogue
        else:
            self.speech_bubble = speech_bubble.SpeechBubble(self, text)
            self.speech_bubble.initialize()
            self.is_speeking = True

    #Actualiser la partie
    def update(self):
        #On actualise les différent groupes de sprites actuellement utilisés
        for group in self.maps.get(self.current_map_name).get("group_list"):
            group.update()
        
        #Si on utilise pas le tableau d'indice, on affiche toute la carte et les blocs
        if not self.is_thinking:
            self.camera_group.custom_draw(self.player)
        #Sinon on actualise le tableau
        else:
            self.screen.fill((88, 41, 0))
            #Pour chaque indice, on affiche son image, puis les différents liens qu'il possède avec les autres indices
            for hint in self.player.hints:
                hint.draw(self.screen)
                
            for hint in self.player.hints:
                hint.draw_links(self.screen)
                
                #Si on est en train de créer un lien, on l'affiche connecté à la souris
                if hint.is_linking:
                    pygame.draw.line(self.screen, "red", hint.link_rect.center, pygame.mouse.get_pos())
        
        #Si on est en train de parler, on afiche la bulle de dialogue
        if self.is_speeking:
            self.speech_bubble.draw()
    
    #Une méthode pour détecter une collision entre un sprite et un groupe de sprites
    def check_collisions(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False)