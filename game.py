import pygame
import player
import mape

class Game():
    def __init__(self):
        self.is_playing = False
        self.map = mape.Map(self)
        self.player = player.Player(self)

    def start(self):
        self.is_playing = True
    
    def stop(self):
        self.is_playing = False
