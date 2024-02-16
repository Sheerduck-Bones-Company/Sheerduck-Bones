import pygame

class Map():
    def __init__(self, game):
        self.image = pygame.image.load('assets/graphics/ground.png')
        self.game = game
        self.screen = game.screen
