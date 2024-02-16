#Start screen
import pygame as pg
import sys

pg.init()

#button class
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(width * scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def draw(self):
        action = False
        #mouse position
        pos = pg.mouse.get_pos()

        
        #mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                
        if pg.mouse.get_pressed()[0] == 0:
                self.clicked = False
        
        #draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        return action

#window
desktop_size = pg.display.get_desktop_sizes()[0]
screen = pg.display.set_mode(desktop_size)
pg.display.set_caption('Welcome to Coin Coin Ville')

#button img
start_img_original = pg.image.load('start_button.png').convert_alpha()
exit_img_original = pg.image.load('exit_button.png').convert_alpha()
help_img_original = pg.image.load('help_button.png').convert_alpha()


start_img = pg.transform.scale(start_img_original, (500,200))
exit_img = pg.transform.scale(exit_img_original, (450,200))
help_img = pg.transform.scale(help_img_original, (200,150))


#button position
desktop_size_list = list(desktop_size)
start_button = Button(100, int(desktop_size_list[1]) - 300, start_img, 0.8)
exit_button = Button(int(desktop_size_list[0]) - 800, int(desktop_size_list[1]) - 300, exit_img, 0.8)
help_button = Button(int(desktop_size_list[0]) - 200, int(desktop_size_list[1]) - 290, help_img, 0.8)

#Background
#bg_img = pg.image.load('background.png').convert_alpha()


#game loop
run = True
while run:
    
    screen.fill((88, 41, 0))
    #screen.blit(bg_img, (0,0))

    if start_button.draw():
        print('START')
    if help_button.draw():
        print('HELP')
    if exit_button.draw():
        run = False
        print('EXIT')
    #exit_button.draw()
    
    pg.display.update()
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            pg.quit()
            sys.exit()

pg.quit()
sys.exit()


        
