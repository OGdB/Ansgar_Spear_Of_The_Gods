import pygame
import application

pygame.init()

# pygame.mixer.music.load('rock.mp3')
# pygame.mixer.music.play(-1)

clock = pygame.time.Clock()

map_size_w = 1920
map_size_h = 1080
camera_port_w = 1920
camera_port_h = 1080

App = application.Application(map_size_w, map_size_h, camera_port_w, camera_port_h)
App.run()
