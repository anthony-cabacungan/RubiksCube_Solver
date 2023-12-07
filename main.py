from cube import RubiksCube
from search import *

def print_cubes(cubes):
    for i in cubes:
        RubiksCube(state=i).show()
        print('-------------------------------------------------------')

if __name__ == '__main__':
    cube = RubiksCube(state="rrrwrwrgryrywwwwrwbrbggggggwowyyyyyygygbbbbbbooobooooo", initial="rrrwrwrgryrywwwwrwbrbggggggwowyyyyyygygbbbbbbooobooooo")
    print(cube.stringify())
    cube.show()
    print(cube.stringify())
    # solution = simulated_annealing_full(problem=cube, schedule=exp_schedule(k=49000,lam=0.00060, limit=60000))
    solution = simulated_annealing_full(problem=cube, schedule=exp_schedule(k=9000,lam=0.0003, limit=500000))
    # print(solution)
    # print_cubes(solution)