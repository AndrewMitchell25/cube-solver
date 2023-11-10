import random
def generate_scramble():
    print("Generating scramble...")
    axis = ['U', 'R', 'F', 'D', 'L', 'B']
    power = ['', '2', "'"]

    scramble = []
    
    scrambled_moves = []

    for i in range(random.randint(18, 22)):
        n = random.randint(0, len(axis) - 1)
        while scrambled_moves and (scrambled_moves[-1] == n or scrambled_moves[-1] == (n + 3) % 6):
            n = random.randint(0, len(axis) - 1)
        scrambled_moves.append(n)
        scramble.append(axis[n])
        n = random.randint(0, len(power) - 1)
        scramble[-1] += power[n]

    return scramble

def print_scramble(scramble):
    s = ""
    for i in scramble:
        s += i + " "
    print(s)