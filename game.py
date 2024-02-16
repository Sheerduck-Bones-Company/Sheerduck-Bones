import pygame, player, mape, camera, speech_bubble

class Game():
    def __init__(self, screen):
        self.is_playing = False
        self.is_speeking = False
        self.screen = screen
        self.pressed = {}
        self.map = mape.Map(self)
        self.camera_group = camera.Camera()
        self.player = player.Player(self, (640,360), self.camera_group)
        
    def start(self):
        self.is_playing = True

    def stop(self):
        self.is_playing = False
        
    def say(self, text):
        self.speech_bubble = speech_bubble.SpeechBubble(self, text)
        self.speech_bubble.initialize()

    def update(self):
        self.screen.fill('#71ddee')
        self.camera_group.update()
        self.camera_group.custom_draw(self.player)
        if self.is_speeking:
            self.speech_bubble.draw()