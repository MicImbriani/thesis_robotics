import math

#60,30  800,300
ROBOT_SIZE = (15,10) # width x height
MAP_SIZE = (800, 300)
robot_width = 0.01


# SENSORS
n_rays = 9
sensor_dist = 100
sensor_range = (sensor_dist, math.radians(180))
collision_distance = 15


#FORMATION
ideal_dist = 50 #triangle