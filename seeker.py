import numpy as np
from game_utils import movement_rules_obided, see_each_other

class Seeker():
    '''
    1. The default constructor of the base class and input arguments should remain unchanged
    2. The move function must be implemented following the movement rules of movement_rules_obided()
    3. Feel free to add any additional methods or properties that you think would be helpful
    '''
    def __init__(self, game_map, spawn_position, enemy_spawn_position):
        # these are default assigns in the constructor
        self.game_map = game_map
        self.pos = spawn_position
        self.enemy_pos = enemy_spawn_position
        self.enemy_is_visible = see_each_other(game_map, spawn_position, enemy_spawn_position)

        self.path_to_victory = self.find_bfs_path(spawn_position, enemy_spawn_position)


    def find_bfs_path(self, start_pos, goal_pos):
        # thanks to https://www.youtube.com/watch?v=rbYxbIMOZkE
        queue = []
        visited = {}
        queue.append({'pos':start_pos, 'last_pos':None})

        max_iters = 10000 # for safety
        while len(queue) > 0 and max_iters > 0:
            item = queue.pop(0)
            pos = item['pos']
            last_pos = item['last_pos']

            in_bounds = pos[0] >= 0 and pos[0] < self.game_map.width and pos[1] >= 0 and pos[1] < self.game_map.height
            if not in_bounds:
                continue # cannot move there
            is_wall = self.game_map.nodes[pos[0], pos[1]] == 1
            if is_wall:
                continue # cannot move there

            if (pos[0], pos[1]) in visited:
                continue

            visited[(pos[0], pos[1])] = last_pos # Keep track of the path

            if pos[0] == goal_pos[0] and pos[1] == goal_pos[1]:
                break

            queue.append({'pos':(pos[0]+1, pos[1]), 'last_pos':pos})
            queue.append({'pos':(pos[0]-1, pos[1]), 'last_pos':pos})
            queue.append({'pos':(pos[0], pos[1]+1), 'last_pos':pos})
            queue.append({'pos':(pos[0], pos[1]-1), 'last_pos':pos})
            max_iters -= 1

        backtraced_path = []
        current_pos = goal_pos
        while (current_pos[0], current_pos[1]) in visited and visited[(current_pos[0], current_pos[1])] is not None:
            backtraced_path.append(current_pos)
            current_pos = visited[(current_pos[0], current_pos[1])]
        backtraced_path.append((start_pos[0], start_pos[1]))

        backtraced_path.reverse()
        print("BFS path from", start_pos, "to", goal_pos, "is:", backtraced_path)
        return backtraced_path

    def move(self):
        if self.enemy_is_visible:
            print("Seeker sees the Hider at position:", self.enemy_pos)

        try:
            idx = self.path_to_victory.index(tuple(self.pos))
        except ValueError:
            print("Oops...")
            # my position is not on the planned path... Something went wrong. Remain in place and accept defeat.
            return

        if idx == len(self.path_to_victory) - 1:
            # I am on my end goal, but there is no hider :( Stay sad here until game is over.
            return
        next_pos = self.path_to_victory[idx+1]

        # Make sure your move function passes this test or you will simply stay at the same place.
        if movement_rules_obided(self.game_map, self.pos, next_pos, player="Seeker"):
            self.pos = next_pos
