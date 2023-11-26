from search import *

class RubiksCube(Problem):
    def __init__(self, initial=frozenset(['F', 'G', 'W', 'C']), goal=frozenset()):
        super().__init__(initial, goal)

    def goal_test(self, state):
        return state == self.goal
    
    def result(self, state, action):
        new_state = set(state)

        if 'F' in state:
            if action == {'F'}:
                new_state.remove('F')
            if action == {'F', 'W'}:
                new_state.remove('F')
                new_state.remove('W')
            if action == {'F', 'G'}:
                new_state.remove('F')
                new_state.remove('G')
            if action == {'F', 'C'}:
                new_state.remove('F')
                new_state.remove('C')
        if 'F' not in state:
            if action == {'F'}:
                new_state.add('F')
            if action == {'F', 'W'}:
                new_state.add('F')
                new_state.add('W')
            if action == {'F', 'G'}:
                new_state.add('F')
                new_state.add('G')
            if action == {'F', 'C'}:
                new_state.add('F')
                new_state.add('C')

        return frozenset(new_state)
    
    def actions(self, state):
        possible_actions = [
                            {'F'},
                            {'F', 'W'},
                            {'F', 'G'},
                            {'F', 'C'}]
                            
        # initial state
        if state == self.initial:
            return [{'F', 'G'}]
        
        if 'F' in state:
            if 'W' not in state:
                possible_actions.remove({'F', 'W'})
                if 'G' in state:
                    if 'C' in state:
                        possible_actions.remove({'F'})
            if 'G' not in state:
                possible_actions.remove({'F', 'G'})
            if 'C' not in state:
                possible_actions.remove({'F', 'C'})
                if 'G' in state:
                    if 'W' in state:
                        possible_actions.remove({'F'})
        else:
            if 'W' in state:
                possible_actions.remove({'F', 'W'})
                if 'G' not in state:
                    if 'C' not in state:
                        possible_actions.remove({'F'})
            if 'G' in state:
                possible_actions.remove({'F', 'G'})
            if 'C' in state:
                possible_actions.remove({'F', 'C'})
                if 'G' not in state:
                    if 'W' not in state:
                        possible_actions.remove({'F'})
        return possible_actions

