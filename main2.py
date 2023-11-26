from cube import RubiksCube
from search import *

def print_cubes(cubes):
    for i in cubes:
        RubiksCube(state=i).show()
        print('-------------------------------------------------------')

if __name__ == '__main__':
    cube = RubiksCube(state="rrrwrwrgryrywwwwrwbrbggggggwowyyyyyygygbbbbbbooobooooo")
    cube.show()
    print(cube.stringify())
    solution = simulated_annealing_full(problem=cube)
    print(solution)
    # print_cubes(solution)