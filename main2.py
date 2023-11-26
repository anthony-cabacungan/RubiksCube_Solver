from cube import RubiksCube
from solver2 import *

#--------------------------------
cube = RubiksCube(
    state="rrrwrwrgryrywwwwrwbrbggggggwowyyyyyygygbbbbbbooobooooo"
)
cube.show()
print('-----------')
#--------------------------------
cube.horizontal_twist(row=0,direction=0)
cube.show()
print(cube.stringify())

# ------------------------------------------------------------------------------------

if __name__ == '__main__':
    wgc = WolfGoatCabbage()
    solution = depth_first_graph_search(wgc).solution()
    print(solution)