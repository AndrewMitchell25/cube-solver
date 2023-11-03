from pieces import Corner, Edge
from helpers import c_nk
from cube import face

class CubieCube:

    def __init__(self, cp=None, co=None, ep=None, eo=None):
        # Initialize corner permutations array
        self.cp = cp[:] if cp else [Corner(i) for i in range(8)]

        # Initialize corner orientations array
        self.co = co[:] if co else [0] * 8

        # Initialize edge permutations array
        self.ep = ep[:] if ep else [Edge(i) for i in range(12)]

        # Initialize edge orientations array
        self.eo = eo[:] if eo else [0] * 12

    def corner_multiply(self, other):
        """Multiplies the corners of this cube by another cube, other"""
        new_cp = [0] * 8
        new_co = [0] * 8
        co = 0

        for c in Corner:
            new_cp[c] = self.cp[other.cp[c]]
            new_co[c] = (self.co[other.cp[c]] + other.co[c]) % 3
            """
            co1 = self.co[other.cp[c]]
            co2 = other.co[c]

            if co1 < 3 and co2 < 3:
                co = co1 + co2
                if co >= 3:
                    co -= 3

            new_co[c] = co
            """

        for c in Corner:
            self.cp[c] = new_cp[c]
            self.co[c] = new_co[c]

    def edge_multiply(self, other):
        """Multiplies the edges of this cube by another cube, other"""
        new_eo = [0] * 12
        new_ep = [0] * 12

        for e in Edge:
            new_eo[e] = (self.eo[other.ep[e]] + other.eo[e]) % 2
            new_ep[e] = self.ep[other.ep[e]]

        for e in Edge:
            self.eo[e] = new_eo[e]
            self.ep[e] = new_ep[e]

    def multiply(self, other):
        """Multiplies this cube by another cube, other"""
        self.corner_multiply(other)
        self.edge_multiply(other)

    def move(self, i):
        """Make one of the 6 moves on the cube"""
        self.multiply(MOVE_CUBE[i])

    def move2(self, axis, power):
        """Make one of the 6 moves on the cube"""
        for i in range(power):
            self.multiply(MOVE_CUBE[axis])

    def to_facecube(self):
        """
        Convert CubieCube to FaceCube.
        """
        ret = face.FaceCube()
        for i in range(8):
            j = self.cp[i]
            ori = self.co[i]
            for k in range(3):
                ret.f[face.corner_facelet[i][(k + ori) % 3]] = face.corner_color[j][k]
        for i in range(12):
            j = self.ep[i]
            ori = self.eo[i]
            for k in range(2):
                facelet_index = face.edge_facelet[i][(k + ori) % 2]
                ret.f[facelet_index] = face.edge_color[j][k]
        return ret
    
    def corner_parity(self):
        """Get the parity of the current corner permutation"""
        s = 0
        for i in range(7, 0, -1):
            for j in range(i - 1, -1, -1):
                if self.cp[j] > self.cp[i]:
                    s += 1
        return s % 2
    
    def edge_parity(self):
        """Get the parity of the current edge permutation"""
        s = 0
        for i in range(11, 0, -1):
            for j in range(i - 1, -1, -1):
                if self.ep[j] > self.ep[i]:
                    s += 1
        return s % 2
    
# --------------------- Coordinates for phase 1 ---------------------

    def get_twist(self):
        """
        Get the twist (coordinate representing corner orientation) of the cube
        
        Because in a valid cube the orientation of the first 7 corners
        determines the orientation of the last, we only need to add the
        first 7 corners to get the twist of the cube.
        
        Each corner can be in one of three positions, so we map out each 
        unique possibility of all the orientations of all the edges
        as an integer from 0 to 3^7
        """
        r = 0
        for i in range(7):
            r = 3 * r + self.co[i]
        return r

    def set_twist(self, twist):
        """Set the twist of the cube"""
        twist_parity = 0
        for i in range(6, -1, -1):
            self.co[i] = twist % 3
            twist_parity += self.co[i]
            twist //= 3
        # Set the last corner based on the parity and orientations of the other 7
        self.co[7] = ((3 - twist_parity % 3) % 3)

    def get_flip(self):
        """
        Get the flip (coordinate representing edge orientation) of the cube
        
        Because in a valid cube the orientation of the first 11 edges
        determines the orientation of the last, we only need to add the
        first 11 corners to get the flip of the cube.
        
        Each edge can be in one of two positions, so we map out each 
        unique possibility of all the orientations of all the edges
        as an integer from 0 to 2^11
        """
        r = 0
        for i in range(11):
            r = 2 * r + self.eo[i]
        return r

    def set_flip(self, flip):
        """Set the flip of the cube"""
        flip_parity = 0
        for i in range(10, -1, -1):
            self.eo[i] = flip % 2
            flip_parity += self.eo[i]
            flip //= 2
        # Set the last edge based on the parity and orientations of the other 11
        self.eo[11] = ((2 - flip_parity % 2) % 2)

    def get_udslice(self):
        """
        Get the udslice, the coordinate representing the position of 
        the UD-slice edges FR, FL, BL, BR. Phase 2 starts when these 4 edges
        are in the middle layer of the cube. This state is represented as
        udslice = 0.

        Since there are 4 pieces and 12 possible edge positions, udslice
        will be in the range of 0 to 12C4
        """
        udslice, seen = 0, 0
        for i in range(11, -1, -1):
            if 8 <= self.ep[i] <= 11:
                udslice += c_nk(11 - i, seen + 1)
                seen += 1
        return udslice
    
    def set_udslice(self, udslice):
        """Set the udslice of the cube"""
        udslice_edge = [Edge.FR, Edge.FL, Edge.BL, Edge.BR]
        other_edge = [Edge.UR, Edge.UF, Edge.UL, Edge.UB, Edge.DR, Edge.DF, Edge.DL, Edge.DB]
        for i in range(12):
            self.ep[i] = -1

        # first position the slice edges
        seen = 3
        for i in range(11, -1, -1):
            if udslice - c_nk(i, seen) < 0:
                self.ep[i] = udslice_edge[seen]
                seen -= 1
            else:
                udslice -= c_nk(i, seen)
        # then the remaining edges
        x = 0
        for i in range(12):
            if self.ep[i] == -1:
                self.ep[i] = other_edge[x]
                x += 1


# --------------------- Coordinates for phase 2 ---------------------

    def get_edge4(self):
        """
        Compute edge4, which is the coordinate representing the permutation of 
        FR, FL, BL, FR, which we correctly placed in phase 1, but not necessarily
        correctly ordered.
        """
        edge4 = self.ep[8:]
        r = 0
        for i in range(3, 0, -1):
            s = 0
            for j in range(i):
                if edge4[j] > edge4[i]:
                    s += 1
            r = i * (r + s)
        return r
    
    def set_edge4(self, edge4):
        """Set the edge4 of the cube"""
        slice_edge = [Edge.FR, Edge.FL, Edge.BL, Edge.BR]
        coeffs = [0] * 3
        for i in range(1, 4):
            coeffs[i - 1] = edge4 % (i + 1)
            edge4 //= i + 1
        perm = [0] * 4
        for i in range(2, -1 ,-1):
            perm[i + 1] = slice_edge.pop(i + 1 - coeffs[i])
        perm[0] = slice_edge[0]
        self.ep[8:] = perm[:]

    def get_edge8(self):
        """
        Compute edge8, which is the coordinate representing the permutation of the 8 
        edges UR, UF, UL, UB, DR, DF, DL, DB which in phase 2 will be in the U and D slices.
        """
        edge8 = 0
        for i in range(7, 0, -1):
            s = 0
            for j in range(i):
                if self.ep[j] > self.ep[i]:
                    s += 1
            edge8 = i * (edge8 + s)
        return edge8
    
    def set_edge8(self, edge8):
        """Set the edge8 of the cube."""
        edges = list(range(8))
        perm = [0] * 8
        coeffs = [0] * 7
        for i in range(1, 8):
            coeffs[i - 1] = edge8 % (i + 1)
            edge8 //= i + 1
        for i in range(6, -1, -1):
            perm[i + 1] = edges.pop(i + 1 - coeffs[i])
        perm[0] = edges[0]
        self.ep[:8] = perm[:]

    def get_corner(self):
        """
        Compute corner, the coordinate representing the permutation of the 8
        corners.
        """
        c = 0
        for i in range(7, 0, -1):
            s = 0
            for j in range(i):
                if self.cp[j] > self.cp[i]:
                    s += 1
            c = i * (c + s)
        return c


    def set_corner(self, corner):
        """Set the corner of the cube"""
        corners = list(range(8))
        perm = [0] * 8
        coeffs = [0] * 7
        for i in range(1, 8):
            coeffs[i - 1] = corner % (i + 1)
            corner //= i + 1
        for i in range(6, -1, -1):
            perm[i + 1] = corners.pop(i + 1 - coeffs[i])
        perm[0] = corners[0]
        self.cp = perm[:]

    def get_edge(self):
        """
        Compute the edge, the coordinate representing the permutation 
        of the 12 edges, of the cube.
        """
        e = 0
        for i in range(11, 0, -1):
            s = 0
            for j in range(i):
                if self.ep[j] > self.ep[i]:
                    s += 1
            e = i * (e + s)
        return e
    
    def set_edge(self, edge):
        """Set the edge of the cube"""
        edges = list(range(12))
        perm = [0] * 12
        coeffs = [0] * 11
        for i in range(1, 12):
            coeffs[i - 1] = edge % (i + 1)
            edge //= i + 1
        for i in range(10, -1, -1):
            perm[i + 1] = edges.pop(i + 1 - coeffs[i])
        perm[0] = edges[0]
        self.ep = perm[:]

# --------------------- Solvability ---------------------

    def verify(self):
        """Check if cube is solvable"""
        total = 0
        edge_count = [0 for i in range(12)]
        for e in range(12):
            edge_count[self.ep[e]] += 1
        for i in range(12):
            if edge_count[i] != 1:
                return -2
        for i in range(12):
            total += self.eo[i]
        if total % 2 != 0:
            return -3
        corner_count = [0] * 8
        for c in range(8):
            corner_count[self.cp[c]] += 1
        for i in range(8):
            if corner_count[i] != 1:
                return -4
        total = 0
        for i in range(8):
            total += self.co[i]
        if total % 3 != 0:
            return -5
        if self.edge_parity() != self.corner_parity():
            return -6
        return 0

# --------------------- The Basic 6 Moves ---------------------

#Up
cpU = [Corner.UBR, Corner.URF, Corner.UFL, Corner.ULB, Corner.DFR, Corner.DLF, Corner.DBL, Corner.DRB]
coU = [0, 0, 0, 0, 0, 0, 0, 0]
epU = [Edge.UB, Edge.UR, Edge.UF, Edge.UL, Edge.DR, Edge.DF, Edge.DL, Edge.DB, Edge.FR, Edge.FL, Edge.BL, Edge.BR]
eoU = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#Right
cpR = [Corner.DFR, Corner.UFL, Corner.ULB, Corner.URF, Corner.DRB, Corner.DLF, Corner.DBL, Corner.UBR]
coR = [2, 0, 0, 1, 1, 0, 0, 2]
epR = [Edge.FR, Edge.UF, Edge.UL, Edge.UB, Edge.BR, Edge.DF, Edge.DL, Edge.DB, Edge.DR, Edge.FL, Edge.BL, Edge.UR]
eoR = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#Front
cpF = [Corner.UFL, Corner.DLF, Corner.ULB, Corner.UBR, Corner.URF, Corner.DFR, Corner.DBL, Corner.DRB]
coF = [1, 2, 0, 0, 2, 1, 0, 0]
epF = [Edge.UR, Edge.FL, Edge.UL, Edge.UB, Edge.DR, Edge.FR, Edge.DL, Edge.DB, Edge.UF, Edge.DF, Edge.BL, Edge.BR]
eoF = [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0]

#Down
cpD = [Corner.URF, Corner.UFL, Corner.ULB, Corner.UBR, Corner.DLF, Corner.DBL, Corner.DRB, Corner.DFR]
coD = [0, 0, 0, 0, 0, 0, 0, 0]
epD = [Edge.UR, Edge.UF, Edge.UL, Edge.UB, Edge.DF, Edge.DL, Edge.DB, Edge.DR, Edge.FR, Edge.FL, Edge.BL, Edge.BR]
eoD = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#Left
cpL = [Corner.URF, Corner.ULB, Corner.DBL, Corner.UBR, Corner.DFR, Corner.UFL, Corner.DLF, Corner.DRB]
coL = [0, 1, 2, 0, 0, 2, 1, 0]
epL = [Edge.UR, Edge.UF, Edge.BL, Edge.UB, Edge.DR, Edge.DF, Edge.FL, Edge.DB, Edge.FR, Edge.UL, Edge.DL, Edge.BR]
eoL = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#Back
cpB = [Corner.URF, Corner.UFL, Corner.UBR, Corner.DRB, Corner.DFR, Corner.DLF, Corner.ULB, Corner.DBL]
coB = [0, 0, 1, 2, 0, 0, 2, 1]
epB = [Edge.UR, Edge.UF, Edge.UL, Edge.BR, Edge.DR, Edge.DF, Edge.DL, Edge.BL, Edge.FR, Edge.FL, Edge.UB, Edge.DB]
eoB = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1]

# ---------------- Create a structure to hold all the moves ----------------
MOVE_CUBE = [CubieCube() for i in range(6)]

MOVE_CUBE[0].cp = cpU
MOVE_CUBE[0].co = coU
MOVE_CUBE[0].ep = epU
MOVE_CUBE[0].eo = eoU

MOVE_CUBE[1].cp = cpR
MOVE_CUBE[1].co = coR
MOVE_CUBE[1].ep = epR
MOVE_CUBE[1].eo = eoR

MOVE_CUBE[2].cp = cpF
MOVE_CUBE[2].co = coF
MOVE_CUBE[2].ep = epF
MOVE_CUBE[2].eo = eoF

MOVE_CUBE[3].cp = cpD
MOVE_CUBE[3].co = coD
MOVE_CUBE[3].ep = epD
MOVE_CUBE[3].eo = eoD

MOVE_CUBE[4].cp = cpL
MOVE_CUBE[4].co = coL
MOVE_CUBE[4].ep = epL
MOVE_CUBE[4].eo = eoL

MOVE_CUBE[5].cp = cpB
MOVE_CUBE[5].co = coB
MOVE_CUBE[5].ep = epB
MOVE_CUBE[5].eo = eoB