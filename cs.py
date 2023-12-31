import time
import sys
import cubie
from pieces import MOVE
import scramble
import webcam
import time
from display import display_cube_color, display_solve

from solve import SolutionManager

def solve(cube_string, max_length=50, max_time=120):
    sm = SolutionManager(cube_string)
    start_time = time.time()
    solution = sm.solve(max_length, time.time() + max_time)
    end_time = time.time()
    total_time = end_time - start_time
    if solution == -1:
        print("No solution found, max_length exceeded")
    elif solution == -2:
        print("No solution found, max_time exceeded")
    else:
        return solution, total_time
    return None, None
    
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
    solution, total_time = solve(fc.to_string())
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
    return solution, total_time

def solve_from_cube_string(cube_string, display=False):
    if display:
        display_cube_color(cube_string)
    solution, total_time = solve(cube_string)
    return solution, total_time

if __name__ == "__main__":
    move_string = []
    display = False
    use_webcam = False
    cube_string = False
    interactive = False
    if len(sys.argv) > 1:
        for i in range(len(sys.argv)):
            if sys.argv[i] == "-c":
                cube_string = input("Input cube string: ")
            if sys.argv[i] == "-m":
                move_string = input("Input move string: ").rstrip().split()
            if sys.argv[i] == "-d":
                display = True
            if sys.argv[i] == "-w":
                use_webcam = True
            if sys.argv[i] == "-i":
                interactive = True

    if use_webcam:
        print("Please scan the cube faces in the same direction as shown in the bottom corner")
        cube_string = webcam.run()
        if(cube_string) == -1:
            exit()
        solution, total_time = solve(cube_string)
    elif cube_string:
        solution, total_time = solve_from_cube_string(cube_string, display)
    else:
        if not move_string:
            move_string = scramble.generate_scramble()
        
        scramble.print_scramble(move_string)
        solution, total_time = solve_from_move_string(move_string, display)
    print(f"Total solve time: {total_time:.3f} seconds")
    print(f"Solution: {solution}")

    if interactive:
        display_solve(solution)
