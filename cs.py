import time
import sys
import cubie
from pieces import MOVE
import scramble
import webcam

from solve import SolutionManager

colors = {
    'U': '\033[47m',
    'R': '\033[41m',
    'F': '\033[42m',
    'D': '\033[103m',
    'L': '\033[43m',
    'B': '\033[44m',
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



def solve(cube_string, max_length=50, max_time=120):
    sm = SolutionManager(cube_string)
    solution = sm.solve(max_length, time.time() + max_time)
    if solution == -1:
        print("No solution found, max_length exceeded")
    elif solution == -2:
        print("No solution found, max_time exceeded")
    else:
        return solution
    
def solve_best(cube_string, max_length=25, max_time=120):
    return list(solve_best_generator(cube_string, max_length, max_time))

def solve_best_generator(cube_string, max_length=25, max_time=10):
    """
    Solve the cube repeatedly, reducing max_length each time a solution is
    found until timeout is reached or no more solutions are found.
    """
    sm = SolutionManager(cube_string)
    timeout = time.time() + max_time
    while True:
        solution = sm.solve(max_length, timeout)

        if isinstance(solution, str):
            yield solution
            max_length = len(solution.split(" ")) - 1
        elif solution == -2 or solution == -1:
            # timeout or no more solutions
            break
        else:
            raise RuntimeError(
                f"SolutionManager.solve: unexpected return value {solution}"
            )

def solve_from_move_string(move_string, display=False):
    cube = cubie.CubieCube()
    for move in move_string:
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
    if display:
        display_cube_color(fc.to_string())
    solution = solve(fc.to_string())
    for move in solution.split():
        axis = MOVE[move[0]]
        if len(move) > 1:
            if move[1] == "2":
                power = 2
            elif move[1] == "'":
                power = 3
        else:
            power = 1
        cube.move2(axis, power)
    if display:
        fc = cube.to_facecube()
        display_cube_color(fc.to_string())
        print(fc.to_string())
    return solution

if __name__ == "__main__":
    move_string = []
    display = False
    use_webcam = False
    if len(sys.argv) > 1:
        for i in range(len(sys.argv)):
            if sys.argv[i] == "-s":
                move_string = sys.argv[i+1].rstrip().split()
            if sys.argv[i] == "-i":
                move_string = input("Input move string: ").rstrip().split()
            if sys.argv[i] == "-d":
                display = True
            if sys.argv[i] == "-w":
                use_webcam = True

    if use_webcam:
        print("Please scan the cube faces in the same direction as shown in the bottom corner")
        cube_string = webcam.run()
        if(cube_string) == -1:
            exit()
        solution = solve(cube_string)
        
    else:
        if not move_string:
            move_string = scramble.generate_scramble()
        
        scramble.print_scramble(move_string)
        solution = solve_from_move_string(move_string, display)
    print(f"Solution: {solution}")


