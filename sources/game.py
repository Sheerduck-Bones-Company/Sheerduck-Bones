import player, camera, speech_bubble, pygame, sys
from settings import loadMap
from generic import Generic

class Game():
    def __init__(self, screen):
        #On définie les différents états du jeu
        self.is_playing = False
        self.is_speeking = False
        self.is_thinking = False
        self.is_helping = False
        self.screen = screen                            #On récupère l'écran
        self.pressed = {}                               #On crée une liste pour les touches pressées
        self.player = player.Player(self, (2402,1250))  #On crée un joueur
        self.maps = loadMap(self.player, self)          #On récupère les cartes du jeu
        self.current_map_name = "ville.txt"             #On définie la carte actuelle comme étant celle de la ville
        self.camera_group = camera.Camera(self)         #On crée une caméra
<<<<<<< HEAD
        self.current_step = 0                           #On définie l'étape actuelle comme étant la première
=======
        self.current_step = 0                         #On définie l'étape actuelle comme étant la première
>>>>>>> a0b6eaa793109c43ab7d2eb34f017d72101e0383
        self.generic_debut = Generic(screen, ['Bonjour Mister Sheerduck.', 'Vous êtes un détective.',
                                              'Vous devez investiguer sur', 'le mystère de Coincoinville.',
                                              'A vous de découvrir votre tâche', 'et de rassembler des preuves.',
                                              'Gagnez la confiance des villageois','afin de résoudre le problème.',
                                              'Nous vous souhaitons bonne chance !'],
                                     60, bgimg='start-screen.png', txtcolor=(255,255,255), bgcolor=(0,0,0), is_centered=True) #On crée un générique
        self.generic_fin = Generic(screen, ['Bravo !!', 'Vous avez réussi à résoudre le mystère :)',
                                            '', 'Crédits :', ''
                                            'Programmation', 'Tout le Chicken Squad', ''
                                            'Graphismes', 'Lianah LOMBARD', 'Chlothilde DINH', 'Thibault HOUPLAIN', '',
                                            'Script', 'Lianah LOMBARD', 'Sarah CAILLAT--ROSEVEGUE', 'Chlothilde DINH', '',
                                            'Dialogues', 'Thibault Houplain', 'Sarah CAILLAT--ROSEVEGUE', 'Chlothilde DINH', '',
                                            'Jeux de mots et humour', 'Sarah CAILLAT--ROSEVEGUE', 'Thibault HOUPLAIN', 'ChatGPT', '',
                                            'Lieux du jeu (programme et réalisation)', 'Antoine GUILMOT', 'Sarah CAILLAT--ROSEVEGUE', '',
                                            'Remerciements :', 'Tout le Chicken Squad se félicite personnellement', 'Sarah CAILLAT--ROSEVEGUE', 'Chlothilde DINH', 'Antoine GUILMOT', 'Thibault HOUPLAIN', 'et Lianah LOMBARD', 'Logan, invité pour la musique'],
                                            60, bgimg='end-screen.png', txtcolor=(255,255,255), bgcolor=(0,0,0), is_centered=True) #On crée un générique de fin

    #Lancer la partie    
    def start(self):
        self.is_playing = True

    #Arrêter la partie
    def stop(self):
        self.is_playing = False
    
    #Afficher le menu d'aide
    def helping(self):
        self.is_helping = True
    
    def stop_helping(self):
        self.is_helping = False
    
    #Lancer une boîte de dialogue
    def say(self, text:list, speech=None):
        #Si un dialogue est déjà lancé, on l'actualise
        if self.is_speeking:
            self.speech_bubble.update()
        #Sinon on lance le dialogue
        else:
            self.speech_bubble = speech_bubble.SpeechBubble(self, text, speech)
            self.speech_bubble.initialize()
            self.is_speeking = True

    #Actualiser la partie
    def update(self):
        if not self.generic_debut.finish: #On affiche le générique de début s'il n'est pas terminé
            self.generic_debut.update()
            
        elif self.generic_fin.finish: #Si le générique de fin est terminé, on ferme le jeu
            pygame.quit()
            sys.exit()
            
        elif self.current_step == 26: #Si on est à l'étape finale, on actualise le générique de fin
            self.generic_fin.update()
            
        else:
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