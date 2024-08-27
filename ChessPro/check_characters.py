blue_pieces = ['hero1', 'hero2', 'hero3', 'pawn', 'pawn']
blue_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
blue_moved = [False, False, False, False, False]
red_pieces = ['hero1', 'hero2', 'hero3', 'pawn', 'pawn']
red_locations = [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]
red_moved = [False, False, False, False, False]


def check_hero2(position, color):
    moves_list = []
    if color == 'blue':
        enemies_list = red_locations
        friends_list = blue_locations
    else:
        friends_list = red_locations
        enemies_list = blue_locations
    
    targets = [(2, 2), (2, -2), (-2, 2), (-2, -2)]
    
    for target in targets:
        move = (position[0] + target[0], position[1] + target[1])
        if 0 <= move[0] <= 4 and 0 <= move[1] <= 4:  
            if move not in friends_list: 
                moves_list.append(move)
    
    return moves_list


def check_hero1(position, color):
    moves_list = []
    if color == 'blue':
        enemies_list = red_locations
        friends_list = blue_locations
    else:
        friends_list = red_locations
        enemies_list = blue_locations
    
    targets = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    
    for target in targets:
        move = (position[0] + target[0], position[1] + target[1])
        if 0 <= move[0] <=4 and 0 <= move[1] <=4: 
            if move not in friends_list:  
                moves_list.append(move)
    
    return moves_list


def check_pawn(position, color):
    moves_list = []
    if color == 'blue':
        enemies_list = red_locations
        friends_list = blue_locations
    else:
        friends_list = red_locations
        enemies_list = blue_locations
    
    targets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    for target in targets:
        move = (position[0] + target[0], position[1] + target[1])
        if 0 <= move[0] <= 4 and 0 <= move[1] <= 4: 
            if move not in friends_list: 
                moves_list.append(move)
    
    return moves_list


def check_hero3(position, color):
    moves_list = []
    if color == 'blue':
        enemies_list = red_locations
        friends_list = blue_locations
    else:
        friends_list = red_locations
        enemies_list = blue_locations
    
    patterns = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (-1, 2), (1, -2), (-1, -2)
    ]
    
    for pattern in patterns:
        move = (position[0] + pattern[0], position[1] + pattern[1])
        if 0 <= move[0] <= 4 and 0 <= move[1] <= 4:  
            if move not in friends_list: 
                moves_list.append(move)
    
    return moves_list


def check_options(pieces, locations, turn):
    all_moves_list = []
    capture_moves = set()
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'hero1':
            moves_list = check_hero1(location, turn)
        elif piece == 'hero2':
            moves_list = check_hero2(location, turn)
        elif piece == 'hero3':
            moves_list = check_hero3(location, turn)
        

        all_moves_list.append(moves_list)
        
        if turn == 'blue':
            capture_moves.update(move for move in moves_list if move in red_locations)
        else:
            capture_moves.update(move for move in moves_list if move in blue_locations)

    return all_moves_list, capture_moves
