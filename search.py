# NOTE TO STUDENT: Please read the handout before continuing.

from queue import LifoQueue, PriorityQueue, Queue
import queue
from typing import Callable, List

from dgraph import DGraph
from searchproblem import SearchProblem, State
from tilegameproblem import TileGame, TileGameState


### GENERAL SEARCH IMPLEMENTATIONS - NOT SPECIFIC TO THE TILEGAME PROBLEM ###

## write the iterations out on paper##
def search(problem: SearchProblem[State], states) -> List[State]:
    start_state = problem.get_start_state()
    states.put(start_state)
    parent = {}
    visited_states = set()
    visited_states.add(start_state)

    while not states.empty():
        state = states.get()
        if problem.is_goal_state(state):
            path = []
            while state in parent:
                path.append(state)
                state = parent[state]
            path.append(state)
            return path[::-1]

        for child_state in problem.get_successors(state):
            if child_state not in visited_states:
                states.put(child_state)
                parent[child_state] = state
                visited_states.add(child_state)
                
    return []  

def id_search(problem: SearchProblem[State], max_depth) -> List[State]:
    states = LifoQueue()
    start_state = problem.get_start_state()
    states.put(start_state)
    parent = {}
    state_to_depth = {}
    state_to_depth[start_state] = 0

    while not states.empty():
        state = states.get()
        if problem.is_goal_state(state):
            path = []
            while state in parent:
                path.append(state)
                state = parent[state]
            path.append(state)
            return path[::-1]

        if state_to_depth[state] < max_depth:
            for child_state in problem.get_successors(state):
                if child_state not in state_to_depth or state_to_depth[child_state] > state_to_depth[state] + 1:
                    state_to_depth[child_state] = state_to_depth[state] + 1
                    states.put(child_state)
                    parent[child_state] = state
                    
    return []   


def bfs(problem: SearchProblem[State]) -> List[State]:
    """
    Implement breadth-first search.

    Input:
        problem - the problem on which the search is conducted, a SearchProblem

    Output: a list of states representing the path of the solution

    """
    states = Queue()
    return search(problem, states)

def dfs(problem: SearchProblem[State]) -> List[State]:
    """
    Implement depth-first search.

    Input:
        problem - the problem on which the search is conducted, a SearchProblem

    Output: a list of states representing the path of the solution

    """
    states = LifoQueue()
    return search(problem, states)

def ids(problem: SearchProblem[State]) -> List[State]:
    """
    Implement iterative deepening search.

    Input:
        problem - the problem on which the search is conducted, a SearchProblem

    Output: a list of states representing the path of the solution

    """
    depth = 0
    while True:
         solution = id_search(problem, depth)
         if solution != []:
             return solution
         depth += 1


def astar(problem: SearchProblem[State], heur: Callable[[State], float]) -> List[State]:
    """
    Implement A* search.

    The given heuristic function will take in a state of the search problem
    and produce a real number.

    Your implementation should be able to work with any heuristic
    that is for the given search problem (but, of course, without a
    guarantee of optimality if the heuristic is not admissible).

    Input:
        problem - the problem on which the search is conducted, a SearchProblem
        heur - a heuristic function that takes in a state as input and outputs a number

    Output: a list of states representing the path of the solution

    """
    states = PriorityQueue()
    start_state = problem.get_start_state()
    states.put((heur(start_state), start_state))
    parent = {}
    cost_so_far = {}
    cost_so_far[start_state] = 0

    while not states.empty():
        _, state = states.get()
        if problem.is_goal_state(state):
            path = []
            while state in parent:
                path.append(state)
                state = parent[state]
            path.append(state)
            return path[::-1]

        for child_state, cost in problem.get_successors(state).items():
            if child_state not in cost_so_far:
                parent[child_state] = state
                cost_so_far[child_state] = cost_so_far[state] + cost
                states.put((cost_so_far[child_state] + heur(child_state), child_state))
                    
    return []   


### SPECIFIC TO THE TILEGAME PROBLEM ###


def tilegame_heuristic(state: TileGameState) -> float:
    """
    Produces a number for the given tile game state representing
    an estimate of the cost to get to the goal state. Remember that this heuristic must be
    admissible, that is it should never overestimate the cost to reach the goal.
    Input:
        state - the tilegame state to evaluate. Consult handout for how the tilegame state is represented

    Output: a float.

    """
    size = len(state)
    cost  = 0
    for n_row, row in enumerate(state):
        for n_col, tile in enumerate(row):
            cost += abs(n_row - (tile - 1) // size) + abs(n_col - (tile - 1)%size)
    return cost //2

### YOUR SANDBOX ###


def main():
    """
    Do whatever you want in here; this is for you.
    The examples below shows how your functions might be used.
    """

    # initialize a random 3x3 TileGame problem
    tg = TileGame(3)
    # print(TileGame.board_to_pretty_string(tg.get_start_state()))
    # compute path using dfs
    print("Running dfs")
    path = dfs(tg)
    # display path
    TileGame.print_pretty_path(path)

    print("Running bfs")
    path = bfs(tg)
    # display path
    TileGame.print_pretty_path(path)

    # # initialize a small DGraph
    # small_dgraph = DGraph([[None, 1], [1, None]], {1})
    # # print the path using ids
    # print(ids(small_dgraph))


if __name__ == "__main__":
    main()
