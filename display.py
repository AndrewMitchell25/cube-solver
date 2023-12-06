from pieces import MOVE
import cubie

colors = {
    'U': '\033[48;5;15m\033[38;5;0m',
    'R': '\033[48;5;196m\033[38;5;0m',
    'F': '\033[48;5;40m\033[38;5;0m',
    'D': '\033[48;5;226m\033[38;5;0m',
    'L': '\033[48;5;208m\033[38;5;0m',
    'B': '\033[44m\033[38;5;15m',
    'r': '\033[0m',
}

def display_cube(cube_string):
    print("    " * 3,end="")
    for i in range(3):
        print("+---", end="")
    print("+")

    for i in range(3):
        print("    " * 3,end="")
        for j in range(3):
            print(f"| {cube_string[i * 3 + j]} ", end="")
        print("|")
    
    for i in range(4):
        for j in range(3):
            print("+---", end="")
    print("+")

    for i in range(3):
        for j in range(3):
            print(f"| {cube_string[i * 3 + j + 36]} ", end="")
        for j in range(3):    
            print(f"| {cube_string[i * 3 + j + 18]} ", end="")
        for j in range(3):    
            print(f"| {cube_string[i * 3 + j + 9]} ", end="")
        for j in range(3):    
            print(f"| {cube_string[i * 3 + j + 45]} ", end="")
        print("|")
    
    for i in range(4):
        for j in range(3):
            print("+---", end="")
    print("+")

    for i in range(3):
        print("    " * 3,end="")
        for j in range(3):
            print(f"| {cube_string[i * 3 + j + 27]} ", end="")
        print("|")

    print("    " * 3,end="")
    for i in range(3):
        print("+---", end="")
    print("+")


arrows = {
    'U': {10: '←', 11: '←', 12: '←', 13: '←', 14: '←', 15: '←', 16: '←', 17: '←', 18: '←', 19: '←', 20: '←', 21: '←'},
    'R': {3: '↑', 6: '↑', 9: '↑', 15: '↑', 27: '↑', 39: '↑', 48: '↑', 51: '↑', 54: '↑', 19: '↓', 31: '↓', 43: '↓'},
    'F': {7: '→', 8: '→', 9: '→', 12: '↑', 24: '↑', 36: '↑', 16: '↓', 28: '↓', 40: '↓', 46: '←', 47: '←', 48: '←'},
    'D': {34: '→', 35: '→', 36: '→', 37: '→', 38: '→', 39: '→', 40: '→', 41: '→', 42: '→', 43: '→', 44: '→', 45: '→'},
    'L': {1: '↓', 4: '↓', 7: '↓', 13: '↓', 25: '↓', 37: '↓', 46: '↓', 49: '↓', 52: '↓', 21: '↑', 33: '↑', 45: '↑'},
    'B': {1: '←', 2: '←', 3: '←', 10: '↓', 22: '↓', 34: '↓', 52: '→', 53: '→', 54: '→', 18: '↑', 30: '↑', 42: '↑'}
}

arrow_opposites = {
    '→': '←',
    '←': '→',
    '↑': '↓',
    '↓': '↑'
}

def display_cube_arrow(cube_string, move):
    index = 1
    for i in range(3):
        print("    " * 3,end="")
        print(" ", end="")
        for _ in range(3):
            print("+---", end="")
        print("+")
        print("    " * 3,end="")
        print(" ", end="")
        for j in range(3):
            s = "   "
            if index in arrows[move[0]]:
                s = " " + arrows[move[0]][index] + " "
                if len(move) > 1 and move[1] == "'":
                    s = " " + arrow_opposites[arrows[move[0]][index]] + " "
            print(f"|{colors[cube_string[i * 3 + j]]}{s}{colors['r']}", end="")
            index += 1
        print("|")
    
    for i in range(4):
        for j in range(3):
            print("+---", end="")
        print("+", end="")
    print()

    for i in range(3):
        for j in range(3):
            s = "   "
            if index in arrows[move[0]]:
                s = " " + arrows[move[0]][index] + " "
                if len(move) > 1 and move[1] == "'":
                    s = " " + arrow_opposites[arrows[move[0]][index]] + " "
            print(f"|{colors[cube_string[i * 3 + j + 36]]}{s}{colors['r']}", end="")
            index += 1
        print("|", end="")
        for j in range(3):
            s = "   "
            if index in arrows[move[0]]:
                s = " " + arrows[move[0]][index] + " "
                if len(move) > 1 and move[1] == "'":
                    s = " " + arrow_opposites[arrows[move[0]][index]] + " "    
            print(f"|{colors[cube_string[i * 3 + j + 18]]}{s}{colors['r']}", end="")
            index += 1
        print("|", end="")
        for j in range(3):
            s = "   "
            if index in arrows[move[0]]:
                s = " " + arrows[move[0]][index] + " "
                if len(move) > 1 and move[1] == "'":
                    s = " " + arrow_opposites[arrows[move[0]][index]] + " "    
            print(f"|{colors[cube_string[i * 3 + j + 9]]}{s}{colors['r']}", end="")
            index += 1
        print("|", end="")
        for j in range(3):
            s = "   "
            if index in arrows[move[0]]:
                s = " " + arrows[move[0]][index] + " "
                if len(move) > 1 and move[1] == "'":
                    s = " " + arrow_opposites[arrows[move[0]][index]] + " "    
            print(f"|{colors[cube_string[i * 3 + j + 45]]}{s}{colors['r']}", end="")
            index += 1
        print("|")
        for _ in range(4):
            for _ in range(3):
                print("+---", end="")
            print("+", end="")
        print()

    for i in range(3):
        print("    " * 3,end="")
        print(" ", end="")
        for j in range(3):
            s = "   "
            if index in arrows[move[0]]:
                s = " " + arrows[move[0]][index] + " "
                if len(move) > 1 and move[1] == "'":
                    s = " " + arrow_opposites[arrows[move[0]][index]] + " " 
            print(f"|{colors[cube_string[i * 3 + j + 27]]}{s}{colors['r']}", end="")
            index += 1
        print("|")
        print("    " * 3,end="")
        print(" ", end="")
        for _ in range(3):
            print("+---", end="")
        print("+")



def display_cube_color(cube_string):
    for i in range(3):
        print("    " * 3,end="")
        print(" ", end="")
        for _ in range(3):
            print("+---", end="")
        print("+")
        print("    " * 3,end="")
        print(" ", end="")
        for j in range(3):
            print(f"|{colors[cube_string[i * 3 + j]]}   {colors['r']}", end="")
        print("|")
    
    for i in range(4):
        for j in range(3):
            print("+---", end="")
        print("+", end="")
    print()

    for i in range(3):
        for j in range(3):
            print(f"|{colors[cube_string[i * 3 + j + 36]]}   {colors['r']}", end="")
        print("|", end="")
        for j in range(3):    
            print(f"|{colors[cube_string[i * 3 + j + 18]]}   {colors['r']}", end="")
        print("|", end="")
        for j in range(3):    
            print(f"|{colors[cube_string[i * 3 + j + 9]]}   {colors['r']}", end="")
        print("|", end="")
        for j in range(3):    
            print(f"|{colors[cube_string[i * 3 + j + 45]]}   {colors['r']}", end="")
        print("|")
        for _ in range(4):
            for _ in range(3):
                print("+---", end="")
            print("+", end="")
        print()

    for i in range(3):
        print("    " * 3,end="")
        print(" ", end="")
        for j in range(3):
            print(f"|{colors[cube_string[i * 3 + j + 27]]}   {colors['r']}", end="")
        print("|")
        print("    " * 3,end="")
        print(" ", end="")
        for _ in range(3):
            print("+---", end="")
        print("+")

def display_solve(solution):
    ready = input("Press enter when you're ready to solve. Press q to quit.")
    if ready == "q":
        return
    cube = cubie.CubieCube()
    solution = solution.split(" ")
    for move in reversed(solution):
        axis = MOVE[move[0]]
        if len(move) > 1:
            if move[1] == "2":
                power = 2
            elif move[1] == "'":
                power = 1
        else:
            power = 3
        cube.move2(axis, power)
    fc = cube.to_facecube()
    display_cube_color(fc.to_string())
    new_solution = []
    for move in solution:
        if len(move) < 2 or move[1] != '2':
            new_solution.append(move)
        else:
            new_solution.append(move[0])
            new_solution.append(move[0])
    for move in new_solution:
        axis = MOVE[move[0]]
        if len(move) > 1:
            if move[1] == "2":
                power = 2
            elif move[1] == "'":
                power = 3
        else:
            power = 1
        cube.move2(axis, power)
        fc = cube.to_facecube()
        display_cube_arrow(fc.to_string(), move)
        print(f"{move}")
        input("Press enter to make the next move.")

    print("Cube is solved")