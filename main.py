import pygame
from time import sleep
import matplotlib.pyplot as plt

from utils.dimensions import *
from utils.utils import check_stop_game, update_swarm, get_distances_log

from robots.robot import Robot
from robots.robot_distance import DistanceRobot
from graphics import Graphics
from sensor import Ultrasonic
from formation import Formation




# MAP
map = pygame.display.set_mode(MAP_SIZE)

# ROBOTS
robot1 = DistanceRobot(map)
robot2 = Robot(map)
robot3 = DistanceRobot(map)
# robot4 = DistanceRobot(map)
swarm = [robot1,robot2, robot3]
for robot in swarm:
    robot.other_robots = [x for x in swarm if x is not robot]
    print(robot.other_robots)

# TRAJECTORY/ FORMATION
formation = Formation("triangle", swarm)

# GRAPHICS
gfx = Graphics(swarm, map, MAP_SIZE, './sprites/robot.png', './sprites/MAP_empty.png')


dt = 0
last_time = pygame.time.get_ticks()

running = True

while running:
    # Check for exit
    running = check_stop_game()
    if not running:
        break

    # Update clock
    dt = (pygame.time.get_ticks() - last_time)/1000
    last_time = pygame.time.get_ticks()

    # Update map
    gfx.map.blit(gfx.map_img, (0,0))



    # ---------------------- Main ----------------------
    update_swarm(swarm, dt)

    gfx.update()
    pygame.display.update()

distances = formation.dists
distances_log = get_distances_log(swarm)
r01 = distances_log[0][1]
r02 = distances_log[0][2]
r12 = distances_log[1][2]
length = len(r01)
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(range(length), [val-distances[(0,1)] for val in r01], color='tab:blue')
ax.plot(range(length), [val-distances[(0,2)] for val in r02], color='tab:green')
ax.plot(range(length), [val-distances[(1,2)] for val in r12], color='tab:red')

plt.savefig("lol.png")