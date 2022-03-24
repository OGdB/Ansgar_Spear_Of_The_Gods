import pygame
import application

pygame.init()

screen_w = 480
screen_h = 320
clock = pygame.time.Clock()
App = application.Application(screen_w, screen_h)
App.run()
