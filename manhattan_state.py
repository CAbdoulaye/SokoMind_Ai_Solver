class Manhattan_State:
    def __init__(self, player_coordinates, boxes_coordinates, previous_move, previous_state):
        self.player = player_coordinates
        self.boxes = boxes_coordinates
        self.prev_move = previous_move
        self.prev_state = previous_state
        self.manhattan_distance = None

    # Return Player Coordinates
    def get_player(self):
        return self.player

    # Return Player Coordinates
    def get_boxes(self):
        return self.boxes

    # Return Previous state for backtracking
    def get_previous_state(self):
        return self.prev_state

    # Return Previous move and coordinates ex. left, right, ...
    def get_previous_move(self):
        return self.prev_move

    # Return the number of moves
    def get_num_of_moves(self):
        return self.prev_move.count("->") + 1

    def set_manhattan(self, manhattan_distance):
        self.manhattan_distance = manhattan_distance

    def get_manhattan_heuristic_value(self):
        return self.manhattan_distance

    def __str__(self):
        return f"State(player={self.player}, boxes={self.boxes}, manhatthan={self.manhattan_distance} ,prev_move={self.prev_move})"