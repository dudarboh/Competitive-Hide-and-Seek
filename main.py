#!/usr/bin/env python3
import sys
import numpy as np
import time
from map import Map
from seeker import Seeker
from hider import Hider
from game_utils import see_each_other, movement_rules_obided, get_seeker_spawn, get_hider_spawn


def main(game_seed=None, map_seed=None):
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
    print("Seeker spawn location:", seeker_spawn)

    hider_spawn = get_hider_spawn(game_map, seeker_spawn)
    print("Hider spawn location:", hider_spawn)

    game_map.display_map(seeker_spawn, hider_spawn)

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
        print(f"Step {step}:")
        if step == 0:
            assert(seeker.pos[0] == seeker_spawn[0] and seeker.pos[1] == seeker_spawn[1]), "Seeker did not spawn at the correct location"
            assert(hider.pos[0] == hider_spawn[0] and hider.pos[1] == hider_spawn[1]), "Hider did not spawn at the correct location"

        seeker_old_pos = seeker.pos

        if see_each_other(game_map, seeker.pos, hider.pos):
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


        game_map.display_map(seeker.pos, hider.pos)

        elapsed_time = time.time() - start_time
        if elapsed_time > 300:
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

        # Uncomment to watch the game step by step
        # input("wait")

    else:
        print(f"Wow, hider managed to hide for {n_steps} steps!")
        winner, score = "Hider", n_steps


    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    print(f"Winner: {winner}, Score: {score}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
    elif len(sys.argv) == 2:
        main(game_seed=int(sys.argv[1]))
    elif len(sys.argv) == 3:
        main(game_seed=int(sys.argv[1]), map_seed=int(sys.argv[2]))