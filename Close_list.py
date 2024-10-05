class Close_List:
    def __init__(self):
        self.visited_states = []


    def add(self, state):
        self.visited_states.append(state)

    def player_is_overlapping(self, player_pos, closed_list_itm):
        if closed_list_itm.get_player()[0] == player_pos[0] and closed_list_itm.get_player()[1] == player_pos[1]:
            return True
        return False

    def box_is_overlapping(self, box_pos, closed_list_itm):
        for key, value in box_pos.items():
            # print("value")
            # print(value)
            # print("element.get_boxes()[key]")
            # print(element.get_boxes()[key])
            if value[0] != closed_list_itm.get_boxes()[key][0] or value[1] != closed_list_itm.get_boxes()[key][1]:
                return False
        return True

    def is_in_closed_list(self, state):
        if len(self.visited_states) == 0:
            return False
        # print("Comparing")
        # print("player ", state.get_player())
        # print("box ", state.get_boxes())
        for element in self.visited_states:
            if self.player_is_overlapping(state.get_player(), element) and self.box_is_overlapping(state.get_boxes(), element):
                return True
        return False