import unittest

from dgraph import DGraph
from search import astar, bfs, dfs, ids, tilegame_heuristic
from tilegameproblem import TileGame
import time
import multiprocessing

def timeit(f):

    def timed(*args, **kw):

        # ts = time.time()
        # result = f(*args, **kw)
        # te = time.time()

        p = multiprocessing.Process(target=lambda: f(*args, **kw))
        ts = time.time()
        p.start()

        # Wait for 10 seconds or until process finishes
        p.join(120)
        if p.is_alive():
            p.kill()
        te = time.time()

        if te - ts >= 120:
            print(f'func: {f.__name__}; args: {args}; kwargs: {kw}; took over 120 seconds')
        else:
            print(f'func: {f.__name__}; args: {args}; kwargs: {kw}; took: {te - ts:.2f} seconds')

        # # If thread is still active
        # if p.is_alive():
        #     print "running... let's kill it..."

        #     # Terminate - may not work if process is stuck for good
        #     p.terminate()
        #     # OR Kill - will work for sure, no chance for process to finish nicely however
        #     # p.kill()

        #     p.join()

        #print(f'func: {f.__name__}; args: {args}; kwargs: {kw}; took: {te - ts:.2f} seconds')

    return timed


class IOTest(unittest.TestCase):
    """
    Tests IO for search implementations. Contains basic/trivial test cases.

    Each test function instantiates a search problem (TileGame) and tests if the three test case
    contains the solution, the start state is in the solution, the end state is in the
    solution and, if applicable, if the length of the solutions are the same.

    These tests are not exhaustive and do not check if your implementation follows the
    algorithm correctly. We encourage you to create your own tests as necessary.
    """

    def _check_algorithm(self, algorithm):
        simple_state = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
        # Construct a TileGame where the start and goal states are the same
        tg = TileGame(3, simple_state, simple_state)
        path = algorithm(tg)
        self.assertEqual(
            path[0], simple_state, "Path should start with the start state"
        )
        self.assertEqual(path[-1], simple_state, "Path should end with the goal state")
        self.assertEqual(len(path), 1, "Path length should be one")

    @timeit
    def _problem_1_1(self, algorithm, shortest):
        simple_problem = ((1))
        goal_state = ((1))
        # Construct a small TileGame one state away from the goal
        tg = TileGame(1, simple_problem, goal_state)
        path = algorithm(tg)
        self.assertEqual(
            path[0], simple_problem, "Path should start with the start state"
        )
        self.assertEqual(path[-1], goal_state, "Path should end with the goal state")
        if shortest:
            self.assertEqual(len(path), 1, "Path length should be one")

    @timeit
    def _problem_2_1(self, algorithm, shortest):
        simple_problem = ((1, 2),(3, 4))
        goal_state = ((1,2), (3, 4))
        # Construct a small TileGame one state away from the goal
        tg = TileGame(2, simple_problem, goal_state)
        path = algorithm(tg)
        self.assertEqual(
            path[0], simple_problem, "Path should start with the start state"
        )
        self.assertEqual(path[-1], goal_state, "Path should end with the goal state")
        if shortest:
            #print("Path for problem 3: ")
            #TileGame.print_pretty_path(path)
            self.assertEqual(len(path), 1, "Path length should be 1")

    @timeit
    def _problem_2_2(self, algorithm, shortest):
        simple_problem = ((3, 2),(1, 4))
        goal_state = ((1,2), (3, 4))
        # Construct a small TileGame one state away from the goal
        tg = TileGame(2, simple_problem, goal_state)
        path = algorithm(tg)
        self.assertEqual(
            path[0], simple_problem, "Path should start with the start state"
        )
        self.assertEqual(path[-1], goal_state, "Path should end with the goal state")
        if shortest:
            #print("Path for problem 3: ")
            #TileGame.print_pretty_path(path)
            self.assertEqual(len(path), 2, "Path length should be 2")

    @timeit
    def _problem_2_3(self, algorithm, shortest):
        simple_problem = ((4, 3),(2, 1))
        goal_state = ((1,2), (3, 4))
        # Construct a small TileGame one state away from the goal
        tg = TileGame(2, simple_problem, goal_state)
        path = algorithm(tg)
        self.assertEqual(
            path[0], simple_problem, "Path should start with the start state"
        )
        self.assertEqual(path[-1], goal_state, "Path should end with the goal state")
        if shortest:
            #print("Path for problem 3: ")
            #TileGame.print_pretty_path(path)
            self.assertEqual(len(path), 5, "Path length should be 5")

    @timeit
    def _problem_2_4(self, algorithm, shortest):
        simple_problem = ((1, 2),(3, 4))
        goal_state = ((3,2), (1, 4))
        # Construct a small TileGame one state away from the goal
        tg = TileGame(2, simple_problem, goal_state)
        path = algorithm(tg)
        self.assertEqual(
            path[0], simple_problem, "Path should start with the start state"
        )
        self.assertEqual(path[-1], goal_state, "Path should end with the goal state")
        if shortest:
            #print("Path for problem 3: ")
            #TileGame.print_pretty_path(path)
            self.assertEqual(len(path), 2, "Path length should be 2")

    @timeit
    def _problem_3_1(self, algorithm, shortest):
        simple_problem = ((9,8,7),(6,5,4),(3,2,1))
        goal_state = ((1,2,3),(4,5,6),(7,8,9))
        # Construct a small TileGame one state away from the goal
        tg = TileGame(3, simple_problem, goal_state)
        path = algorithm(tg)
        self.assertEqual(
            path[0], simple_problem, "Path should start with the start state"
        )
        self.assertEqual(path[-1], goal_state, "Path should end with the goal state")
        if shortest:
            #print("Path for problem 2: ")
            #TileGame.print_pretty_path(path)
            self.assertEqual(len(path), 17, "Path length should be 17")

    @timeit
    def _problem_3_2(self, algorithm, shortest):
        simple_problem = ((1,2,3),(4,5,6),(7,8,9))
        goal_state = ((1,2,3),(4,5,6),(7,8,9))
        # Construct a small TileGame one state away from the goal
        tg = TileGame(3, simple_problem, goal_state)
        path = algorithm(tg)
        self.assertEqual(
            path[0], simple_problem, "Path should start with the start state"
        )
        self.assertEqual(path[-1], goal_state, "Path should end with the goal state")
        if shortest:
            #print("Path for problem 2: ")
            #TileGame.print_pretty_path(path)
            self.assertEqual(len(path), 1, "Path length should be 1")
    
    @timeit
    def _problem_3_3(self, algorithm, shortest):
        simple_problem = ((8,2,4),(6,3,1),(9,5,7))
        goal_state = ((1,2,3),(4,5,6),(7,8,9))
        # Construct a small TileGame one state away from the goal
        tg = TileGame(3, simple_problem, goal_state)
        path = algorithm(tg)
        self.assertEqual(
            path[0], simple_problem, "Path should start with the start state"
        )
        self.assertEqual(path[-1], goal_state, "Path should end with the goal state")
        if shortest:
            #print("Path for problem 2: ")
            #TileGame.print_pretty_path(path)
            self.assertEqual(len(path), 11, "Path length should be 11")
    
    @timeit
    def _problem_3_4(self, algorithm, shortest):
        simple_problem = ((3,2,1),(6,5,4),(9,8,7))
        goal_state = ((1,2,3),(4,5,6),(7,8,9))
        # Construct a small TileGame one state away from the goal
        tg = TileGame(3, simple_problem, goal_state)
        path = algorithm(tg)
        self.assertEqual(
            path[0], simple_problem, "Path should start with the start state"
        )
        self.assertEqual(path[-1], goal_state, "Path should end with the goal state")
        if shortest:
            #print("Path for problem 2: ")
            #TileGame.print_pretty_path(path)
            self.assertEqual(len(path), 10, "Path length should be 10")
    
    @timeit
    def _problem_3_5(self, algorithm, shortest):
        simple_problem = ((9,8,7),(6,5,4),(3,2,1))
        goal_state = ((4,5,3),(1,2,6),(7,8,9))
        # Construct a small TileGame one state away from the goal
        tg = TileGame(3, simple_problem, goal_state)
        path = algorithm(tg)
        self.assertEqual(
            path[0], simple_problem, "Path should start with the start state"
        )
        self.assertEqual(path[-1], goal_state, "Path should end with the goal state")
        if shortest:
            #print("Path for problem 2: ")
            #TileGame.print_pretty_path(path)
            self.assertEqual(len(path), 15, "Path length should be 15")

    @timeit
    def _problem_4_1(self, algorithm, shortest):
        simple_problem = ((1,2,3,4),(5,6,7,8),(9,10,11,12),(13,14,15,16))
        goal_state = ((1,2,3,4),(5,6,7,8),(9,10,11,12),(13,14,15,16))
        # Construct a small TileGame one state away from the goal
        tg = TileGame(4, simple_problem, goal_state)
        path = algorithm(tg)
        self.assertEqual(
            path[0], simple_problem, "Path should start with the start state"
        )
        self.assertEqual(path[-1], goal_state, "Path should end with the goal state")
        if shortest:
            #print("Path for problem 2: ")
            #TileGame.print_pretty_path(path)
            self.assertEqual(len(path), 1, "Path length should be 1")

    @timeit
    def _problem_4_2(self, algorithm, shortest):
        simple_problem = ((1,3,2,4),(5,6,8,7),(9,11,10,12),(16,14,15,13))
        goal_state = ((1,2,3,4),(5,6,7,8),(9,10,11,12),(13,14,15,16))
        # Construct a small TileGame one state away from the goal
        tg = TileGame(4, simple_problem, goal_state)
        path = algorithm(tg)
        self.assertEqual(
            path[0], simple_problem, "Path should start with the start state"
        )
        self.assertEqual(path[-1], goal_state, "Path should end with the goal state")
        if shortest:
            #print("Path for problem 2: ")
            #TileGame.print_pretty_path(path)
            self.assertEqual(len(path), 9, "Path length should be 9")

    @timeit
    def _problem_4_3(self, algorithm, shortest):
        simple_problem = ((4,1,2,3),(6,7,8,5),(9,11,12,10),(16,13,14,15))
        goal_state = ((1,2,3,4),(5,6,7,8),(9,10,11,12),(13,14,15,16))
        # Construct a small TileGame one state away from the goal
        tg = TileGame(4, simple_problem, goal_state)
        path = algorithm(tg)
        self.assertEqual(
            path[0], simple_problem, "Path should start with the start state"
        )
        self.assertEqual(path[-1], goal_state, "Path should end with the goal state")
        if shortest:
            #print("Path for problem 2: ")
            #TileGame.print_pretty_path(path)
            self.assertEqual(len(path), 12, "Path length should be 12")

    @timeit
    def _problem_4_4(self, algorithm, shortest):
        simple_problem = ((3,2,1,4),(5,6,7,8),(9,11,10,12),(14,15,16,13))
        goal_state = ((1,2,3,4),(5,6,7,8),(9,10,11,12),(13,14,15,16))
        # Construct a small TileGame one state away from the goal
        tg = TileGame(4, simple_problem, goal_state)
        path = algorithm(tg)
        self.assertEqual(
            path[0], simple_problem, "Path should start with the start state"
        )
        self.assertEqual(path[-1], goal_state, "Path should end with the goal state")
        if shortest:
            #print("Path for problem 2: ")
            #TileGame.print_pretty_path(path)
            self.assertEqual(len(path), 8, "Path length should be 8")

    def _check_dgraph(self, algorithm):
        # Construct a small DGraph one state away from the goal
        dg = DGraph([[None, 1], [1, None]], {1})
        path = algorithm(dg)
        self.assertEqual(path[0], 0, "Path should start with the start state")
        self.assertEqual(path[-1], 1, "Path should end with the goal state")
        self.assertEqual(len(path), 2, "Path length should be two")

    def test_bfs(self):
        print("Testing bfs")
        self._check_algorithm(bfs)
        self._problem_1_1(bfs, True)
        self._problem_2_1(bfs, True)
        self._problem_2_2(bfs, True)
        self._problem_2_3(bfs, True)
        self._problem_2_4(bfs, True)
        self._problem_3_1(bfs, True)
        self._problem_3_2(bfs, True)
        self._problem_3_3(bfs, True)
        self._problem_3_4(bfs, True)
        self._problem_3_5(bfs, True)
        self._problem_4_1(bfs, True)
        self._problem_4_2(bfs, True)
        self._problem_4_3(bfs, True)
        self._problem_4_4(bfs, True)
        self._check_dgraph(bfs)

    def test_dfs(self):
        print("Testing dfs")
        self._check_algorithm(dfs)
        self._problem_1_1(dfs, False)
        self._problem_2_1(dfs, False)
        self._problem_2_2(dfs, False)
        self._problem_2_3(dfs, False)
        self._problem_2_4(dfs, False)
        self._problem_3_1(dfs, False)
        self._problem_3_2(dfs, False)
        self._problem_3_3(dfs, False)
        self._problem_3_4(dfs, False)
        self._problem_3_5(dfs, False)
        self._problem_4_1(dfs, False)
        self._problem_4_2(dfs, False)
        self._problem_4_3(dfs, False)
        self._problem_4_4(dfs, False)
        self._check_dgraph(dfs)

    def test_ids_output(self):
        self._check_algorithm(ids)
        self._problem_1_1(ids, True)
        self._problem_2_1(ids, True)
        self._problem_2_2(ids, True)
        self._problem_2_3(ids, True)
        self._problem_2_4(ids, True)
        self._problem_3_1(ids, True)    
        self._problem_3_2(ids, True)
        self._problem_3_3(ids, True)
        self._problem_3_4(ids, True)
        self._problem_3_5(ids, True)
        self._problem_4_1(ids, True)
        self._problem_4_2(ids, True)
        self._problem_4_3(ids, True)
        self._problem_4_4(ids, True)
        self._check_dgraph(ids)

    def test_astar_output(self):
        alg = lambda p: astar(p, lambda s: tilegame_heuristic(s))
        self._check_algorithm(alg)
        self._problem_1_1(alg, True)
        self._problem_2_1(alg, True)
        self._problem_2_2(alg, True)
        self._problem_2_3(alg, True)
        self._problem_2_4(alg, True)
        self._problem_3_1(alg, True)
        self._problem_3_2(alg, True)
        self._problem_3_3(alg, True)
        self._problem_3_4(alg, True)
        self._problem_3_5(alg, True)
        self._problem_4_1(alg, True)
        self._problem_4_2(alg, True)
        self._problem_4_3(alg, True)
        self._problem_4_4(alg, True)
        self._check_dgraph(lambda p: astar(p, lambda s: 0))


if __name__ == "__main__":
    print("Unit testing started")
    unittest.main()
