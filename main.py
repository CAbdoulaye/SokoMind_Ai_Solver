import sys


# Scan the map from text file and return a 2d array
def read_map(file_path):
    with open(file_path, 'r') as file:
        sokoban_map = []
        for line in file:
            row = list(line.strip())  # Convert each line to a list of characters
            sokoban_map.append(row)
    return sokoban_map


# Scan 2d array map and return obstacles x y coordinates
def get_obstacles(map):
    obstacles = []
    x = y = 0
    for row in map:
        x = 0
        for element in row:
            if element == 'O':
                obstacles.append((x, y))
            x = x + 1
        y = y - 1
    return obstacles


# Scan 2d array map and return boxes x y coordinates
def get_boxes(map):
    boxes_count = {}
    boxes = {}
    x = y = 0
    for row in map:
        x = 0
        for element in row:
            # If element = 0 (not an obstacle) or R (not a robot) or S (storage for box X) and is uppercase (is a
            # box). lowercase is for other storages
            if element.isupper() and (element != 'O' and element != 'R' and element != 'S'):
                if element in boxes_count:
                    boxes_count[element] = boxes_count[element] + 1
                    temp = boxes_count[element]
                    boxes[(element + str(temp))] = [x, y]
                else:
                    boxes_count[element] = 1
                    boxes[(element + str(1))] = [x, y]
            x = x + 1
        y = y - 1
    return boxes


# Scan 2d array map and return storage x y coordinates
def get_storage(map):
    storage = {}
    storage_count = {}
    x = y = 0
    for row in map:
        x = 0
        for element in row:
            # S and lowercase letters represent storage units
            if element == 'S' or element.islower():
                if element in storage_count:
                    storage_count[element] = storage_count[element] + 1
                    temp = storage_count[element]
                    storage[(element + str(temp))] = [x, y]
                else:
                    storage_count[element] = 1
                    storage[(element + str(1))] = [x, y]
            x = x + 1
        y = y - 1
    return storage


# Scan 2d array map and return player/robot x y coordinates
def get_player(map):
    x = y = 0
    for row in map:
        x = 0
        for element in row:
            if element == 'R':
                # boxes.append((("X" + str(len(boxes) + 1)), (x,y)))
                return [x, y]
            x = x + 1
        y = y - 1
    return False


def check_for_errors(player, boxes, storage):
    if player == False:
        print("Error: Player is missing from map")
        sys.exit(1)
    if len(boxes) > len(storage):
        print("Error: Their are more boxes than storage units on map")
        sys.exit(1)
    # must also check and make sure the sokomind is closed, if they is a gap our player may move to infinity. map must BE retricted

    print("Map Looks Good")


# check for possible legal states
# will change player coordinates and see if it is overlapping with anything
# example p (1, -1) will become p (1, 0) -> up then p (1, -2) -> down then p (0, -1) -> left, ...
# will return a list with the possible placements of player
def possible_movement(player, boxes):
    print("Initial Coordinates")
    print(player)
    # Move Left
    move_left = check_for_obstacle_overlap((player[0] - 1, player[1]))
    # Move Up
    move_up = check_for_obstacle_overlap((player[0], player[1] + 1))
    # Move right
    move_right = check_for_obstacle_overlap((player[0] + 1, player[1]))
    # Move down
    move_down = check_for_obstacle_overlap((player[0], player[1] - 1))

    # Dictionary with possible moves and the coordinates
    player_move = {
        "left": { "coordinate": (player[0] - 1, player[1]), "legal": move_left},
        "up": {"coordinate": (player[0], player[1] + 1), "legal": move_up},
        "right": {"coordinate": (player[0] + 1, player[1]), "legal": move_right},
        "down": {"coordinate": (player[0], player[1] - 1), "legal": move_down}
    }

    # check if a box was moved
    # only try when player_move is true meaning the move is legal in the first place
    box_move = {
        "left": False,
        "up": False,
        "down": False,
        "right":False
    }
    for key, value in player_move.items():
        # if move is legal
        if value["legal"]:
            box_move[key] = check_if_box_moved(value, boxes)

    # Check if the moved box is in a legal state
    # illegal state is where an obstacle or another box is
    box_coordinate = {
        "left": {"coordinate": (player[0] - 2, player[1]), "legal": move_left},
        "up": {"coordinate": (player[0], player[1] + 2), "legal": move_up},
        "right": {"coordinate": (player[0] + 2, player[1]), "legal": move_right},
        "down": {"coordinate": (player[0], player[1] - 2), "legal": move_down}
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
            box_overlap[key] = check_for_box_overlap(value, boxes)
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

    print("legal moves:")
    print(player_move)

    return player_move


# After every movement, this function checks if the player's position is overlapping with an obstacle
# Returns True if position is legal and False if illegal
def check_for_obstacle_overlap(player):
    for element in obstacles:
        # element[0] == player[0] means if the x coordinates are the same
        if element[0] == player[0] and element[1] == player[1]:
            return False
    return True


def check_if_box_moved(movement, boxes):
    player_position = movement["coordinate"]
    for element in boxes.values():
        if element[0] == player_position[0] and element[1] == player_position[1]:
            return True
    return False


def check_for_box_overlap(box, boxes):

    # check if it's overlapping with another box
    return check_if_box_moved(box, boxes)


sokomind_map = read_map("sokomind_maps/sokomind_map1_test.txt")
obstacles = get_obstacles(sokomind_map)
boxes = get_boxes(sokomind_map)
player = get_player(sokomind_map)
storage = get_storage(sokomind_map)
check_for_errors(player, boxes, storage)
legal_moves = possible_movement(player, boxes)


# develop a class that represents a state.

# print("Player position: " , player)
# print("Boxes position: " , boxes)
# print("storage position: " , storage)
# print("obstacles position: " , obstacles)

