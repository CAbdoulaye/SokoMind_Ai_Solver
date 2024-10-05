import sys
import copy
from state import State
from BFS_fringe import Fringe_BFS
from DFS_fringe import Fringe_DFS
from Close_list import Close_List


# Scan the map from text file and return a 2d array
def read_map(file_path):
    with open(file_path, 'r') as file:
        sokoban_map = []
        for line in file:
            row = list(line.strip())  # Convert each line to a list of characters
            sokoban_map.append(row)
    return sokoban_map


# Scan 2d array map and return obstacles x y coordinates
def get_obstacles(my_map):
    my_obstacles = []
    x = y = 0
    for row in my_map:
        x = 0
        for element in row:
            if element == 'O':
                my_obstacles.append((x, y))
            x = x + 1
        y = y - 1
    return my_obstacles


# Scan 2d array map and return boxes x y coordinates
def get_boxes(my_map):
    boxes_count = {}
    my_boxes = {}
    my_boxes_sorted = {}
    x = y = 0
    for row in my_map:
        x = 0
        for element in row:
            # If element = 0 (not an obstacle) or R (not a robot) or S (storage for box X) and is uppercase (is a
            # box). lowercase is for other storages
            if element.isupper() and (element != 'O' and element != 'R' and element != 'S'):
                if element in boxes_count:
                    boxes_count[element] = boxes_count[element] + 1
                    temp = boxes_count[element]
                    my_boxes[(element + str(temp))] = [x, y]
                    my_boxes_sorted[element][(element + str(temp))] = [x, y]
                else:
                    boxes_count[element] = 1
                    my_boxes[(element + str(1))] = [x, y]
                    my_boxes_sorted[element] = {}
                    my_boxes_sorted[element][(element + str(1))] = [x, y]
            x = x + 1
        y = y - 1
    return {"my_boxes": my_boxes, "my_boxes_sorted": my_boxes_sorted}


# Scan 2d array map and return storage x y coordinates
def get_storage(my_map):
    my_storage = {}
    storage_count = {}
    my_storage_sorted = {}

    x = y = 0
    for row in my_map:
        x = 0
        for element in row:
            # S and lowercase letters represent storage units
            if element == 'S' or element.islower():
                if element not in storage_count:
                    my_storage_sorted[element] = {}
                    storage_count[element] = 1
                    my_storage[(element + str(1))] = [x, y]
                    my_storage_sorted[element][(element + str(1))] = [x, y]
                else:
                    storage_count[element] = storage_count[element] + 1
                    temp = storage_count[element]
                    my_storage[(element + str(temp))] = [x, y]
                    my_storage_sorted[element][(element + str(temp))] = [x, y]

            x = x + 1
        y = y - 1
    return {"my_storage": my_storage, "my_storage_sorted": my_storage_sorted}


# Scan 2d array map and return player/robot x y coordinates
def get_player(my_map):
    x = y = 0
    for row in my_map:
        x = 0
        for element in row:
            if element == 'R':
                # boxes.append((("X" + str(len(boxes) + 1)), (x,y)))
                return [x, y]
            x = x + 1
        y = y - 1
    return False


def check_for_errors(my_player, my_boxes, my_storage):
    if my_player == False:
        print("Error: Player is missing from map")
        sys.exit(1)
    if len(my_boxes) > len(my_storage):
        print("Error: Their are more boxes than storage units on map")
        sys.exit(1)
    # must also check and make sure the sokomind is closed, if they is a gap our player may move to infinity.
    # map must BE restricted

    print("Map Looks Good")


# check for possible legal states
# will change player coordinates and see if it is overlapping with anything
# example p (1, -1) will become p (1, 0) -> up then p (1, -2) -> down then p (0, -1) -> left, ...
# will return a list with the possible placements of player
def possible_movement(my_player, my_boxes):
    # Move Left
    move_left = check_for_obstacle_overlap((my_player[0] - 1, my_player[1]))
    # Move Up
    move_up = check_for_obstacle_overlap((my_player[0], my_player[1] + 1))
    # Move right
    move_right = check_for_obstacle_overlap((my_player[0] + 1, my_player[1]))
    # Move down
    move_down = check_for_obstacle_overlap((my_player[0], my_player[1] - 1))

    # Dictionary with possible moves and the coordinates
    player_move = {
        "left": {"coordinate": (my_player[0] - 1, my_player[1]), "legal": move_left},
        "up": {"coordinate": (my_player[0], my_player[1] + 1), "legal": move_up},
        "right": {"coordinate": (my_player[0] + 1, my_player[1]), "legal": move_right},
        "down": {"coordinate": (my_player[0], my_player[1] - 1), "legal": move_down}
    }

    # check if a box was moved
    # only try when player_move is true meaning the move is legal in the first place
    box_move = {
        "left": False,
        "up": False,
        "down": False,
        "right": False
    }
    for key, value in player_move.items():
        # if move is legal
        if value["legal"]:
            box_move[key] = check_if_box_moved(value, my_boxes)

    # Check if the moved box is in a legal state
    # illegal state is where an obstacle or another box is
    box_coordinate = {
        "left": {"coordinate": (my_player[0] - 2, my_player[1]), "legal": move_left},
        "up": {"coordinate": (my_player[0], my_player[1] + 2), "legal": move_up},
        "right": {"coordinate": (my_player[0] + 2, my_player[1]), "legal": move_right},
        "down": {"coordinate": (my_player[0], my_player[1] - 2), "legal": move_down}
    }
    # Box is overlapped with another box after move
    box_overlap = {
        "left": False,
        "up": False,
        "down": False,
        "right": False
    }
    # Box is overlapped with an obstacle after move
    box_obstacle_overlap = {
        "left": False,
        "up": False,
        "down": False,
        "right": False
    }

    # check if box is overlapped
    for key, value in box_coordinate.items():
        # If box moved after player movement
        if box_move[key]:
            # check if box is overlapped with another box
            box_overlap[key] = check_for_box_overlap(value, my_boxes)
            # check if box is overlapped with obstacles
            box_obstacle_overlap[key] = not check_for_obstacle_overlap(box_coordinate[key]["coordinate"])
        # Else if player moved but box did not: there is no overlap
        elif value["legal"] and not box_move[key]:
            box_overlap[key] = False

    for key, value in player_move.items():
        # If the player move is legal but the box moved is illegal: move becomes illegal
        if value["legal"] and (box_overlap[key] or box_obstacle_overlap[key]):
            player_move[key]["legal"] = False

    keys_to_delete = []
    for key, value in player_move.items():
        if not value["legal"]:
            keys_to_delete.append(key)

    for key in keys_to_delete:
        del player_move[key]

    # Only the legal moves are returned. So we can get rid of the legal element in the dict
    for move in player_move:
        del player_move[move]["legal"]

    return player_move


# After every movement, this function checks if the player's position is overlapping with an obstacle
# Returns True if position is legal and False if illegal
def check_for_obstacle_overlap(my_player):
    for element in obstacles:
        # element[0] == player[0] means if the x coordinates are the same
        if element[0] == my_player[0] and element[1] == my_player[1]:
            return False
    return True


def check_if_box_moved(movement, my_boxes):
    player_position = movement["coordinate"]
    for element in my_boxes.values():
        if element[0] == player_position[0] and element[1] == player_position[1]:
            return True
    return False


def check_for_box_overlap(box, my_boxes):

    # check if it's overlapping with another box
    return check_if_box_moved(box, my_boxes)


# Initial State
def init_state(my_player, my_boxes):
    s1 = State(my_player, my_boxes, None, None)
    return s1


def new_state(my_player, my_boxes, move, state):
    # new state
    nw_state = State(my_player, my_boxes, move, state)
    return nw_state


# Final state. all boxes must be in their respective storage units
def is_final_state(my_boxes, my_storage):
    # print("boxes")
    # print(my_boxes)
    # for box in my_boxes:
    #     print(box)
    # print("storage")
    # for storage in my_storage:
    #     print(storage)
    #     print(my_storage[storage])

    for key, value in my_boxes.items():
        # print(key)
        # print(value)
        if key[0] == 'X':
            # print("Storage S")
            # print(my_storage["S"])
            if value not in my_storage["S"].values():
                return False
        else:
            # print("Storage ", key[0].lower())
            # print(my_storage[key[0].lower()])
            if value not in my_storage[key[0].lower()].values():
                return False
        return True


def successor(player_move, my_boxes, move_coordinates, old_move, old_state):
    # legal state was already explored. This function makes the move and creates a new state
    # move coordinates tells the new move values. for left move coordinates = (-1, 0)
    # move coordinates will be added to the box if player is overlapping with box
    # legal moves already checked if the move is legal. so if new position = a box position then
    # box position must be changed and is legal
    state_boxes = copy.deepcopy(my_boxes)
    player_position = player_move["coordinate"]
    for element in state_boxes.values():
        if element[0] == player_position[0] and element[1] == player_position[1]:
            element[0] = element[0] + move_coordinates[0]
            element[1] = element[1] + move_coordinates[1]
            break
    nw_state = new_state(player_position, state_boxes, old_move, old_state)

    return nw_state


# Getting required data to run code eg. player position, ...
sokomind_map = read_map("sokomind_maps/sokomind_map5_test.txt")
obstacles = get_obstacles(sokomind_map)

all_boxes = get_boxes(sokomind_map)
boxes = all_boxes["my_boxes"]
sorted_boxes = all_boxes["my_boxes_sorted"]

all_storage = get_storage(sokomind_map)
storage = all_storage["my_storage"]
sorted_storage = all_storage["my_storage_sorted"]

player = get_player(sokomind_map)

current_state = init_state(player, boxes)

moves = {
        "left": (-1, 0),
        "up": (0, 1),
        "right": (1, 0),
        "down": (0, -1)
    }

# for key, value in legal_moves.items():
#     print(key)
#     current_state = successor(legal_moves[key], boxes, moves[key], key, current_state)

my_fringe = Fringe_DFS()
my_fringe.add(current_state)
my_closed_list = Close_List()

count = 100000
temp = 100000

found_solution = False

while not my_fringe.is_empty() and count != 0:
    # remove head of fringe
    current_state = my_fringe.remove()
    print("Popped State")
    print(current_state)
    if not my_closed_list.is_in_closed_list(current_state):
        my_closed_list.add(current_state)
        current_state_move = current_state.get_previous_move()
        # get player and boxes coordinates
        player = current_state.get_player()
        boxes = current_state.get_boxes()
        if is_final_state(boxes, sorted_storage):
            print("Puzzle Solved")
            print(current_state)
            found_solution = True
            break

        # get legal moves
        legal_moves = possible_movement(player, boxes)
        for key, value in legal_moves.items():
            if current_state_move is not None:
                my_old_move = current_state_move + " -> " + key
            else:
                my_old_move = key

            state_to_add = successor(legal_moves[key], boxes, moves[key], my_old_move, current_state)
            # if not my_closed_list.is_in_closed_list(state_to_add):
            my_fringe.add(state_to_add)
        count = count - 1

    else:
        print("is in closed list")
my_fringe.print_elements()

if found_solution:
    print("Num of Tries")
    print(temp - count)
    print("Steps")
    print(current_state.get_previous_move())

#

# final_state(sorted_boxes, storage)
# player = get_player(sokomind_map)
# check_for_errors(player, boxes, storage)
# legal_moves = possible_movement(player, boxes)
# init_state(player, boxes)


