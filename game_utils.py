import numpy as np

def distance(pos1, pos2):
    # https://en.wikipedia.org/wiki/Taxicab_geometry
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def movement_rules_obided(game_map, old_pos, new_pos, player="Player"):
    # NOTE: only +1 move is allowed
    # NOTE: no climbing walls or going out of bounds

    if distance(old_pos, new_pos) > 1:
        print(f"WARNING: {player} tried to move too far in one step. Staying still.")
        return False

    if game_map.nodes[new_pos[0], new_pos[1]] == 1:
        print(f"WARNING: {player} tried to move into a wall. Staying still.")
        return False

    if new_pos[0] < 0 or new_pos[0] >= game_map.width or new_pos[1] < 0 or new_pos[1] >= game_map.height:
        print(f"WARNING: {player} tried to move out of bounds. Staying still.")
        return False
    return True

def get_seeker_spawn(game_map):
    empty_nodes = np.argwhere(game_map.nodes == 0)
    return empty_nodes[np.random.choice(empty_nodes.shape[0])]


def get_hider_spawn(game_map, seeker_spawn):
    empty_nodes = np.argwhere(game_map.nodes == 0)

    # get the corner of the seeker spawn
    seeker_spawn_lt = seeker_spawn[0] < game_map.width // 2 and seeker_spawn[1] < game_map.height // 2
    seeker_spawn_rt = seeker_spawn[0] >= game_map.width // 2 and seeker_spawn[1] < game_map.height // 2
    seeker_spawn_lb = seeker_spawn[0] < game_map.width // 2 and seeker_spawn[1] >= game_map.height // 2
    seeker_spawn_rb = seeker_spawn[0] >= game_map.width // 2 and seeker_spawn[1] >= game_map.height // 2

    for _ in range(1000000):  # avoid infinite loop, should be enough
        hider_spawn = empty_nodes[np.random.choice(empty_nodes.shape[0])]

        # get the corner of the potential hider spawn
        hider_spawn_lt = hider_spawn[0] < game_map.width // 2 and hider_spawn[1] < game_map.height // 2
        hider_spawn_rt = hider_spawn[0] >= game_map.width // 2 and hider_spawn[1] < game_map.height // 2
        hider_spawn_lb = hider_spawn[0] < game_map.width // 2 and hider_spawn[1] >= game_map.height // 2
        hider_spawn_rb = hider_spawn[0] >= game_map.width // 2 and hider_spawn[1] >= game_map.height // 2

        spawned_in_opposite_corners = (seeker_spawn_lt and hider_spawn_rb) or \
                                      (seeker_spawn_rt and hider_spawn_lb) or \
                                      (seeker_spawn_lb and hider_spawn_rt) or \
                                      (seeker_spawn_rb and hider_spawn_lt) 

        if spawned_in_opposite_corners and distance(seeker_spawn, hider_spawn) >= 3:
            return hider_spawn
    raise ValueError("Could not find a valid hider spawn position.")


def see_each_other(game_map, seeker_pos, hider_pos):
    if distance(seeker_pos, hider_pos) == 0:
        raise ValueError("Seeker and Hider are at the same position. Should never happen at this point!")


    if seeker_pos[0] == hider_pos[0]:
        # Special case. Same column, vertical line, infinite slope
        for y in range(min(seeker_pos[1], hider_pos[1]) + 1, max(seeker_pos[1], hider_pos[1])):
            if game_map.nodes[seeker_pos[0], y] == 1:
                print("Found a blocking wall on the line of sight. No vision.")
                return False
        return True

    seeker_is_left = seeker_pos[0] < hider_pos[0]
    x_left = seeker_pos[0] if seeker_is_left else hider_pos[0]
    x_right = hider_pos[0] if seeker_is_left else seeker_pos[0]
    y_left = seeker_pos[1] if seeker_is_left else hider_pos[1]

    slope = (hider_pos[1] - seeker_pos[1]) / (hider_pos[0] - seeker_pos[0])

    step = 0.01 # should be small enough
    x_range = np.arange(x_left, x_right+step, step, dtype=float)
    y_range = y_left + slope * (x_range - x_left)

    nodes_to_check = []
    for x, y in zip(x_range, y_range):
        # This is the perfect middle between the two tiles. Need to check both tiles
        if np.isclose(x % 1, 0.5):
            node1 = (round(x-0.5), round(y))
            node2 = (round(x+0.5), round(y))
            if node1 not in nodes_to_check:
                nodes_to_check.append(node1)
            if node2 not in nodes_to_check:
                nodes_to_check.append(node2)

        # This is the perfect middle between the two tiles. Need to check both tiles
        if np.isclose(y % 1, 0.5):
            node1 = (round(x), round(y-0.5))
            node2 = (round(x), round(y+0.5))
            if node1 not in nodes_to_check:
                nodes_to_check.append(node1)
            if node2 not in nodes_to_check:
                nodes_to_check.append(node2)

        # Otherwise just add the node we are in.
        node = (round(x), round(y))
        if node not in nodes_to_check:
            nodes_to_check.append(node)

    for node in nodes_to_check:
        x, y = node
        if game_map.nodes[x, y] == 1:
            # print("Found a blocking wall on the line of sight. No vision.")
            return False

    # print("No walls found on the line of sight.")
    return True

