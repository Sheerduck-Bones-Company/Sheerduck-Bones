import pygame, obstacles, random, sys
from game import Game

pygame.init()
pygame.display.set_caption('Sheerduck-Bones')
pygame.display.set_icon(pygame.image.load('assets/graphics/Sheerduck_Bones-down-left.png'))
screen = pygame.display.set_mode((1080, 720), pygame.SCALED)
clock = pygame.time.Clock()
FPS = 60
pygame.event.set_grab(True)

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
        game.start()
        
    pygame.display.update()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
            
            if event.key == pygame.K_ESCAPE:
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
        
        if event.type == pygame.MOUSEWHEEL:
            if (2.5 > game.camera_group.zoom_scale + event.y > 0) and not game.is_speeking:
                game.camera_group.zoom_scale += event.y * 0.08
    
    clock.tick(FPS)