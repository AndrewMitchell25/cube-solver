import time

from coord import CoordCube
from face import FaceCube
from pieces import Color
from tables import Tables

class SolutionManager:
    def __init__(self, facelets):
        self.tables = Tables()

        self.facelets = facelets.upper()

        status = self.verify()
        if status:
            error_message = {
                -1: "each colour should appear exactly 9 times",
                -2: "not all edges exist exactly once",
                -3: "one edge should be flipped",
                -4: "not all corners exist exactly once",
                -5: "one corner should be twisted",
                -6: "two corners or edges should be exchanged",
            }
            raise ValueError(f"Invalid cube: {error_message[status]}")
        

    def solve(self, max_length=50, timeout=float("inf")):
        """
        Implement two consecutive IDA* searches for phase 1 and phase 2
        to solve the cube.
        """
        self.phase1_initialize(max_length)
        self.allowed_length = max_length
        self.timeout = timeout
        print("Phase 1 starting")
        for depth in range(self.allowed_length):
            n = self.phase1_search(0, depth)
            if n >= 0:
                # found solution
                return self.solution_to_string(n)
            elif n == -2:
                # exceeded the time limit
                return -2
            
        # no solution found
        return -1
    
    def verify(self):
        count = [0] * 6
        try:
            for char in self.facelets:
                count[Color[char]] += 1
        except (IndexError, ValueError):
            return -1
        for i in range(6):
            if count[i] != 9:
                return -1

        face_cube = FaceCube(self.facelets)
        cubie_cube = face_cube.to_cubiecube()

        return cubie_cube.verify()
    
    def phase1_initialize(self, max_length):
        print("Phase 1 initializing")
        # axis and power store the nth move 
        # axis = the index of the face being turned
        # power = the number of clockwise quarter turns (direction of turn)
        self.axis = [0] * max_length
        self.power = [0] * max_length

        # these lists store the phase 1 coordinates after n moves
        self.twist = [0] * max_length
        self.flip = [0] * max_length
        self.udslice = [0] * max_length

        # these lists store the phase 2 coordinates
        self.corner = [0] * max_length
        self.edge4 = [0] * max_length
        self.edge8 = [0] * max_length

        # these lists store the minimum number of moves required to reach the next phase
        # the estimates come from the pruning tables
        self.min_dist_1 = [0] * max_length
        self.min_dist_2 = [0] * max_length

        # initialize the arrays
        self.f = FaceCube(self.facelets)
        c = self.f.to_cubiecube()
        self.c = CoordCube(c.get_twist(), c.get_flip(), c.get_udslice(), c.get_edge4(), c.get_edge8(), c.get_corner())
        self.twist[0] = self.c.twist
        self.flip[0] = self.c.flip
        self.udslice[0] = self.c.udslice
        self.corner[0] = self.c.corner
        self.edge4[0] = self.c.edge4
        self.edge8[0] = self.c.edge8
        self.min_dist_1[0] = self.phase1_cost(0)

    def phase2_initialize(self, n):
        print("Phase 2 initializing")
        if time.time() > self.timeout:
            return -2
        # initialise phase 2 search from the phase 1 solution
        cc = self.f.to_cubiecube()
        for i in range(n):
            for j in range(self.power[i]):
                cc.move(self.axis[i])
        self.edge4[n] = cc.get_edge4()
        self.edge8[n] = cc.get_edge8()
        self.corner[n] = cc.get_corner()
        self.min_dist_2[n] = self.phase2_cost(n)
        print("Phase 2 starting")
        for depth in range(self.allowed_length - n):
            m = self.phase2_search(n, depth)
            if m >= 0:
                return m
        return -1
    
    def phase1_cost(self, n):
        """
        Cost of current position in phase 1
        Gives the lower bound estimate on the number of moves to get to phase 2
        """
        return max(
            self.tables.udslice_twist_prune[self.udslice[n], self.twist[n]],
            self.tables.udslice_flip_prune[self.udslice[n], self.flip[n]],
        )
    
    def phase2_cost(self, n):
        """
        Cost of current position in phase 2
        Gives the lower bound estimate on the number of moves to get to solution
        """
        return max(
            self.tables.edge4_corner_prune[self.edge4[n], self.corner[n]],
            self.tables.edge4_edge8_prune[self.edge4[n], self.edge8[n]],
        )
    
    def phase1_search(self, n, depth):
        if time.time() > self.timeout:
            return -2
        elif self.min_dist_1[n] == 0:
            print("Phase 1 ended")
            return self.phase2_initialize(n)
        elif self.min_dist_1[n] <= depth:
            for i in range(6):
                if n > 0 and self.axis[n - 1] in (i, i + 3):
                    continue
                for j in range(1, 4):
                    self.axis[n] = i
                    self.power[n] = j
                    mv = 3 * i + j - 1

                    # update coordinates
                    self.twist[n + 1] = self.tables.twist_move[self.twist[n]][mv]
                    self.flip[n + 1] = self.tables.flip_move[self.flip[n]][mv]
                    self.udslice[n + 1] = self.tables.udslice_move[self.udslice[n]][mv]
                    self.min_dist_1[n + 1] = self.phase1_cost(n + 1)

                    # start search from next node
                    m = self.phase1_search(n + 1, depth - 1)
                    if m >= 0:
                        return m
                    if m == -2:
                        # time limit exceeded
                        return -2
        # if no solution found at current depth, return -1
        return -1
    
    def phase2_search(self, n, depth):
        if self.min_dist_2[n] == 0:
            print("Phase 2 ended")
            return n
        elif self.min_dist_2[n] <= depth:
            for i in range(6):
                if n > 0 and self.axis[n - 1] in (i, i + 3):
                    continue
                for j in range(1, 4):
                    if i in [1, 2, 4, 5] and j != 2:
                        continue
                    self.axis[n] = i
                    self.power[n] = j
                    mv = 3 * i + j - 1

                    # update coordinates following the move mv
                    self.edge4[n + 1] = self.tables.edge4_move[self.edge4[n]][mv]
                    self.edge8[n + 1] = self.tables.edge8_move[self.edge8[n]][mv]
                    self.corner[n + 1] = self.tables.corner_move[self.corner[n]][mv]
                    self.min_dist_2[n + 1] = self.phase2_cost(n + 1)

                    # start search from new node
                    m = self.phase2_search(n + 1, depth - 1)
                    if m >= 0:
                        return m             
        return -1
    
    def solution_to_string(self, length):
        """Generate solution string"""
        def generate_move(axis, power):
            if power == 1:
                return Color(axis).name
            if power == 2:
                return Color(axis).name + "2"
            if power == 3:
                return Color(axis).name + "'"
            return None

        return " ".join([generate_move(self.axis[i], self.power[i]) for i in range(length)])    
