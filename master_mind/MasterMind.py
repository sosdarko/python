import random
from typing import List
import itertools

COLORS = [1, 2, 3, 4, 5, 6]
COLOR_NAMES = ['RED', 'YELLOW', 'GREEN', 'BLUE', 'ORANGE', 'PURPLE']
COLOR_NAMES_SHORT = ['R', 'Y', 'G', 'B', 'O', 'P']
EMPTY_COLOR = 0
COLORS_CNT = len(COLORS)
COMBINATION_LEN = 4

HIT_COLOR = 1
HIT_COLOR_NAME = 'W'
HIT_COLOR_PLACE = 2
HIT_COLOR_PLACE_NAME = 'B'

WORLD = list(itertools.product(COLORS, repeat=COMBINATION_LEN))


def calc_distance(comb1: List, comb2: List) -> List:
    comb1_copy = comb1.copy()
    comb2_copy = comb2.copy()
    distance = []
    hit_count = 0
    for i in range(len(comb1_copy)):
        if comb1_copy[i] == comb2_copy[i]:
            distance.append(HIT_COLOR_PLACE)
            hit_count += 1
            comb1_copy[i] = EMPTY_COLOR
            comb2_copy[i] = EMPTY_COLOR

    for i in range(len(comb1_copy)):
        if comb1_copy[i] == EMPTY_COLOR:
            continue
        for j in range(len(comb2_copy)):
            if comb2_copy[j] == EMPTY_COLOR:
                continue
            if comb2_copy[j] == comb1_copy[i]:
                distance.append(HIT_COLOR)
                hit_count += 1
                comb2_copy[j] = EMPTY_COLOR
                comb1_copy[i] = EMPTY_COLOR

    return distance


def evaluate_distance(distance: List) -> float | int:
    l = len(distance)
    if l == 0:
        return 0
    val = 0
    for i in range(0, l):
        if distance[i] == HIT_COLOR:
            val += 12.5
        elif distance[i] == HIT_COLOR_PLACE:
            val += 25

    return val


def dump_list(l: List):
    print(f"Length: {len(l)}")
    print("Elements:")
    for item in l:
        print(item)

#for c in WORLD:
#    print(c)

def reduce_world(world: List, guess: List, distance: List):
    world[:] = [el for el in world if calc_distance(list(el), guess) == distance]


def choose_possibility(world: List, method: str) -> List:
    if not world:
        return []
    ret = world[0]
    # this part to improve: find "middle" list based on distance to the other
    if method == "random":
        ret = world[random.randint(0, len(world) - 1)]
    elif method == "first":
        ret = world[0]
    elif method == "middle":
        ret = world[int(len(world) / 2)]
    return list(ret)


def play_mm_simulation(seq_to_guess, method: str = "random"):
    print(seq_to_guess)
    world_of_possibilities = WORLD
    distance = []
    guess = [1,1,2,2]
    guess_number = 0
    progression = []
    while distance != [HIT_COLOR_PLACE for _ in range(COMBINATION_LEN)]:
        print(f"Guess #:{guess_number}: {guess}")
        print(f"Possibilities: {len(world_of_possibilities)}")
        guess_number += 1
        progression.append(len(world_of_possibilities))
        # this step is simulation; otherwise given by other player
        distance = calc_distance(guess, seq_to_guess)
        print(f"Distance: {distance}")
        reduce_world(world_of_possibilities, guess, distance)
        dump_list(world_of_possibilities)
        guess = choose_possibility(world_of_possibilities, method)
        if not guess:
            print("No possibilities")
            break
    print("END")
    print(f"{guess_number}, {progression}: {guess}; to guess: {seq_to_guess}")


def get_distance() -> List:
    answer = input("Answer:")
    ret = []
    for a in answer.upper():
        if a == HIT_COLOR or a == HIT_COLOR_NAME:
            ret.append(HIT_COLOR)
        elif a == HIT_COLOR_PLACE or a == HIT_COLOR_PLACE_NAME:
            ret.append(HIT_COLOR_PLACE)
    return ret


def play_mm(method: str = "random"):
    world_of_possibilities = WORLD
    distance = []
    guess = [1,1,2,2]
    guess_number = 0
    progression = []
    while distance != [HIT_COLOR_PLACE for _ in range(COMBINATION_LEN)]:
        guess_number += 1
        progression.append(len(world_of_possibilities))
        # this step is simulation; otherwise given by other player
        guess_colors = [COLOR_NAMES[x-1] for x in guess]
        print(f"Guess #:{guess_number}: {guess_colors}")
        distance = get_distance()
        reduce_world(world_of_possibilities, guess, distance)
        dump_list(world_of_possibilities)
        guess = choose_possibility(world_of_possibilities, method)
        if not guess:
            print("No possibilities")
            break
    print("END")
    guess_colors = [COLOR_NAMES[x-1] for x in guess]
    print(f"steps: {guess_number}, progression: {progression}, guess: {guess_colors}")


def simulate():
    print(f"World size: {len(WORLD)}")
    to_guess: List[int] = [random.randint(1,6) for _ in range(COMBINATION_LEN)]
    play_mm_simulation(to_guess)

if __name__ == "__main__":
    play_mm()