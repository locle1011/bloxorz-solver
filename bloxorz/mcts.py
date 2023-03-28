import numpy as np
import random
import time
from collections import deque
from state import State
from state import Action

ROW = 0
COL = 1
C_ABYSS = ' '
C_GREYTILE = '█'
C_HOLE = '#'
C_ORANGETILE = '▒'
C_SOFTSWITCH = 'O'
C_HARDSWITCH = 'X'
C_TELEPORTSWITCH = 'C'


class MCTSNode:
    def __init__(self, game_state: State, parent=None):
        self.gameState = game_state
        self.children = []
        self.parent = parent
        self.untriedStates = None
        self.visitNum = 0
        self.points = -1.0

        def _get_result(current_state: State, mask_list: list, points_list=None):
            if current_state.is_goal():
                return 1.0

            if points_list is not None:
                points = np.array(points_list)
                if mask_list[3]:
                    return points[2]
                if any(x for x in mask_list[0:2]):
                    return np.max(points[0:2][mask_list[0:2]])

            return 0.0

        self.get_result = _get_result

    def copy(self):
        game_state = self.gameState.copy()
        return MCTSNode(game_state)

    @property
    def n(self):
        return self.visitNum

    @property
    def q(self):
        return self.points

    @staticmethod
    def get_rollout_policy(game_state: State, simulation_hash_table: deque):
        actions = list(Action)
        random.shuffle(actions)
        for action in actions:
            test_game_state = game_state.copy()
            if test_game_state.perform(action):
                if not test_game_state.is_end():
                    if test_game_state not in simulation_hash_table:
                        return test_game_state
        returned_game_state = game_state.copy()
        returned_game_state.perform(actions[0])
        return returned_game_state

    def get_untried_actions(self):
        if self.untriedStates is None:
            self.untriedStates = []
            for action in Action:
                test_game_state = self.gameState.copy()
                if test_game_state.perform(action):
                    if not test_game_state.is_end():
                        self.untriedStates.append(test_game_state)
            random.shuffle(self.untriedStates)
        return self.untriedStates

    def expand(self, hash_table):
        next_game_state = self.get_untried_actions().pop()
        if next_game_state.encode() in hash_table:
            return None
        mcst_child_node = MCTSNode(next_game_state, self)
        self.children.append(mcst_child_node)
        return mcst_child_node

    def is_terminal_node(self):
        return self.gameState.is_end() or self.gameState.is_goal()

    def get_best_child(self, c=1.0):
        if len(self.children) == 0:
            return None

        if any(child.q != 0.0 for child in self.children):
            c = 0
        weights = [child.q + c * np.sqrt((np.log(self.n)) / child.n) for child in self.children]

        return self.children[np.argmax(weights)]

    def is_fully_expanded(self):
        return len(self.get_untried_actions()) == 0

    @staticmethod
    def handle_result(first_game_state: State, second_game_state: State):
        if not first_game_state.box.is_splitted() and second_game_state.box.is_splitted():
            return 1

        if first_game_state.board.to_string().count(C_GREYTILE) \
                < second_game_state.board.to_string().count(C_GREYTILE):
            return 2
        elif first_game_state.board.to_string().count(C_GREYTILE) \
                > second_game_state.board.to_string().count(C_GREYTILE):
            return 3

        return 0

    def simulate(self, previous_game_state: State, explored_nodes: set, max_simulation_depth=10,
                 max_previous_nodes=2, points_list=None):
        current_game_state = self.gameState

        mask_list = [False, False, False, False]

        index = self.handle_result(previous_game_state, current_game_state)
        if index:
            mask_list[index - 1] = True
        if index == 3:
            mask_list[3] = True

        simulation_hash_table = deque()
        solution = []

        depth = 0

        while not current_game_state.is_goal() and not current_game_state.is_end():
            if depth > max_simulation_depth:
                break

            test_game_state = self.get_rollout_policy(current_game_state, simulation_hash_table)
            if test_game_state is None:
                break
            simulation_hash_table.append(test_game_state)
            if len(simulation_hash_table) > max_previous_nodes:
                simulation_hash_table.popleft()

            if points_list is not None:
                index = self.handle_result(current_game_state, test_game_state)
                if index:
                    mask_list[index - 1] = True
                if index == 3 and not mask_list[0] and not mask_list[1]:
                    mask_list[3] = True
            solution.append(test_game_state)

            if test_game_state.encode() not in explored_nodes:
                explored_nodes.add(test_game_state)

            current_game_state = test_game_state
            depth += 1

        del simulation_hash_table

        if current_game_state.is_goal():
            return self.get_result(current_game_state, mask_list), solution

        del solution
        return self.get_result(current_game_state, mask_list, points_list), []

    def backpropagate(self, result):
        self.visitNum += 1
        self.points = max(self.points, result)
        if self.parent:
            self.parent.backpropagate(result)


class MCTS:
    def __init__(self, state: State, simulation_number=None, simulation_time=None, max_simulation_depth=30,
                 max_previous_nodes=2, points_list=None, is_unique_node=False, c=1.4):
        self.root = MCTSNode(state)
        self.simulationNumber = simulation_number
        self.simulationTime = simulation_time
        self.maxSimulationDepth = max_simulation_depth
        self.maxPreviousNodes = max_previous_nodes
        self.pointsList = points_list
        self.isUniqueNode = is_unique_node
        self.c = c

        self.hashTable = set()
        if self.isUniqueNode:
            self.hashTable.add(self.root.gameState.encode())
        self.exploredNodes = set()
        self.exploredNodes.add(self.root.gameState.encode())

    def solve(self):
        if self.simulationNumber is not None:
            returned_solution = None
            for i in range(self.simulationNumber):
                solution = []
                child = self.tree_policy(solution)
                if child.gameState.is_goal():
                    return solution, len(self.exploredNodes)
                if self.isUniqueNode and child.gameState.encode() not in self.hashTable:
                    self.hashTable.add(child.gameState.encode())
                if child.gameState.encode() not in self.exploredNodes:
                    self.exploredNodes.add(child.gameState.encode())
                result, extended_solution_list = child.simulate(child.parent.gameState, self.exploredNodes,
                                                                max_simulation_depth=self.maxSimulationDepth,
                                                                max_previous_nodes=self.maxPreviousNodes)
                if len(extended_solution_list) > 0:
                    solution.extend(extended_solution_list)
                    return solution, len(self.exploredNodes)
                child.backpropagate(result)
                returned_solution = solution
            return returned_solution, len(self.exploredNodes)

        elif self.simulationTime is not None:
            # returned_solution = []
            end_time = time.time() + self.simulationTime
            while True:
                solution = []
                child = self.tree_policy(solution)
                if child.gameState.is_goal():
                    return solution, len(self.exploredNodes)
                if self.isUniqueNode and child.gameState.encode() not in self.hashTable:
                    self.hashTable.add(child.gameState.encode())
                if child.gameState.encode() not in self.exploredNodes:
                    self.exploredNodes.add(child.gameState.encode())
                result, extended_solution_list = child.simulate(child.parent.gameState, self.exploredNodes,
                                                                max_simulation_depth=self.maxSimulationDepth,
                                                                max_previous_nodes=self.maxPreviousNodes,
                                                                points_list=self.pointsList)
                if len(extended_solution_list) > 0:
                    solution.extend(extended_solution_list)
                    return solution, len(self.exploredNodes)
                child.backpropagate(result)
                returned_solution = solution
                if time.time() > end_time:
                    break
            return returned_solution, len(self.exploredNodes)
        else:
            raise ValueError("No simulation param is provided")

    def tree_policy(self, solution: list):
        current_node = self.root
        solution.append(current_node.gameState)
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                next_node = current_node.expand(self.hashTable)
                if next_node is not None:
                    solution.append(next_node.gameState)
                    return next_node
            else:
                next_node = current_node.get_best_child(c=self.c)
                if next_node is not None:
                    solution.append(next_node.gameState)
                    current_node = next_node
                else:
                    break
        return current_node

    def __del__(self):
        del self.hashTable
