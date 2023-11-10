from pieces import Color, Facelet
from cube import cubie

# Map corner pieces to the corresponding facelet positions
corner_facelet = (
    (Facelet.U9, Facelet.R1, Facelet.F3),
    (Facelet.U7, Facelet.F1, Facelet.L3),
    (Facelet.U1, Facelet.L1, Facelet.B3),
    (Facelet.U3, Facelet.B1, Facelet.R3),
    (Facelet.D3, Facelet.F9, Facelet.R7),
    (Facelet.D1, Facelet.L9, Facelet.F7),
    (Facelet.D7, Facelet.B9, Facelet.L7),
    (Facelet.D9, Facelet.R9, Facelet.B7),
)

# Map edge pieces to the corresponding facelet positions
edge_facelet = (
    (Facelet.U6, Facelet.R2),
    (Facelet.U8, Facelet.F2),
    (Facelet.U4, Facelet.L2),
    (Facelet.U2, Facelet.B2),
    (Facelet.D6, Facelet.R8),
    (Facelet.D2, Facelet.F8),
    (Facelet.D4, Facelet.L8),
    (Facelet.D8, Facelet.B8),
    (Facelet.F6, Facelet.R4),
    (Facelet.F4, Facelet.L6),
    (Facelet.B6, Facelet.L4),
    (Facelet.B4, Facelet.R6),
)

# Map corners to the colors of each side
corner_color = (
    (Color.U, Color.R, Color.F),
    (Color.U, Color.F, Color.L),
    (Color.U, Color.L, Color.B),
    (Color.U, Color.B, Color.R),
    (Color.D, Color.F, Color.R),
    (Color.D, Color.L, Color.F),
    (Color.D, Color.B, Color.L),
    (Color.D, Color.R, Color.B),
)

# Map edges to the colors of each side
edge_color = (
    (Color.U, Color.R),
    (Color.U, Color.F),
    (Color.U, Color.L),
    (Color.U, Color.B),
    (Color.D, Color.R),
    (Color.D, Color.F),
    (Color.D, Color.L),
    (Color.D, Color.B),
    (Color.F, Color.R),
    (Color.F, Color.L),
    (Color.B, Color.L),
    (Color.B, Color.R),
)

class FaceCube:
    def __init__(self, cube_string="".join(i * 9 for i in "URFDLB")):
        self.f = [Color[i] for i in cube_string]

    def to_string(self):
        return "".join(Color(i).name for i in self.f)

    def to_cubiecube(self):
        """Convert FaceCube to CubieCube"""
        cube = cubie.CubieCube()
        for i in range(8):
            # all corner names start with U or D, allowing us to find
            # orientation of any given corner as follows
            for ori in range(3):
                if self.f[corner_facelet[i][ori]] in [Color.U, Color.D]:
                    break
            color1 = self.f[corner_facelet[i][(ori + 1) % 3]]
            color2 = self.f[corner_facelet[i][(ori + 2) % 3]]
            for j in range(8):
                if (color1 == corner_color[j][1] and color2 == corner_color[j][2]):
                    cube.cp[i] = j
                    cube.co[i] = ori
                    break

        for i in range(12):
            for j in range(12):
                if (
                    self.f[edge_facelet[i][0]] == edge_color[j][0]
                    and self.f[edge_facelet[i][1]] == edge_color[j][1]
                ):
                    cube.ep[i] = j
                    cube.eo[i] = 0
                    break
                if (
                    self.f[edge_facelet[i][0]] == edge_color[j][1]
                    and self.f[edge_facelet[i][1]] == edge_color[j][0]
                ):
                    cube.ep[i] = j
                    cube.eo[i] = 1
                    break
        return cube