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
        new_cp = []
        new_co = []
        co = 0

        for c in Corner:
            new_cp.append(self.cp[other.cp[c]])

            co1 = self.co[other.cp[c]]
            co2 = other.co[c]

            if co1 < 3 and co2 < 3:
                co = co1 + co2
                if co >= 3:
                    co -= 3

            new_co.append(co)

        for c in Corner:
            self.cp[c] = new_cp[c]
            self.co[c] = new_co[c]


o = CubieCube([Corner.DFR, Corner.UFL, Corner.ULB, Corner.URF, Corner.DRB, Corner.DLF, Corner.DBL, Corner.UBR],
              [2, 0, 0, 1, 1, 0, 0, 2],
              [Edge.FR, Edge.UF, Edge.UL, Edge.UB, Edge.BR, Edge.DF, Edge.DL, Edge.DB, Edge.DR, Edge.FL, Edge.BL, Edge.UR],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

c = CubieCube()

c.corner_multiply(o)

print(c.co, c.cp, c.eo, c.ep)