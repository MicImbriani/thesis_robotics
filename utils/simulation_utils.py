import matplotlib as plt
def make_plots(formation, robots) -> None:
    """ Plots the distances between robots over time.
    """
    distances = formation.dists
    distances_log = get_distances_log(robots)
    r01 = distances_log[0][1]
    r02 = distances_log[0][2]
    r12 = distances_log[1][2]
    length = len(r01)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(range(length), [val-distances[(0, 1)]
            for val in r01], color='tab:blue')
    ax.plot(range(length), [val-distances[(0, 2)]
            for val in r02], color='tab:green')
    ax.plot(range(length), [val-distances[(1, 2)]
            for val in r12], color='tab:red')

    plt.savefig("lol.png")






# GAME STATE
def get_distances_log(swarm):
    final = {}
    for robot in swarm:
        final[robot.id] = robot.distances_log
    return final

import pygame
def check_stop_game():
    """Returns true if game needs to be stopped. """
    running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = True
    return running
