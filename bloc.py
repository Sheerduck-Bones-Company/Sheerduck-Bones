import pygame

#On crée une classe permettant de gérer les blocs
class Bloc(pygame.sprite.Sprite):
    def __init__(self,
                    bloc_type:str,
                    top_left:tuple = (0,0),
                    big = False,
                    is_above_player = False,
                    is_in_group = False,
                    collisions = [False, False, False, False],
                    libraryx = 0,
                    libraryy = 0):
        super().__init__()
        self.type = bloc_type
        self.big = big
        self.set_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = top_left
        self.is_above_player = is_above_player
        self.is_in_group = is_in_group
        self.collisions = [elem for elem in collisions]
        self.libraryx = libraryx
        self.libraryy = libraryy
    
    #Définir l'image du bloc
    def set_image(self):
        self.image = pygame.image.load(f"assets/graphics/blocs/{self.type}.png").convert_alpha()
        self.info_surface = pygame.Surface((16,16))
        if self.big:
            self.image = pygame.transform.scale(self.image, (64,64))
            self.info_surface = pygame.Surface((64,64))
        self.info_surface.set_alpha(60)
    
    #Récupérer les collisions
    def get_booleans(self):
        return self.is_above_player, self.collisions
    
    #Dessiner les collisions
    def draw_collisions(self):
        for i, collision in enumerate(self.collisions):
            if collision:
                color = (255,0,0)
            else:
                color = (255,255,255)
            pygame.draw.rect(self.info_surface, color, pygame.Rect((i*8)%16, (i//2)*8, 8, 8))
    
    def draw_group(self):   
        if self.is_in_group:
            pygame.draw.rect(self.info_surface, (0,255,0), pygame.Rect(0, 0, 16, 16))
        else:
            pygame.draw.rect(self.info_surface, (255,0,0), pygame.Rect(0, 0, 16, 16))
            
    def draw_is_above(self):
        if self.is_above_player:
            pygame.draw.rect(self.info_surface, (0,255,0), pygame.Rect(0, 0, 16, 16))
        else:
            pygame.draw.rect(self.info_surface, (255,0,0), pygame.Rect(0, 0, 16, 16))