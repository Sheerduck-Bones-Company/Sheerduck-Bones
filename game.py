import player, mape, camera, speech_bubble

class Game():
    def __init__(self, screen):
        self.is_playing = False
        self.is_speeking = False
        self.screen = screen
        self.pressed = {}
        self.map = mape.Map(self)
        self.camera_group = camera.Camera()
        self.player = player.Player(self, (640,360), self.camera_group)
    
    #Lancer la partie    
    def start(self):
        self.is_playing = True

    #Arrêter la partie
    def stop(self):
        self.is_playing = False
    
    #Lancer une boîte de dialogue
    def say(self, text):
        self.speech_bubble = speech_bubble.SpeechBubble(self, text)
        self.speech_bubble.initialize()

    #Actualiser la partie
    def update(self):
        self.camera_group.update()
        self.camera_group.custom_draw(self.player)
        if self.is_speeking:
            self.speech_bubble.draw()