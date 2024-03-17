import player, camera, speech_bubble, pygame
from settings import loadMap
from math import pi

class Game():
    def __init__(self, screen):
        self.is_playing = False
        self.is_speeking = False
        self.is_thinking = False
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
        
        if not self.is_thinking:
            self.camera_group.custom_draw(self.player)
        else:
            self.screen.fill((88, 41, 0))
            for hint in self.player.hints:
                self.screen.blit(hint.image, hint.rect)
                pygame.draw.rect(self.screen, "red", hint.link_rect)
                for link in hint.links:
                    pygame.draw.line(self.screen, "red", hint.link_rect.center, link.link_rect.center)
                if hint.is_linking:
                    pygame.draw.line(self.screen, "red", hint.link_rect.center, pygame.mouse.get_pos())
                
        if self.is_speeking:
            self.speech_bubble.draw()
            
    def check_collisions(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False)