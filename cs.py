import time
import sys
import cubie
from pieces import MOVE

from solve import SolutionManager

def solve(cube_string, max_length=25, max_time=120):
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

if __name__ == "__main__":
    if len(sys.argv) > 1:
        move_string = sys.argv[1]
    else:
        move_string = input("Input move string: ")
    
    move_string = move_string.rstrip().split()
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
    print(fc.to_string())
    solution = solve(fc.to_string())
    print(solution)