#!/usr/bin/env python3
import numpy as np
import sys

class Map:
    width = 20
    height = 20

    def __init__(self, seed, build_walls=True):
        # node values indicate is it s wall node (True) or an empty node (False)
        self.seed = seed
        self.nodes = np.zeros((self.width, self.height), dtype=int)
        self.connections = self.initialize_connections()
        if build_walls:
            self.build_walls(seed)

    def initialize_connections(self):
        connections = {}
        for x in range(self.width):
            for y in range(self.height):
                connections[(x, y)] = []

        for x in range(self.width):
            for y in range(self.height):
                if x-1 >= 0:
                    connections[(x, y)].append((x-1, y)) # left
                if x+1 < self.width:
                    connections[(x, y)].append((x+1, y)) # right
                if y+1 < self.height:
                    connections[(x, y)].append((x, y+1)) # down
                if y-1 >= 0:
                    connections[(x, y)].append((x, y-1)) # up
        return connections

    def get_first_empty_node(self, nodes):
        for x in range(self.width):
            for y in range(self.height):
                if not nodes[(x, y)]:
                    return (x, y)
        return None


    # Thanks to https://www.geeksforgeeks.org/dsa/connected-components-in-an-undirected-graph/#approach-1-using-depth-first-search-dfs
    def good_graph_connectivity(self, nodes, connections):
        visited = set()
        start_node = self.get_first_empty_node(nodes)
        if start_node is None:
            raise Exception("Walls are everywhere...")
        self.dfs(start_node, connections, visited)
        return len(visited) == np.sum(nodes == 0)

    def dfs(self, node, connections, visited):
        if node in visited:
            return
        visited.add(node)
        for neighbor in connections[node]:
            if neighbor not in visited:
                self.dfs(neighbor, connections, visited)

    def build_wall_cell(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return
        wall_node = (x, y)

        tmp_nodes = self.nodes.copy()
        tmp_connections = {key:list(l) for key, l in self.connections.items()}


        tmp_nodes[wall_node] = 1 # make a wall
        tmp_connections[wall_node] = []
        # Remove neighbor connections
        if (x-1, y) in tmp_connections:
            while wall_node in tmp_connections[(x-1,y)]: tmp_connections[(x-1,y)].remove(wall_node)
        if (x+1, y) in tmp_connections:
            while wall_node in tmp_connections[(x+1,y)]: tmp_connections[(x+1,y)].remove(wall_node)
        if (x, y-1) in tmp_connections:
            while wall_node in tmp_connections[(x,y-1)]: tmp_connections[(x,y-1)].remove(wall_node)
        if (x, y+1) in tmp_connections:
            while wall_node in tmp_connections[(x,y+1)]: tmp_connections[(x,y+1)].remove(wall_node)
        if not self.good_graph_connectivity(tmp_nodes, tmp_connections):
            # Wall would disconnect the graph. Ignoring the placement.
            return
        self.nodes = tmp_nodes
        self.connections = tmp_connections

    def build_1x1_wall(self, x, y):
        self.build_wall_cell(x, y)
    
    def build_2x2_wall(self, x, y):
        self.build_wall_cell(x, y)
        self.build_wall_cell(x + 1, y)
        self.build_wall_cell(x, y + 1)
        self.build_wall_cell(x + 1, y + 1)

    def build_3x3_wall(self, x, y):
        self.build_wall_cell(x, y)
        self.build_wall_cell(x + 1, y)
        self.build_wall_cell(x, y + 1)
        self.build_wall_cell(x + 1, y + 1)
        self.build_wall_cell(x, y + 2)
        self.build_wall_cell(x + 1, y + 2)
        self.build_wall_cell(x + 2, y)
        self.build_wall_cell(x + 2, y + 1)
        self.build_wall_cell(x + 2, y + 2)

    def build_L_wall(self, x, y):
        self.build_wall_cell(x, y)
        self.build_wall_cell(x, y + 1)
        self.build_wall_cell(x + 1, y + 1)

    def build_Lrot90_wall(self, x, y):
        self.build_wall_cell(x, y)
        self.build_wall_cell(x + 1, y)
        self.build_wall_cell(x, y + 1)

    def build_Lrot180_wall(self, x, y):
        self.build_wall_cell(x, y)
        self.build_wall_cell(x + 1, y)
        self.build_wall_cell(x + 1, y + 1)


    def build_walls(self, seed):
        # IMPROVE: https://www.youtube.com/watch?v=dQw4w9WgXcQ
        build_wall = {"1x1": self.build_1x1_wall,
                    "2x2": self.build_2x2_wall,
                    "3x3": self.build_3x3_wall,
                    "L": self.build_L_wall,
                    "Lrot90": self.build_Lrot90_wall,
                    "Lrot180": self.build_Lrot180_wall
                    }

        rng = np.random.RandomState(seed)
        while self.wall_fraction() < 0.25:
            x = rng.randint(0, self.width)
            y = rng.randint(0, self.height)
            wall_type = rng.choice(list(build_wall.keys()))
            build_wall[wall_type](x, y)

    def wall_fraction(self):
        total_cells = self.width * self.height
        wall_cells = np.sum(self.nodes)
        return wall_cells / total_cells

    def display_map(self):
        print(f"Map is generated with seed {self.seed}. Good connectivity? {self.good_graph_connectivity(self.nodes, self.connections)}. Wall fraction: {self.wall_fraction()}.")
        display = ''
        for y in range(self.height):
            for x in range(self.width):
                if self.nodes[x, y]:
                    display += '#' + " "
                else:
                    display += '.' + " "
            display += '\n'
        print(display)
        print("0 - empty")
        print("1 - wall")



if __name__ == "__main__":
    game_map = Map(seed=int(sys.argv[1]) if len(sys.argv) > 1 else 42)
    game_map.display_map()
