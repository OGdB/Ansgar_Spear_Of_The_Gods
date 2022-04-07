import pygame
import application
import main_menu

pygame.init()

screen_w = 1920
screen_h = 1080

pygame.mixer.music.load('rock.mp3')
pygame.mixer.music.play(-1)

start = main_menu.Start_screen(screen_w, screen_h)
start.run()
App = application.Application(screen_w, screen_h)
if start.done == True:
    App.clock.tick()
    App.run()
