import json
import os

from cubie import CubieCube, MOVE_CUBE

class PruningTable:
    """Helper class to use pruning on the tables"""
    def __init__(self, table, stride):
        self.table = table
        self.stride = stride

    def __getitem__(self, x):
        return self.table[x[0] * self.stride + x[1]]
    

class Tables:
    tables_loaded = False

    # Variables to hold the number of permutations of different cube moves
    
    # 8 corner pieces can be oriented 3 ways so
    # 3^7 possible corner orientations
    TWIST = 2187
    # 12 edge piece can be flipped 2 ways so
    # 2^11 possible edge flips
    FLIP = 2048
    # 4 edge pieces can be in any of 12 edge positions so
    # 12C4 possible positions of FR, FL, BL, BR
    UDSLICE = 495
    # 4! possible permutations of FR, FL, BL, BR
    EDGE4 = 24
    # 8! possible permutations of UR, UF, UL, UB, DR, DF, DL, DB (phase two)
    EDGE8 = 40320
    # 8! possible permutations of the corners
    CORNER = 40320
    # 12! possible permutations of the edges
    EDGE = 479001600
    # 6 moves can be turned 3 ways (once clockwise, once counterclockwise, and twice)
    # 6*3 possible moves
    MOVES = 18

    def __init__(self):
        if not self.tables_loaded:
            pass
            self.load_tables()

    
    def load_tables(self):
        if os.path.isfile("tables.json"):
            with open("tables.json", "r") as file:
                tables = json.load(file)
            self.twist_move = tables["twist_move"]
            self.flip_move = tables["flip_move"]
            self.udslice_move = tables["udslice_move"]
            self.edge4_move = tables["edge4_move"]
            self.edge8_move = tables["edge8_move"]
            self.corner_move = tables["corner_move"]
            self.udslice_twist_prune = PruningTable(tables["udslice_twist_prune"], self.TWIST)
            self.udslice_flip_prune = PruningTable(tables["udslice_flip_prune"], self.FLIP)
            self.edge4_edge8_prune = PruningTable(tables["edge4_edge8_prune"], self.EDGE8)
            self.edge4_corner_prune = PruningTable(tables["edge4_corner_prune"], self.CORNER)

        else:
            # ----------  Phase 1 move tables  ---------- #
            self.twist_move = self.make_twist_table()
            self.flip_move = self.make_flip_table()
            self.udslice_move = self.make_udslice_table()

            # ----------  Phase 2 move tables  ---------- #
            self.edge4_move = self.make_edge4_table()
            self.edge8_move = self.make_edge8_table()
            self.corner_move = self.make_corner_table()

            # ----------  Phase 1 pruning tables  ---------- #
            self.udslice_twist_prune = self.make_udslice_twist_prune()
            self.udslice_flip_prune = self.make_udslice_flip_prune()

            # --------  Phase 2 pruning tables  ---------- #
            self.edge4_edge8_prune = self.make_edge4_edge8_prune()
            self.edge4_corner_prune = self.make_edge4_corner_prune()

            tables = {
                "twist_move": self.twist_move,
                "flip_move": self.flip_move,
                "udslice_move": self.udslice_move,
                "edge4_move": self.edge4_move,
                "edge8_move": self.edge8_move,
                "corner_move": self.corner_move,
                "udslice_twist_prune": self.udslice_twist_prune.table,
                "udslice_flip_prune": self.udslice_flip_prune.table,
                "edge4_edge8_prune": self.edge4_edge8_prune.table,
                "edge4_corner_prune": self.edge4_corner_prune.table,
            }
            with open("tables.json", "w") as file:
                json.dump(tables, file)

        self.tables_loaded = True
    


    def make_twist_table(self):
        """Move table for the twists of the 8 corners"""
        twist_move = [[0 for _ in range(self.MOVES)] for _ in range(self.TWIST)]
        cube = CubieCube()
        for i in range(self.TWIST):
            cube.set_twist(i)
            for j in range(6):
                for k in range(3):
                    cube.corner_multiply(MOVE_CUBE[j])
                    twist_move[i][3 * j + k] = cube.get_twist()
                cube.corner_multiply(MOVE_CUBE[j])
        return twist_move
    
    def make_flip_table(self):
        """Move table for the flip of the 12 edges"""
        flip_move = [[0 for _ in range(self.MOVES)] for _ in range(self.FLIP)]  
        cube = CubieCube()
        for i in range(self.FLIP):
            cube.set_flip(i)
            for j in range(6):
                for k in range(3):
                    cube.edge_multiply(MOVE_CUBE[j])
                    flip_move[i][3 * j + k] = cube.get_flip()
                cube.edge_multiply(MOVE_CUBE[j])
        return flip_move

    def make_udslice_table(self):
        """Move table for the four UD-slice edges FR, FL, BL and BR"""
        udslice_move = [[0 for _ in range(self.MOVES)] for _ in range(self.UDSLICE)]
        cube = CubieCube()
        for i in range(self.UDSLICE):
            cube.set_udslice(i)
            for j in range(6):
                for k in range(3):
                    cube.edge_multiply(MOVE_CUBE[j])
                    udslice_move[i][3 * j + k] = cube.get_udslice()
                cube.edge_multiply(MOVE_CUBE[j])
        return udslice_move
    
    def make_edge4_table(self):
        """Move table for the four UD-slice edges FR, FL, BL and BR in the phase 1 -> phase 2 transition"""
        edge4_move = [[0 for _ in range(self.MOVES)] for _ in range(self.EDGE4)]
        cube = CubieCube()
        for i in range(self.EDGE4):
            cube.set_edge4(i)
            for j in range(6):
                for k in range(3):
                    cube.edge_multiply(MOVE_CUBE[j])
                    if k % 2 == 0 and j % 3 != 0:
                        edge4_move[i][3 * j + k] = -1
                    else:
                        edge4_move[i][3 * j + k] = cube.get_edge4()
                cube.edge_multiply(MOVE_CUBE[j])
        return edge4_move

    def make_edge8_table(self):
        """Move table for the edges in the U-face and D-face"""
        edge8_move = [[0 for _ in range(self.MOVES)] for _ in range(self.EDGE8)]
        cube = CubieCube()
        for i in range(self.EDGE8):
            cube.set_edge8(i)
            for j in range(6):
                for k in range(3):
                    cube.edge_multiply(MOVE_CUBE[j])
                    if k % 2 == 0 and j % 3 != 0:
                        edge8_move[i][3 * j + k] = -1
                    else:
                        edge8_move[i][3 * j + k] = cube.get_edge8()
                cube.edge_multiply(MOVE_CUBE[j])
        return edge8_move

    def make_corner_table(self):
        """Move table for the corners coordinate in phase 2"""
        corner_move = [[0 for _ in range(self.MOVES)] for _ in range(self.CORNER)]
        cube = CubieCube()
        for i in range(self.CORNER):
            cube.set_corner(i)
            for j in range(6):
                for k in range(3):
                    cube.corner_multiply(MOVE_CUBE[j])
                    if k % 2 == 0 and j % 3 != 0:
                        corner_move[i][3 * j + k] = -1
                    else:
                        corner_move[i][3 * j + k] = cube.get_corner()
                cube.corner_multiply(MOVE_CUBE[j])
        return corner_move

    def make_udslice_twist_prune(self):
        udslice_twist_prune = [-1] * (self.UDSLICE * self.TWIST)
        udslice_twist_prune[0] = 0
        count, depth = 1, 0
        while count < self.UDSLICE * self.TWIST:
            for i in range(self.UDSLICE * self.TWIST):
                if udslice_twist_prune[i] == depth:
                    m = [
                        self.udslice_move[i // self.TWIST][j] * self.TWIST
                        + self.twist_move[i % self.TWIST][j]
                        for j in range(18)
                    ]
                    for x in m:
                        if udslice_twist_prune[x] == -1:
                            count += 1
                            udslice_twist_prune[x] = depth + 1
            depth += 1
        return PruningTable(udslice_twist_prune, self.TWIST)

    def make_udslice_flip_prune(self):
        udslice_flip_prune = [-1] * (self.UDSLICE * self.FLIP)
        udslice_flip_prune[0] = 0
        count, depth = 1, 0
        while count < self.UDSLICE * self.FLIP:
            for i in range(self.UDSLICE * self.FLIP):
                if udslice_flip_prune[i] == depth:
                    m = [
                        self.udslice_move[i // self.FLIP][j] * self.FLIP
                        + self.flip_move[i % self.FLIP][j]
                        for j in range(18)
                    ]
                    for x in m:
                        if udslice_flip_prune[x] == -1:
                            count += 1
                            udslice_flip_prune[x] = depth + 1
            depth += 1
        return PruningTable(udslice_flip_prune, self.FLIP)


    def make_edge4_edge8_prune(self):
        edge4_edge8_prune = [-1] * (self.EDGE4 * self.EDGE8)
        edge4_edge8_prune[0] = 0
        count, depth = 1, 0
        while count < self.EDGE4 * self.EDGE8:
            for i in range(self.EDGE4 * self.EDGE8):
                if edge4_edge8_prune[i] == depth:
                    m = [
                        self.edge4_move[i // self.EDGE8][j] * self.EDGE8
                        + self.edge8_move[i % self.EDGE8][j]
                        for j in range(18)
                    ]
                    for x in m:
                        if edge4_edge8_prune[x] == -1:
                            count += 1
                            edge4_edge8_prune[x] = depth + 1
            depth += 1
        return PruningTable(edge4_edge8_prune, self.EDGE8)

    def make_edge4_corner_prune(self):
        edge4_corner_prune = [-1] * (self.EDGE4 * self.CORNER)
        edge4_corner_prune[0] = 0
        count, depth = 1, 0
        while count < self.EDGE4 * self.CORNER:
            for i in range(self.EDGE4 * self.CORNER):
                if edge4_corner_prune[i] == depth:
                    m = [
                        self.edge4_move[i // self.CORNER][j] * self.CORNER
                        + self.corner_move[i % self.CORNER][j]
                        for j in range(18)
                    ]
                    for x in m:
                        if edge4_corner_prune[x] == -1:
                            count += 1
                            edge4_corner_prune[x] = depth + 1
            depth += 1
        return PruningTable(edge4_corner_prune, self.CORNER)
