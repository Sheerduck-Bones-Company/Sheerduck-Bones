#Start screen
import pygame as pg
import button

#window
screen_height = 500
screen_width = 800

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Button Demo')

#button img
start_img = pg.image.load('start_button.png').convert_alpha()
exit_img = pg.image.load('exit_button.pgn').convert.alpha()

start_button = button.Button(100, 200, start_img, 0.8)
exit_button = button.Button(450, 200, exit_img, 0.8)
