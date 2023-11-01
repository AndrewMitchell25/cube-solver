from pieces import Corner, Edge

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


o = CubieCube([Corner.DFR, Corner.UFL, Corner.ULB, Corner.URF, Corner.DRB, Corner.DLF, Corner.DBL, Corner.UBR],
              [2, 0, 0, 1, 1, 0, 0, 2],
              [Edge.FR, Edge.UF, Edge.UL, Edge.UB, Edge.BR, Edge.DF, Edge.DL, Edge.DB, Edge.DR, Edge.FL, Edge.BL, Edge.UR],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

c = CubieCube()
print(c.co, c.cp, c.eo, c.ep)
c.multiply(o)
print(c.co, c.cp, c.eo, c.ep)

