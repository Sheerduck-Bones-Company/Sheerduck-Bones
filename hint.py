import pygame

class Hint():
    def __init__(self, hint):
        self.type = hint
        self.image = pygame.image.load(f"assets/graphics/hints/{hint}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100,100))
        self.rect = self.image.get_rect(topleft=(10,10))
        self.link_rect = self.image.get_rect(left=self.rect.centerx-15, top=self.rect.y+10, width=30, height=30)
        self.offset = pygame.Vector2((0,0))
        self.is_linking = False
        self.links = []
    
    def touch_dot_link(self, pos):
        return self.link_rect.collidepoint(pos)
    
    def is_caught(self, pos):
        return self.rect.collidepoint(pos)
    
    def clear_touched_link(self, pos):
        for link in self.links:
            l1_vect = pygame.Vector2(self.link_rect.centerx-pos[0], self.link_rect.centery-pos[1])
            l2_vect = pygame.Vector2(link.link_rect.centerx-pos[0], link.link_rect.centery-pos[1])
            l3_vect = pygame.Vector2(self.link_rect.centerx-link.link_rect.centerx, self.link_rect.centery-link.link_rect.centery)
            
            if l2_vect.x != 0 and l2_vect.y != 0:
                if l1_vect.x/l2_vect.x < 0 and l1_vect.y/l2_vect.y < 0 and abs(l1_vect.x*l3_vect.y-l1_vect.y*l3_vect.x) < 3000:
                    self.links.remove(link)
    
    def set_offset(self, pos):
        self.offset = pygame.Vector2(self.rect.topleft) - pygame.Vector2(pos)
        
    def track_mouse(self):
        self.rect.topleft = pygame.Vector2(pygame.mouse.get_pos()) + self.offset
        
        if self.rect.left < 0 :
            self.rect.left = 0
        elif self.rect.right > 1080:
            self.rect.right = 1080
            
        if self.rect.top < 0 :
            self.rect.top = 0
        elif self.rect.bottom > 720:
            self.rect.bottom = 720
            
        self.link_rect = self.image.get_rect(left=self.rect.centerx-15, top=self.rect.y+10, width=30, height=30)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.circle(screen, "red", self.link_rect.center, self.link_rect.width/2)
        
    def draw_links(self, screen):
        for link in self.links:
            pygame.draw.line(screen, "red", self.link_rect.center, link.link_rect.center)