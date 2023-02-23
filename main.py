import pygame
from time import sleep

from dimensions import *
from utils import check_stop_game, update_swarm

from robot import Robot
from graphics import Graphics
from sensor import Ultrasonic
from formation import Formation




# MAP
map = pygame.display.set_mode(MAP_SIZE)

# ROBOTS
robot1 = Robot(map)
robot2 = Robot(map)
robot3 = Robot(map)
swarm = [robot1,robot2, robot3]

# TRAJECTORY/ FORMATION
formation = Formation("line", swarm)

# GRAPHICS
gfx = Graphics(swarm, map, MAP_SIZE, './sprites/robot.png', './sprites/MAP.png')


dt = 0
last_time = pygame.time.get_ticks()

running = True

while running:
    # Check for exit
    running = check_stop_game()

    # Update clock
    dt = (pygame.time.get_ticks() - last_time)/1000
    last_time = pygame.time.get_ticks()

    # Update map
    gfx.map.blit(gfx.map_img, (0,0))



    # ---------------------- Main ----------------------
    update_swarm(swarm, dt)

    gfx.update()
    pygame.display.update()