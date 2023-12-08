from random import randint, choice
from search import *

class RubiksCube(Problem):
    """
    Class containing the rubiks cube code
    """

    def __init__(
        self,
        initial,
        n=3,
        colours=['w', 'o', 'g', 'r', 'b', 'y'],
        state=None,
        goal=["rrrrrrrrrwwwwwwwwwgggggggggyyyyyyyyybbbbbbbbbooooooooo",
              "rrrrrrrrrgggggggggyyyyyyyyybbbbbbbbbwwwwwwwwwooooooooo",
              "rrrrrrrrryyyyyyyyybbbbbbbbbwwwwwwwwwgggggggggooooooooo",
              "rrrrrrrrrbbbbbbbbbwwwwwwwwwgggggggggyyyyyyyyyooooooooo",
              
              "ooooooooobbbbbbbbbyyyyyyyyygggggggggwwwwwwwwwrrrrrrrrr",
              "oooooooooyyyyyyyyygggggggggwwwwwwwwwbbbbbbbbbrrrrrrrrr",
              "ooooooooogggggggggwwwwwwwwwbbbbbbbbbyyyyyyyyyrrrrrrrrr",
              "ooooooooowwwwwwwwwbbbbbbbbbyyyyyyyyygggggggggrrrrrrrrr",
              
              "yyyyyyyyygggggggggooooooooobbbbbbbbbrrrrrrrrrwwwwwwwww",
              "yyyyyyyyyooooooooobbbbbbbbbrrrrrrrrrgggggggggwwwwwwwww",
              "yyyyyyyyybbbbbbbbbrrrrrrrrrgggggggggooooooooowwwwwwwww",
              "yyyyyyyyyrrrrrrrrrgggggggggooooooooobbbbbbbbbwwwwwwwww",
              
              "gggggggggoooooooooyyyyyyyyyrrrrrrrrrwwwwwwwwwbbbbbbbbb",
              "gggggggggyyyyyyyyyrrrrrrrrrwwwwwwwwwooooooooobbbbbbbbb",
              "gggggggggrrrrrrrrrwwwwwwwwwoooooooooyyyyyyyyybbbbbbbbb",
              "gggggggggwwwwwwwwwoooooooooyyyyyyyyyrrrrrrrrrbbbbbbbbb",

              "wwwwwwwwwbbbbbbbbbooooooooogggggggggrrrrrrrrryyyyyyyyy",
              "wwwwwwwwwooooooooogggggggggrrrrrrrrrbbbbbbbbbyyyyyyyyy",
              "wwwwwwwwwgggggggggrrrrrrrrrbbbbbbbbboooooooooyyyyyyyyy",
              "wwwwwwwwwrrrrrrrrrbbbbbbbbbooooooooogggggggggyyyyyyyyy",
              
              "bbbbbbbbbyyyyyyyyyooooooooowwwwwwwwwrrrrrrrrrggggggggg",
              "bbbbbbbbbooooooooowwwwwwwwwrrrrrrrrryyyyyyyyyggggggggg",
              "bbbbbbbbbwwwwwwwwwrrrrrrrrryyyyyyyyyoooooooooggggggggg",
              "bbbbbbbbbrrrrrrrrryyyyyyyyyooooooooowwwwwwwwwggggggggg"
              ]
    ):
        super().__init__(initial, goal)
        """
        Input: n - integer representing the width and height of the rubiks cube
               colours - list containing the first letter of ever colour you wish to use (Default = ['w', 'o', 'g', 'r', 'b', 'y']) [OPTIONAL]
               state - string representing the current state of the rubix cube (Default = None) [OPTIONAL]
        Description: Initialize the rubiks cube
        Output: None
        """

        if state is None:
            self.n = n
            self.colours = colours
            self.reset()
        else:
            self.n = int((len(state) / 6) ** (.5))
            self.colours = []
            self.cube = [[[]]]
            for i, s in enumerate(state):
                if s not in self.colours: self.colours.append(s)
                self.cube[-1][-1].append(s)
                if len(self.cube[-1][-1]) == self.n and len(self.cube[-1]) < self.n:
                    self.cube[-1].append([])
                elif len(self.cube[-1][-1]) == self.n and len(self.cube[-1]) == self.n and i < len(state) - 1:
                    self.cube.append([[]])

    def actions(self, state):
        """Return the legal moves for the Rubik's Cube in the given state."""
        possible_actions = []

        for row in range(self.n):
            possible_actions.append(f'horizontal_{row}_0')
            possible_actions.append(f'horizontal_{row}_1')

        for col in range(self.n):
            possible_actions.append(f'vertical_{col}_0')
            possible_actions.append(f'vertical_{col}_1')

        for col in range(self.n):
            possible_actions.append(f'side_{col}_0')
            possible_actions.append(f'side_{col}_1')
        
        return possible_actions
    
    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        # parsing action into twist, index, and direction
        twist, index, direction = action.split('_')
        index, direction = int(index), int(direction)
        # create temp cube
        temp_cube = RubiksCube(state=state, initial=state)

        if twist == "horizontal":
            temp_cube.horizontal_twist(row=index, direction=direction)
        elif twist == "vertical":
            temp_cube.vertical_twist(column=index, direction=direction)
        elif twist == "side":
            temp_cube.side_twist(column=index, direction=direction)
            
        return temp_cube.stringify()

    def goal_test(self):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        return self.solved()
    
    def manhattan_distance(self, state):
        """Calculate the Manhattan distance between the current state and a list of goal states."""
        min_distance = float('inf')  # Initialize with positive infinity
        
        for goal_state in self.goal:
            distance = 0
            for i in range(len(state)):
                if state[i] != ' ' and state[i] != goal_state[i]:
                    # Assuming each move has a cost of 1
                    distance += 1

            min_distance = min(min_distance, distance)

        return min_distance

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1."""
        
        # Calculate the minimum Manhattan distance as the cost
        distance = self.manhattan_distance(state2)
        # print(distance)
        return distance

    def value(self, state):
        """For optimization problems, each state has a value. Hill Climbing
        and related algorithms try to maximize this value."""

        # find num of correct colors of each side, return sum
        # correct colors are based off of center colors

        center_colors = {
            "top_color": state[4],
            "left_color": state[13],
            "center_color": state[22],
            "right_color": state[31],
            "back_color": state[40],
            "bottom_color": state[49]
        }

        sum = 0

        top, left, center, right, back, bottom = [(state[i:i+9]) for i in range(0, len(state), 9)]

        sum = (self.find_most_common_color(top, center_colors['top_color']) +
               self.find_most_common_color(left, center_colors['left_color']) +
               self.find_most_common_color(center, center_colors['center_color']) +
               self.find_most_common_color(right, center_colors['right_color']) +
               self.find_most_common_color(back, center_colors['back_color']) +
               self.find_most_common_color(bottom, center_colors['bottom_color']))
        # print(sum)
        print(state, sum)
        return sum
    
    def find_most_common_color(self, side, center_color):
        return side.count(center_color)

    def num_of_unique_char(self, str):
        s = set(str)
        return len(s)

    def reset(self):
        """
        Input: None
        Description: Reset the cube to its inital state
        Output: None
        """
        self.cube = [[[c for x in range(self.n)] for y in range(self.n)] for c in self.colours]

    def solved(self):
        """
        Input: None
        Description: Determine if the cube is solved or not
        Output: boolean representing if the cube is solved or not
        """
        for side in self.cube:
            hold = []
            check = True
            for row in side:
                if len(set(row)) == 1:
                    hold.append(row[0])
                else:
                    check = False
                    break
            if check == False:
                break
            if len(set(hold)) > 1:
                check = False
                break
        return check

    def stringify(self):
        """
        Input: None
        Description: Create string representation of the current state of the cube
        Output: string representing the cube current state
        """
        return ''.join([i for r in self.cube for s in r for i in s])

    def shuffle(self, l_rot = 5, u_rot = 100):
        """
        Input: l_rot - integer representing the lower bounds of amount of moves (Default = 5) [OPTIONAL]
               u_rot - integer representing the upper bounds of amount of moves (Default = 100) [OPTIONAL]
        Description: Shuffles rubiks cube to random solvable state
        Output: None
        """
        moves = randint(l_rot, u_rot)
        actions = [
            ('h', 0),
            ('h', 1),
            ('v', 0),
            ('v', 1),
            ('s', 0),
            ('s', 1)
        ]
        for i in range(moves):
            a = choice(actions)
            j = randint(0, self.n - 1)
            if a[0] == 'h':
                self.horizontal_twist(j, a[1])
            elif a[0] == 'v':
                self.vertical_twist(j, a[1])
            elif a[0] == 's':
                self.side_twist(j, a[1])

    def show(self):
        """
        Input: None
        Description: Show the rubiks cube
        Output: None
        """
        spacing = f'{" " * (len(str(self.cube[0][0])) + 2)}'
        l1 = '\n'.join(spacing + str(c) for c in self.cube[0])
        l2 = '\n'.join('  '.join(str(self.cube[i][j]) for i in range(1,5)) for j in range(len(self.cube[0])))
        l3 = '\n'.join(spacing + str(c) for c in self.cube[5])
        print(f'{l1}\n\n{l2}\n\n{l3}')

    def horizontal_twist(self, row, direction):
        """
        Input: row - integer representing which row you would like to twist
               direction - boolean representing if you want to twist right or left [left - 0, right - 1]
        Description: Twist desired row of rubiks cube
        Output: None
        """
        if row < len(self.cube[0]):
            if direction == 0: #Twist left
                self.cube[1][row], self.cube[2][row], self.cube[3][row], self.cube[4][row] = (self.cube[2][row],
                                                                                              self.cube[3][row],
                                                                                              self.cube[4][row],
                                                                                              self.cube[1][row])

            elif direction == 1: #Twist right
                self.cube[1][row], self.cube[2][row], self.cube[3][row], self.cube[4][row] = (self.cube[4][row],
                                                                                              self.cube[1][row],
                                                                                              self.cube[2][row],
                                                                                              self.cube[3][row])
            else:
                print(f'ERROR - direction must be 0 (left) or 1 (right)')
                return
            #Rotating connected face
            if direction == 0: #Twist left
                if row == 0:
                    self.cube[0] = [list(x) for x in zip(*reversed(self.cube[0]))] #Transpose top
                elif row == len(self.cube[0]) - 1:
                    self.cube[5] = [list(x) for x in zip(*reversed(self.cube[5]))] #Transpose bottom
            elif direction == 1: #Twist right
                if row == 0:
                    self.cube[0] = [list(x) for x in zip(*self.cube[0])][::-1] #Transpose top
                elif row == len(self.cube[0]) - 1:
                    self.cube[5] = [list(x) for x in zip(*self.cube[5])][::-1] #Transpose bottom
        else:
            print(f'ERROR - desired row outside of rubiks cube range. Please select a row between 0-{len(self.cube[0])-1}')
            return

    def vertical_twist(self, column, direction):
        """
        Input: column - integer representing which column you would like to twist
               direction - boolean representing if you want to twist up or down [down - 0, up - 1]
        Description: Twist desired column of rubiks cube
        Output: None
        """
        if column < len(self.cube[0]):
            for i in range(len(self.cube[0])):
                if direction == 0: #Twist down
                    self.cube[0][i][column], self.cube[2][i][column], self.cube[4][-i-1][-column-1], self.cube[5][i][column] = (self.cube[4][-i-1][-column-1],
                                                                                                                                self.cube[0][i][column],
                                                                                                                                self.cube[5][i][column],
                                                                                                                                self.cube[2][i][column])
                elif direction == 1: #Twist up
                    self.cube[0][i][column], self.cube[2][i][column], self.cube[4][-i-1][-column-1], self.cube[5][i][column] = (self.cube[2][i][column],
                                                                                                                                self.cube[5][i][column],
                                                                                                                                self.cube[0][i][column],
                                                                                                                                self.cube[4][-i-1][-column-1])
                else:
                    print(f'ERROR - direction must be 0 (down) or 1 (up)')
                    return
            #Rotating connected face
            if direction == 0: #Twist down
                if column == 0:
                    self.cube[1] = [list(x) for x in zip(*self.cube[1])][::-1] #Transpose left
                elif column == len(self.cube[0]) - 1:
                    self.cube[3] = [list(x) for x in zip(*self.cube[3])][::-1] #Transpose right
            elif direction == 1: #Twist up
                if column == 0:
                    self.cube[1] = [list(x) for x in zip(*reversed(self.cube[1]))] #Transpose left
                elif column == len(self.cube[0]) - 1:
                    self.cube[3] = [list(x) for x in zip(*reversed(self.cube[3]))] #Transpose right
        else:
            print(f'ERROR - desired column outside of rubiks cube range. Please select a column between 0-{len(self.cube[0])-1}')
            return

    def side_twist(self, column, direction):
        """
        Input: column - integer representing which column you would like to twist
               direction - boolean representing if you want to twist up or down [down - 0, up - 1]
        Description: Twist desired side column of rubiks cube
        Output: None
        """
        if column < len(self.cube[0]):
            for i in range(len(self.cube[0])):
                if direction == 0: #Twist down
                    self.cube[0][column][i], self.cube[1][-i-1][column], self.cube[3][i][-column-1], self.cube[5][-column-1][-1-i] = (self.cube[3][i][-column-1],
                                                                                                                                      self.cube[0][column][i],
                                                                                                                                      self.cube[5][-column-1][-1-i],
                                                                                                                                      self.cube[1][-i-1][column])
                elif direction == 1: #Twist up
                    self.cube[0][column][i], self.cube[1][-i-1][column], self.cube[3][i][-column-1], self.cube[5][-column-1][-1-i] = (self.cube[1][-i-1][column],
                                                                                                                                      self.cube[5][-column-1][-1-i],
                                                                                                                                      self.cube[0][column][i],
                                                                                                                                      self.cube[3][i][-column-1])
                else:
                    print(f'ERROR - direction must be 0 (down) or 1 (up)')
                    return
            #Rotating connected face
            if direction == 0: #Twist down
                if column == 0:
                    self.cube[4] = [list(x) for x in zip(*reversed(self.cube[4]))] #Transpose back
                elif column == len(self.cube[0]) - 1:
                    self.cube[2] = [list(x) for x in zip(*reversed(self.cube[2]))] #Transpose top
            elif direction == 1: #Twist up
                if column == 0:
                    self.cube[4] = [list(x) for x in zip(*self.cube[4])][::-1] #Transpose back
                elif column == len(self.cube[0]) - 1:
                    self.cube[2] = [list(x) for x in zip(*self.cube[2])][::-1] #Transpose top
        else:
            print(f'ERROR - desired column outside of rubiks cube range. Please select a column between 0-{len(self.cube[0])-1}')
            return