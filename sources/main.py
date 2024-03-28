#On importe les modules nécessaires
import pygame, os, sys, button
from game import Game

#On récupère le path absolu du fichier pour que les chemins relatifs marchent toujours (qu'on lance le programme depuis le fichier lui-même ou depuis le dosisier du projet)
FILE_PATH = os.path.dirname(os.path.abspath(__file__))

#On initialise la fenêtre
pygame.init()
pygame.display.set_caption('Sheerduck-Bones')
pygame.display.set_icon(pygame.image.load(f'{FILE_PATH}/assets/graphics/icons/game.ico'))

#On crée notre écran
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)

#On crée notre clock
clock = pygame.time.Clock()
FPS = 60

#On initialise l'écran de démarrage
start_screen = pygame.image.load(f'{FILE_PATH}/assets/graphics/screens/start-screen.png').convert_alpha()

#On crée les boutons de démarage
start_button = button.Button(screen, 'start', 20, -10, 10)
exit_button = button.Button(screen, 'exit', -20, -10, 10)
help_button = button.Button(screen, 'help', -10, 10, 10)
hint_button = button.Button(screen, 'hint', -2, -2, 5)

#On crée notre partie
game = Game(screen)

#On intialise la musique
pygame.mixer.init() 
start_music = pygame.mixer.Sound(f"{FILE_PATH}/assets/music/music3.mp3") 
game_music = pygame.mixer.Sound(f"{FILE_PATH}/assets/music/music2.mp3")                
start_channel = pygame.mixer.Channel(0)
game_channel = pygame.mixer.Channel(1)
current_channel = start_channel
current_music = start_music

running = True

#On lance la boucle principale
while running:
    
    #On joue la musique
    current_channel.play(current_music, loops=-1, fade_ms=250)
    
    #Si on est en train de jouer
    if game.is_playing:
        #On actualise la partie
        game.update()
        hint_button.draw()
        current_music = start_music
        current_channel = start_channel
        
    #Sinon on affiche l'écran d'accueil    
    else:
        screen.blit(start_screen, start_screen.get_rect())
        start_button.draw()
        exit_button.draw()
        help_button.draw()
        current_music = game_music
        current_channel = game_channel
    
    #On actualise l'écran    
    pygame.display.flip()
    
    #On vérifie des events
    for event in pygame.event.get():
        
        #Quitter le jeu
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            #On ajoute la touche appuyée à une liste et on précise son état
            game.pressed[event.key] = True
            
            #Quitter le jeu ou retourner sur l'écran d'acceuil
            if event.key == pygame.K_ESCAPE:
                if game.is_playing:
                    game.stop()
                else:
                    running = False
                    pygame.quit()
                    sys.exit()
            
            #Intéragir avec l'environnement
            if event.key == pygame.K_e:
                game.player.check_interact()
            
            #Mettre en plein écran
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
        
        #On précise qu'une touche n'est plus pressée
        if event.type == pygame.KEYUP:
            game.pressed[event.key] = False
        
        #Vérifier si on appuie sur un bouton
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game.is_playing:
                #Lancer la partie
                if start_button.rect.collidepoint(event.pos):
                    game.start()
                #Quitter la partie
                elif exit_button.rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                #Demander de l'aide
                elif help_button.rect.collidepoint(event.pos):
                    print('OSCOUR')
            #Si c'est le clic gauche
            elif event.button == 1:
                #Si on clique sur le bouton pour accéder au tableau d'indices
                if hint_button.rect.collidepoint(event.pos) and not game.is_speeking:
                    game.is_thinking = not game.is_thinking
                #Sinon on vérifie si on intéragie avce un indice
                else:
                    game.player.check_document_interact(event.pos)
        
        #Si on arrête d'appuyer sur la souris, on arrête l'intéraction avec l'indice
        if event.type == pygame.MOUSEBUTTONUP:
            if game.is_playing:
                game.player.stop_document_interact(event.pos)
        
        #Changer le zoom de la caméra
        if event.type == pygame.MOUSEWHEEL:
            if (2.5 > game.camera_group.zoom_scale + event.y*0.08 > 1) and not (game.is_speeking or game.is_thinking):
                game.camera_group.zoom_scale += event.y * 0.08
    
    #On actualise la clock
    clock.tick(FPS)
