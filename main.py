import pygame, obstacles, random, sys, start_screen
from game import Game

pygame.init()
pygame.display.set_caption('Sheerduck-Bones')
pygame.display.set_icon(pygame.image.load('assets/graphics/Sheerduck_Bones-down-left.png'))
screen_width, screen_height = 1080, 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.SCALED)
clock = pygame.time.Clock()
FPS = 60
pygame.event.set_grab(True)

#button img
'''start_img = pygame.transform.scale(start_img, (500,200))
exit_img = pygame.transform.scale(exit_img, (450,200))
help_img = pygame.transform.scale(help_img, (200,150))
'''

#button position
start_button = start_screen.Button(screen, 30, -20, 'start', 10)
exit_button = start_screen.Button(screen, -30, -20, 'exit', 10)
help_button = start_screen.Button(screen, -10, 20, 'help', 10)

# setup
game = Game(screen)

for i in range(20):
    x, y = random.randint(1000,2000), random.randint(1000,2000)
    obstacles.Tree(((x//4)*4+2, (y//4)*4+2),game.camera_group)

running = True

while running:
    if game.is_playing:
        game.update()
    else:
        screen.fill((88, 41, 0)) 
        start_button.draw()
        exit_button.draw()
        help_button.draw()
        
    pygame.display.update()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
            
            if event.key == pygame.K_ESCAPE:
                if game.is_playing:
                    game.stop()
                else:
                    running = False
                    pygame.quit()
                    sys.exit()
                
            if event.key == pygame.K_e:
                if game.is_speeking:
                    game.speech_bubble.update()
                else:
                    game.is_speeking = True
                    game.say(['Bonjour je suis Antoine et je voudrais du chocolat ! Je suis vraiment quelqu\'un de très gourmand qui a du mal a se controler pour manger des choses sucrée',
                              'Je mappelle Jean pierre et je fais des bêtises tout plein tout plein beaucoup',
                              'Suis',
                              'Antoine'])
            
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
        
        if event.type == pygame.KEYUP:
            game.pressed[event.key] = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game.is_playing:
                if start_button.rect.collidepoint(event.pos):
                    game.start()
                elif exit_button.rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif help_button.rect.collidepoint(event.pos):
                    print('OSCOUR')
        
        if event.type == pygame.MOUSEWHEEL:
            if (2.5 > game.camera_group.zoom_scale + event.y > 0) and not game.is_speeking:
                game.camera_group.zoom_scale += event.y * 0.08
    
    clock.tick(FPS)