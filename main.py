#On importe les modules nécessaires
import pygame, obstacles, random, sys, button
from game import Game

#On initialise la fenêtre
pygame.init()
pygame.display.set_caption('Sheerduck-Bones')
pygame.display.set_icon(pygame.image.load('assets/graphics/icons/game.ico'))

#On crée notre écran
screen_width, screen_height = 1080, 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.SCALED)

#On crée notre clock
clock = pygame.time.Clock()
FPS = 60

#On crée les boutons de démarage
start_button = button.Button(screen, 'start', 30, -20, 10)
exit_button = button.Button(screen, 'exit', -30, -20, 10)
help_button = button.Button(screen, 'help', -10, 20, 10)

#On crée notre partie
game = Game(screen)

running = True

#On lance la boucle principale
while running:
    if game.is_playing:
        #On actualise la partie
        game.update()
    else:
        #On affiche l'écran d'accueil
        screen.fill((88, 41, 0))
        start_button.draw()
        exit_button.draw()
        help_button.draw()
    
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
            
            #Activer la boîte de dialogue    
            if event.key == pygame.K_e:
                if game.is_speeking:
                    game.speech_bubble.update()
                else:
                    game.is_speeking = True
                    game.say(['Bonjour je suis Antoine et je voudrais du chocolat ! Je suis vraiment quelqu\'un de très gourmand qui a du mal a se controler pour manger des choses sucrée',
                              'Je mappelle Jean pierre et je fais des bêtises tout plein tout plein beaucoup',
                              'Suis',
                              'Antoine'])
            
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
        
        #Changer le zoom de la caméra
        if event.type == pygame.MOUSEWHEEL:
            if (2.5 > game.camera_group.zoom_scale + event.y > 0) and not game.is_speeking:
                game.camera_group.zoom_scale += event.y * 0.08
    
    #On actualise la clock
    clock.tick(FPS)