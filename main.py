from queue import PriorityQueue

# Manhattan distance as heuristic
def heuristic(state):
    h = 0
    for i in range(3):
        for j in range(10):
            # get the fruit and size of the current cell in the puzzle state
            fruit, size = state[i][j]
            # find the position of the same fruit and size in the goal state and compute the Manhattan distance
            row, col = find_fruit(goal_state, fruit, size)
            h += abs(i - row) + abs(j - col)
    return h

# returns the row and column index of the first occurrence of the given fruit in the puzzle state
def find_fruit(state, fruit, size):
    for i in range(3):
        for j in range(10):
            if state[i][j][0] == fruit and state[i][j][1] == size:
                return i, j
    return -1, -1


# A* search algorithm
def astar(initial_state):
    # create a priority queue to store the states to be explored
    queue = PriorityQueue()
    # add the initial state to the queue with a priority based on the heuristic value and the cost so far (which is zero)
    queue.put((heuristic(initial_state), 0, tuple(map(tuple, initial_state))))

    # create a set to store the visited states
    visited = set()

    # iterate until the priority queue is empty
    while not queue.empty():
        # get the state with the lowest priority (i.e., the lowest estimated cost to reach the goal state)
        _, cost_so_far, current_state = queue.get()

        # if the current state is the goal state, return the path and the cost
        if current_state == tuple(map(tuple, goal_state)):
            return cost_so_far, current_state

        # if the current state has already been visited, skip it
        if current_state in visited:
            continue

        # mark the current state as visited
        visited.add(tuple(map(tuple, current_state)))

        # generate all the possible neighboring states by swapping adjacent fruits in the current state
        for i in range(3):
            for j in range(10):
                # check if it's possible to swap the current fruit with the one to its right
                if j < 9:
                    next_state = [list(row) for row in current_state]

                    # create a new state by swapping the current fruit with the one to its right
                    next_state[i][j], next_state[i][j+1] = next_state[i][j+1], next_state[i][j]

                    # check if the new state has not been visited yet
                    if tuple(map(tuple, next_state)) not in visited:
                        # compute the cost of the new state as the cost so far plus one (i.e., the cost of the current state plus the cost of the move)
                        new_cost = cost_so_far + 1
                        # add the new state to the priority queue with a priority based on the heuristic value and the cost of the path to reach the new state
                        queue.put((new_cost + heuristic(next_state),
                                  new_cost, tuple(map(tuple, next_state))))

                # check if it's possible to swap the current fruit with the one to its up
                if i < 2:
                    next_state = [list(row) for row in current_state]
                    next_state[i][j], next_state[i+1][j] = next_state[i+1][j], next_state[i][j]
                    if tuple(map(tuple, next_state)) not in visited:
                        new_cost = cost_so_far + 1
                        queue.put((new_cost + heuristic(next_state),
                                  new_cost, tuple(map(tuple, next_state))))

    return None


initial_state = [
    [('apple', 5), ('apple', 4), ('apple', 6), ('apple', 1), ('apple', 9),
     ('apple', 3), ('apple', 0), ('apple', 2), ('apple', 8), ('apple', 7)],
    [('banana', 8), ('banana', 1), ('banana', 9), ('banana', 4), ('banana', 3),
     ('banana', 7), ('banana', 2), ('banana', 5), ('banana', 6), ('banana', 0)],
    [('orange', 0), ('orange', 4), ('orange', 2), ('orange', 3), ('orange', 9),
     ('orange', 6), ('orange', 1), ('orange', 8), ('orange', 7), ('orange', 5)]
]

goal_state = [
    [('apple', i) for i in range(10)],
    [('orange', i) for i in range(10)],
    [('banana', i) for i in range(10)]
]

_, result = astar(initial_state)

if result is not None:
    for i in range(3):
        print(result[i])
else:
    print("No solution found.")

print("cost ", _)
