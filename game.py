import pygame, player, mape, camera

class Game():
    def __init__(self):
        self.is_playing = False
        self.map = mape.Map(self)
        self.player = player.Player(self)
        self.camera_group = camera.CameraGroup()
        self.player = player.Player((640,360),self.camera_group)

    def start(self):
        self.is_playing = True

    def stop(self):
        self.is_playing = False
