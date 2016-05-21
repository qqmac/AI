'''
Quyen Mac
ECE 4524
Project 1
'''

from search import Problem, astar_search, Node
import utils

# main public function
# debug parameter toggles debug output. It is set as 0 automatically, any number 1 or greater would toggle it.
def solve(initial, goal, heur, debug=0):
    '''
    8 puzzle using A* search
    using misplaced and cityblock heuristics
    '''
    # return a list that indicates the sequence of steps that are needed to reach the goal state
    # if no solution exists, return 'None'

    # list to be returned
    results = list()

    if valid_input(initial, goal, heur, debug):
        # Valid inputs, convert to tuples
        init_node = tuple(initial)
        goal_node    = tuple(goal)
        heuristic    = (heur == 'cityblock')

        ##################################################
        # Debug tuple conversion
        if debug >= 1:
            print("Node Initial: ", init_node)
            print("Node Goal: ", goal_node)
            if heuristic:
                print("CityBlock Heuristic")
            else:
                print("Misplaced Heuristic")
        ##################################################

        # astar problem and result
        astar_problem  = Puzzle(init_node, goal_node, heuristic, debug)
        astar_results = astar_search(astar_problem)
        if isinstance(astar_results, (Node) ):
            results = astar_results.solution()
            if debug == 0:
                if len(results) == 0:
                    print ("None")
                else:
                    print results
        else:
            print("None")

    ##################################################
    if debug >= 1:
        print("Solve returning: ", results)
    ##################################################

    return results

def valid_input(initial, goal, heur, debug=0):
    '''
    If input is valid
    Returns true or false
    '''

    # boolean
    results = True

    # Verify Types
    results = results and isinstance(initial, (list))
    results = results and isinstance(goal, (list))
    results = results and ('misplaced' == heur or 'cityblock' == heur)
    results = results and isinstance(debug, (int) )

    ##################################################
    if results and debug >= 1:
        print("input type valid")
    ##################################################

    # Verify Lengths
    if results:
        results = results and len(initial) == 9
        results = results and len(goal) == 9

    ##################################################
    if results and debug >= 1:
        print("input length valid")

    # Debug Output for entire function
    if results and debug >= 1:
        print("valid_input passed")
    elif not results:
        print("valid_input failed")
    ##################################################

    return results


def emptyIndex(state):
    # takes the state and returns the index of the empty tile
    i = 0

    # Iterate over tuple to find empty
    while i < len(state):
        if state[i] == 0:
            return i
        i += 1

    # no empty value
    print("Error: Empty value was not found in state: \n", state)
    return 9

def distance(index1, index2, debug=0):
    # get the horizontal, vertical, and diagonal distance
    results   = 0

    index1_row    = index1/3
    index2_row    = index2/3

    index1_column = index1%3
    index2_column = index2%3

    ###############################################
    if debug >= 1:
        print("distance of ",index1, index2)
        print("index1 row: ", index1_row)
        print("index1 column: ", index2_column)
        print("index2 row: ", index2_row)
        print("index2 column: ", index2_column)
    ###############################################

    # Values in same column
    # Distance is difference of the two rows
    elif index1_column == index2_column:
        if index2_row > index1_row:
            results = index2_row - index1_row
        else:
            results = index1_row - index2_row

    # Values in same row
    # Distance is difference of the two columns
    if index1_row == index2_row:
        if index2_column > index1_column:
            results = index2_column - index1_column
        else:
            results = index1_column - index2_column

    # Diagonal
    # Distance is the difference in columns + difference in rows
    else:
        if (index2_row >= index1_row) and (index2_column >= index1_column):
            results = (index2_column - index1_column) + (index2_row - index1_row)

        elif (index2_row >= index1_row) and (index2_column <= index1_column):
            results = (index1_column - index2_column) + (index2_row - index1_row)

        elif (index2_row <= index1_row) and (index2_column >=  index1_column):
            results = (index2_column - index1_column) + (index1_row - index2_row)

        elif (index2_row <= index1_row) and (index2_column <= index1_column):
            results = (index1_column - index2_column) + (index1_row - index2_row)

        else:
            print("Error with distance and diagonal distance")
            print("Indices: ", index1, index2)

    #########################################
    if debug >= 1:
        print("distance returns ", results)
    #########################################

    return results


# Class Puzzle ---------------------------------------------------------
class Puzzle(Problem):

    # key is the empty state index
    actionPairs = { 0 : (1, 3), 1 : (0, 2, 4), 2 : (1, 5), 3 : (0, 4, 6), 
    4 : (1, 3, 5, 7), 5 : (2, 4, 8), 6 : (3, 7), 7 : (4, 6, 8), 8 : (5, 7) }

    # override functions
    # init constructor
    def __init__(self, initial, goal, heuristic=False, debug=0):
        self.initial   = initial
        self.goal      = goal
        self.heuristic = heuristic
        self.debug   = debug

    # for astar_search, was getting errors before
    def h(self, node):
        return self.value(node.state)

    # return actions executed in the given state
    def actions(self, state):

        # Assume that the state is correct
        results = self.actionPairs.get(emptyIndex(state), tuple())

        #################################################
        if self.debug >= 1:
            print("Actions returning: ", results)
            print("Actions state: ", state)
            print("Actions goal: ", self.goal)
        #################################################

        return results

    # return state that results from executing the given action in the state
    def result(self, state, action):

        # Assume that the action and state are correct
        # Convert state to list
        state_list = list(state)
        a, b = state_list.index(0), action
        state_list[a], state_list[b] = state_list[b], state_list[a]
        results = tuple(state_list)

        #########################################################
        if self.debug >= 1:
            print("state: ", state)
            print("action: ", action)
            print("empty index: ", a)
            print("returning state: ", results)
        #########################################################

        return results

    # value at each state, for the two heuristics
    def value(self, state):
        if self.heuristic:
            results = self.cityblock(state)
        else:
            results = self.misplaced(state)

        return results

        # get misplaced tiles
    def misplaced_tiles(self, state):
        i = 0

        while i < len(state):
            if not state[i] == self.goal[i]:
                yield i
            i += 1

    # get index of value at goal
    def index_goal(self, tile):
        results = 9

        for i in self.goal:
            if i == tile:
                return i

        # if no index found
        return results

    # city block heuristic
    def cityblock(self, state):
        # count moves in the horizontal and vertical position
        results = 0

        for i in self.misplaced_tiles(state):
            results += distance(i, self.index_goal(state[i]))

            #####################################################
            if self.debug >= 1:
                print("tile out of place at ", i)

        if self.debug >= 1:
            print("cityblock returns ", results)
        ######################################################

        return results

    # misplaced heuristic
    def misplaced(self, state):
        results = 0

        for i in self.misplaced_tiles(state):
            results += 1
            if self.debug >= 1:
                print("tile out of place at ", i)

        if self.debug >= 1:
            print("misplaced returns ", results)

        return results

if __name__ == '__main__':
    initial = [3, 1, 2, 6, 4, 5, 0, 7, 8]
    goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    solve(initial, goal, 'cityblock')
    solve(initial, goal, 'misplaced')

    # this would print out the debug outputs, uncomment it to see the debug output
    # solve(initial, goal, 'cityblock', 1)
    # solve(initial, goal, 'misplaced', 1)

    initial = [4, 5, 1, 7, 6, 2, 0, 8, 3]
    goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    solve(initial, goal, 'cityblock')
    solve(initial, goal, 'misplaced')

    # solve(initial, goal, 'cityblock', 1)
    # solve(initial, goal, 'misplaced', 1)

    initial = [1, 4, 2, 3, 0, 5, 6, 7, 8]
    goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    solve(initial, goal, 'cityblock')
    solve(initial, goal, 'misplaced')

    # solve(initial, goal, 'cityblock', 1)
    # solve(initial, goal, 'misplaced', 1)

    initial = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    solve(initial, goal, 'cityblock')
    solve(initial, goal, 'misplaced')

    # solve(initial, goal, 'cityblock', 1)
    # solve(initial, goal, 'misplaced', 1)

