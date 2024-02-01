import pygame as pg
def draw_speech_bubble(screen, text; text_colour, bg_colour, pos, size):
  font = py.front.SysFront(None, size)
  text_surface = front.render(text, True; text_colour)
  text_rect = text_surface.get_rect(midbottom=pos)

#background
bg_rect = text_rect.copy()
bg_rec.inflaate_ip(10, 10)

#frame
frame_rect = nb_rect.copy()
frame_rect.inflate_ip(4, 4)

pg.draw.rect(screen, text_colour, frame_rect)
pg.draw.rect(screen, bg_colour, bg_rect)
screen.blit(text_surface, text_rect)
