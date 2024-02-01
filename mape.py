import pygame

class Map():
    def __init__(self, game):
        self.image = pygame.image.load('../assets/map.jpeg')
        self.game = game
        self.screen = game.screen
