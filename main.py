#!/usr/bin/env python3
import sys
import numpy as np
import time
import argparse
from map import Map
from game_utils import see_each_other, movement_rules_obided, get_seeker_spawn, get_hider_spawn, display_game_state
from seeker import Seeker
from hider import Hider


def main(game_seed=None, map_seed=None, interactive=False):
    start_time = time.time()
    winner, score = "", 0

    seeker_thinking_time = 0
    hider_thinking_time = 0

    if game_seed is None:
        np.random.seed(np.random.randint(0, 1000000))
    else:
        np.random.seed(game_seed)

    if map_seed is None:
        game_map = Map(seed=np.random.randint(0, 1000000))
    else:
        game_map = Map(seed=map_seed)

    seeker_spawn = get_seeker_spawn(game_map)
    hider_spawn = get_hider_spawn(game_map, seeker_spawn)

    t1 = time.time()
    seeker = Seeker(game_map, spawn_position=seeker_spawn, enemy_spawn_position=hider_spawn)
    t2 = time.time()
    seeker_thinking_time += t2 - t1

    t1 = time.time()
    hider = Hider(game_map, spawn_position=hider_spawn, enemy_spawn_position=seeker_spawn)
    t2 = time.time()
    hider_thinking_time += t2 - t1

    n_steps = 10 * game_map.width * game_map.height  # x10 game map size = 4000
    for step in range(n_steps):
        if interactive:
            display_game_state(game_map, seeker.pos, hider.pos, step)
            input("Press Enter to continue...")

        if step == 0:
            assert(seeker.pos[0] == seeker_spawn[0] and seeker.pos[1] == seeker_spawn[1]), "Seeker did not spawn at the correct location"
            assert(hider.pos[0] == hider_spawn[0] and hider.pos[1] == hider_spawn[1]), "Hider did not spawn at the correct location"

        seeker_old_pos = seeker.pos

        if see_each_other(game_map, seeker.pos, hider.pos) == (True, (None, None)):
            seeker.enemy_pos = hider.pos
            seeker.enemy_is_visible = True
            hider.enemy_pos = seeker.pos
            hider.enemy_is_visible = True


        t1 = time.time()
        seeker.move()
        t2 = time.time()
        seeker_thinking_time += t2 - t1

        if not movement_rules_obided(game_map, seeker_old_pos, seeker.pos, player="Seeker"):
            seeker.pos = seeker_old_pos

        if seeker.pos[0] == hider.pos[0] and seeker.pos[1] == hider.pos[1]:
            print(f"Seeker caught the Hider in {step} steps.")
            winner, score = "Seeker", step
            break

        if step % 2 == 1:
            hider_old_pos = hider.pos

            t1 = time.time()
            hider.move()
            t2 = time.time()
            hider_thinking_time += 2*(t2 - t1) # factor of 2 for hider because algorithm idle every other turn

            if not movement_rules_obided(game_map, hider_old_pos, hider.pos, player="Hider"):
                hider.pos = hider_old_pos


        elapsed_time = time.time() - start_time
        if elapsed_time > 300:
            print("\n *** GAME OVER *** \n")
            print("Game over: 5 minutes time limit is exceeded")
            print(f"Seeker thinking time: {seeker_thinking_time:.2f} seconds ( {seeker_thinking_time / elapsed_time * 100 if elapsed_time > 0 else 0:.2f}%)")
            print(f"Hider thinking time: {hider_thinking_time:.2f} seconds ( {hider_thinking_time / elapsed_time * 100 if elapsed_time > 0 else 0:.2f}%)")
            if seeker_thinking_time < hider_thinking_time:
                print("Seeker was more efficient than Hider.")
                winner, score = "Seeker", 1
            else:
                print("Hider was more efficient than Seeker.")
                winner, score = "Hider", n_steps

            break

    else:
        winner, score = "Hider", n_steps

    print("\n *** GAME OVER *** \n")
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    print(f"Winner: {winner}, Score: {score}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-gs',"--game_seed", type=int, default=None)
    parser.add_argument('-ms',"--map_seed", type=int, default=None)
    parser.add_argument('-i',"--interactive", action='store_true', default=False)
    args = parser.parse_args()
    main(game_seed=args.game_seed, map_seed=args.map_seed, interactive=args.interactive)