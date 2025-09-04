import numpy as np
from game_utils import movement_rules_obided, see_each_other


class Hider():
    '''
    1. The default constructor of the base class and input arguments should remain unchanged
    2. The move function must be implemented following the movement rules of movement_rules_obided()
    3. Feel free to add any additional methods or properties that you think would be helpful
    '''

    def __init__(self, game_map, spawn_position, enemy_spawn_position):
        # the default asiggns in the constructor
        self.game_map = game_map
        self.pos = spawn_position
        self.enemy_pos = enemy_spawn_position
        self.enemy_is_visible = see_each_other(game_map, spawn_position, enemy_spawn_position)

    def move(self):

        if self.enemy_is_visible:
            pass

        # Stationary target.
        next_pos = self.pos.copy()

        # Make sure your move function passes this test or the game will force you to stay in place.
        if movement_rules_obided(self.game_map, self.pos, next_pos, player="Hider"):
            self.pos = next_pos
