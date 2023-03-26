from state import State, Action, ROW, COL
from queue import PriorityQueue, Queue, LifoQueue


class Node:
    def __init__(self, state: State, dept=0, parent=None):
        self.state = state
        self.parent = parent
        self.dept = dept
        self.score = 0

    @property
    def children(self):
        if self.state.is_end():
            return []
        for action in Action:
            child = self.state.copy()
            if child.perform(action):
                yield Node(child, dept=self.dept+1, parent=self)

    def __lt__(self, other: None):
        return self.score < other.score


class StandardSearch:
    def __init__(self, state: State):
        self.root = Node(state)

    def tracking(self, goal: Node):
        current = goal.parent
        path = [goal.state]
        while current:
            path.append(current.state)
            current = current.parent

        path.reverse()
        return path

    def solve(self):
        return [], 0


class DFS(StandardSearch):
    def solve(self):
        st = LifoQueue()
        st.put(self.root)
        explored = 1
        while not st.empty():
            current = st.get()
            if current.state.is_goal():
                return self.tracking(current), explored
            for child in current.children:
                st.put(child)
                explored += 1

        raise RuntimeError("Can not reach goal state.")


class BFS(StandardSearch):
    def solve(self):
        q = Queue()
        q.put(self.root)
        explored = 1
        while not q.empty():
            current = q.get()
            if current.state.is_goal():
                return self.tracking(current), explored
            for child in current.children:
                q.put(child)
                explored += 1

        raise RuntimeError("Can not reach goal state.")


class DFGS(StandardSearch):
    def solve(self):
        st = LifoQueue()
        st.put(self.root)
        explored = {self.root.state.encode()}
        while not st.empty():
            current = st.get()
            if current.state.is_goal():
                return self.tracking(current), len(explored)
            for child in current.children:
                encoded_child = child.state.encode()
                if encoded_child not in explored:
                    st.put(child)
                    explored.add(encoded_child)

        raise RuntimeError("Can not reach goal state.")


class BFGS(StandardSearch):
    def solve(self):
        q = Queue()
        q.put(self.root)
        explored = {self.root.state.encode()}
        while not q.empty():
            current = q.get()
            if current.state.is_goal():
                return self.tracking(current), len(explored)
            for child in current.children:
                encoded_child = child.state.encode()
                if encoded_child not in explored:
                    q.put(child)
                    explored.add(encoded_child)

        raise RuntimeError("Can not reach goal state.")


class BestFS(StandardSearch):
    def __init__(self, state: State, distance='manhattan', strategy='a-star'):
        super().__init__(state)

        if distance == 'manhattan':
            def manhattan_distance(current: tuple[int, int], goal: tuple[int, int]):
                return abs(current[ROW] - goal[ROW]) + abs(current[COL] - goal[COL])

            self._distance = manhattan_distance
        elif distance == 'euclidean':
            def euclidean_distance(current: tuple[int, int], goal: tuple[int, int]):
                return ((current[ROW] - goal[ROW])**2 + (current[COL] - goal[COL])**2)**0.5

            self._distance = euclidean_distance
        elif distance == 'chebyshev':
            def chebyshev_distance(current: tuple[int, int], goal: tuple[int, int]):
                return max(current[ROW] - goal[ROW], current[COL] - goal[COL])

            self._distance = chebyshev_distance
        elif callable(distance):
            self._distance = distance
        else:
            raise ValueError(distance)

        if strategy == 'a-star':
            self.f = lambda node: node.dept + self.heuristic(node)
        elif strategy == 'greedy':
            self.f = self.heuristic
        else:
            raise ValueError(strategy)

        self.root.score = self.f(self.root)

    def heuristic(self, node: Node):
        current = node.state.box.get_first_half()
        goal = node.state.board.hole
        return self._distance(current, goal)

    def solve(self):
        p = PriorityQueue()
        p.put(self.root)
        explored = {self.root.state.encode()}
        while not p.empty():
            current = p.get()
            if current.state.is_goal():
                return self.tracking(current), len(explored)
            for child in current.children:
                encoded_child = child.state.encode()
                if encoded_child not in explored:
                    explored.add(encoded_child)
                    child.score = self.f(child)
                    p.put(child)

        raise RuntimeError("Can not reach goal state.")
