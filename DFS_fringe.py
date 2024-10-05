class Fringe_DFS:
    def __init__(self):
        self.stack = []

    def add(self, state):
        self.stack.append(state)

    def remove(self):
        return self.stack.pop() if self.stack else None

    def is_empty(self):
        return len(self.stack) == 0

    def print_elements(self):
        if self.is_empty():
            print("Fringe is empty")
        else:
            print("Elements in DFS Fringe")
            for state in self.stack:
                print(state)

