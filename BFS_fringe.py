from collections import deque


class Fringe_BFS:
    def __init__(self):
        self.queue = deque()

    def add(self, state):
        self.queue.append(state)

    def remove(self):
        return self.queue.popleft() if self.queue else None

    def is_empty(self):
        return len(self.queue) == 0

    def print_elements(self):
        if self.is_empty():
            print("Fringe is empty")
        else:
            print("Elements in BFS Fringe")
            for state in self.queue:
                print(state)