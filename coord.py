from tables import Tables
from cube import cubie

class CoordCube:
    """
    Coordinate representation of cube, keeping track of
    twist, flip, udslice, edge4, edge8, and corner.
    """

    def __init__(self, twist=0, flip=0, udslice=0, edge4=0, edge8=0, corner=0):
        self.tables = Tables()

        self.twist = twist
        self.flip = flip
        self.udslice = udslice
        self.edge4 = edge4
        self.edge8 = edge8
        self.corner = corner

    def from_cubiecube(self, cube):
        """Create a CoordCube from a CubieCube"""
        return self(cube.get_twist(), cube.get_flip(), cube.get_udslice(), cube.get_edge4(), cube.get_edge8(), cube.get_corner())
    
    def move(self, mv):
        """Update all coordinates after applying move mv"""
        self.twist = self.tables.twist_move[self.twist][mv]
        self.flip = self.tables.flip_move[self.flip][mv]
        self.udslice = self.tables.udslice_move[self.udslice][mv]
        self.edge4 = self.tables.edge4_move[self.edge4][mv]
        self.edge8 = self.tables.edge8_move[self.edge8][mv]
        self.corner = self.tables.corner_move[self.corner][mv]