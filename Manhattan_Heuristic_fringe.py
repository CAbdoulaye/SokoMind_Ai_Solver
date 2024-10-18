class Fringe_Manhattan:
    def __init__(self):
        self.stack = []

    def add(self, my_state):
        heuristic_value = my_state.get_manhattan_heuristic_value()  # Retrieve the heuristic from the state
        # Insert the state based on the heuristic value
        inserted = False
        for i in range(len(self.stack)):
            if heuristic_value > self.stack[i].get_manhattan_heuristic_value():  # Compare heuristic values
                self.stack.insert(i, my_state)
                inserted = True
                break
        if not inserted:
            self.stack.append(my_state)  # Add to the end if it's the largest

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

    def print_elements(self):
        if self.is_empty():
            print("Fringe is empty")
        else:
            print("Elements in Manhattan Fringe")
            for state in self.stack:
                print(state)
