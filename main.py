import pygame
import application
import main_menu

pygame.init()

map_size_w = 1920
map_size_h = 1080
camera_port_w = 1920/4
camera_port_h = 1080/4

start = main_menu.Start_screen(map_size_w, map_size_h)
start.run()

App = application.Application(map_size_w, map_size_h, camera_port_w, camera_port_h)
if start.done == True and start.playing == True:
    App.clock.tick()
    App.run()
