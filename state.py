class State:
    def __init__(self, player_coordinates, boxes_coordinates, previous_move, previous_state):
        self.player = player_coordinates
        self.boxes = boxes_coordinates
        self.prev_move = previous_move
        self.prev_state = previous_state

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

    def __str__(self):
        return f"State(player={self.player}, boxes={self.boxes}, prev_move={self.prev_move})"