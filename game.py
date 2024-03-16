import player, camera, speech_bubble, pygame
from settings import loadMap

class Game():
    def __init__(self, screen):
        self.is_playing = False
        self.is_speeking = False
        self.screen = screen
        self.pressed = {}
        self.player = player.Player(self, (640,360))
        self.maps = loadMap(self.player)
        self.current_map_name = "test.txt"
        self.camera_group = camera.Camera(self)
        self.current_step = 1
    
    #Lancer la partie    
    def start(self):
        self.is_playing = True

    #Arrêter la partie
    def stop(self):
        self.is_playing = False
    
    #Lancer une boîte de dialogue
    def say(self, text:list):
        if self.is_speeking:
            self.speech_bubble.update()
        else:
            self.speech_bubble = speech_bubble.SpeechBubble(self, text)
            self.speech_bubble.initialize()
            self.is_speeking = True

    #Actualiser la partie
    def update(self):
        for group in self.maps.get(self.current_map_name).get("group_list"):
            group.update()
        
        self.camera_group.custom_draw(self.player)
        if self.is_speeking:
            self.speech_bubble.draw()
            
    def check_collisions(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False)