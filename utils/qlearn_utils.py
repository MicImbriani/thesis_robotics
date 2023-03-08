IN_RANGE = 0
TOO_FAR = 1
TOO_CLOSE = -1

def get_spacing_from_dist(dists: dict) -> dict:
    def is_in_range(dist):
        if 3 <= dist <= 7:
            return IN_RANGE
        elif dist < 3:
            return TOO_CLOSE
        else:
            return TOO_FAR

    # Substitute every value of distances with IN_RANGE, TOO_FAR or TOO_CLOSE
    for robot, other_robots in dists.items():
        for k, v in other_robots.items():
            dists[robot][k] = is_in_range(v)
    return dists

