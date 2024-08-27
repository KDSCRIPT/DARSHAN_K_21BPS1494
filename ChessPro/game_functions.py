import pygame
import time
from constants import *
from check_characters import *
from sys import exit
pygame.init()

# Initialize game state
start_time = time.time()

def get_elapsed_time():
    elapsed_seconds = int(time.time() - start_time)
    minutes, seconds = divmod(elapsed_seconds, 60)
    return f"{minutes:02}:{seconds:02}"

def translate_move_to_direction(piece, start, end, turn):
    direction = ""
    if piece == "pawn" or piece == "hero1":
        if start[0] == end[0]:  # Same column
            if start[1] > end[1]:
                direction = "B" if turn == 'blue' else "F"
            else:
                direction = "F" if turn == 'blue' else "B"
        elif start[1] == end[1]:  # Same row
            if start[0] > end[0]:
                direction = "R" if turn == 'blue' else "L"
            else:
                direction = "L" if turn == 'blue' else "R"
    elif piece == "hero2":
        if start[0] > end[0] and start[1] > end[1]:
            direction = "BR" if turn == 'blue' else "FL"
        elif start[0] < end[0] and start[1] > end[1]:
            direction = "BL" if turn == 'blue' else "FR"
        elif start[0] > end[0] and start[1] < end[1]:
            direction = "FR" if turn == 'blue' else "BL"
        elif start[0] < end[0] and start[1] < end[1]:
            direction = "FL" if turn == 'blue' else "BR"
    elif piece == "hero3":
            dx = end[0] - start[0]
            dy = end[1] - start[1]

            if dx == 2 and dy == 1:
                direction = "RF" if turn == 'blue' else "LF"
            elif dx == 2 and dy == -1:
                direction = "RB" if turn == 'blue' else "LB"
            elif dx == -2 and dy == 1:
                direction = "LF" if turn == 'blue' else "RF"
            elif dx == -2 and dy == -1:
                direction = "LB" if turn == 'blue' else "RB"
            elif dx == 1 and dy == 2:
                direction = "FR" if turn == 'blue' else "BR"
            elif dx == -1 and dy == 2:
                direction = "FL" if turn == 'blue' else "BL"
            elif dx == 1 and dy == -2:
                direction = "BR" if turn == 'blue' else "FR"
            elif dx == -1 and dy == -2:
                direction = "BL" if turn == 'blue' else "FL"

    return direction

def update_move_history(color, piece, direction):
    timestamp = get_elapsed_time()
    move_history.append(f"{timestamp} {color} {piece}: {direction}")
    # Keep only the last 5 moves
    move_history[:] = move_history[-5:]

def check_valid_moves():
    if turn_step == 0:
        options_list = blue_options
    else:
        options_list = red_options
    valid_options = options_list[selection]
    return valid_options

def draw_board():
    for i in range(25):
        column = i % 5
        row = i // 5
        color = colors['board_light'] if (row + column) % 2 == 0 else colors['board_dark']
        pygame.draw.rect(screen, color, [column * 100, row * 100, 100, 100])
    for i in range(6):
        pygame.draw.line(screen, 'white', (0, 100 * i), (500, 100 * i), 2)
        pygame.draw.line(screen, 'white', (100 * i, 0), (100 * i, 500), 2)

    time_text = get_elapsed_time()
    time_surface = medium_font.render(f"Time: {time_text}", True, 'white')
    screen.blit(time_surface, (10, 10)) 

def draw_pieces():
    piece_font = pygame.font.Font(None, 30)
    
    for i in range(len(blue_pieces)):
        piece_symbol = f'A-{blue_pieces[i]}'
        piece_text = piece_font.render(piece_symbol, True,'blue')
        screen.blit(piece_text, (blue_locations[i][0] * 100 + 10, blue_locations[i][1] * 100 + 40))
        if turn_step == 0 and selection == i:
            pygame.draw.rect(screen, 'blue', [blue_locations[i][0] * 100 + 1, blue_locations[i][1] * 100 + 1, 100, 100], 2)

    for i in range(len(red_pieces)):
        piece_symbol = f'B-{red_pieces[i]}'
        piece_text = piece_font.render(piece_symbol, True, 'red')
        screen.blit(piece_text, (red_locations[i][0] * 100 + 10, red_locations[i][1] * 100 + 40))
        if turn_step == 1 and selection == i:
            pygame.draw.rect(screen, 'red', [red_locations[i][0] * 100 + 1, red_locations[i][1] * 100 + 1, 100, 100], 2)

def check_options(pieces, locations, turn):
    moves_list = []
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
        elif piece=='hero3':
            moves_list=check_hero3(location,turn)

        all_moves_list.append(moves_list)
        
        if turn == 'blue':
            capture_moves.update(move for move in moves_list if move in red_locations)
        else:
            capture_moves.update(move for move in moves_list if move in blue_locations)

    return all_moves_list, capture_moves

def draw_move_buttons(moves, capture_moves, piece, start_location):
    button_radius = 20
    button_spacing = 10
    button_y = HEIGHT - 50
    buttons = []
    for i, move in enumerate(moves):
        button_x = 10 + i * (button_radius * 2 + button_spacing)
        button_color = colors['button_background'] if move not in capture_moves else 'red'
        pygame.draw.circle(screen, button_color, (button_x + button_radius, button_y + button_radius), button_radius)
        pygame.draw.circle(screen, colors['button_border'], (button_x + button_radius, button_y + button_radius), button_radius, 1)
        direction = translate_move_to_direction(piece, start_location, move, 'blue' if turn_step == 0 else 'red')
        text_surface = button_font.render(direction, True, 'white')
        text_rect = text_surface.get_rect(center=(button_x + button_radius, button_y + button_radius))
        screen.blit(text_surface, text_rect)
        buttons.append((pygame.Rect(button_x, button_y, button_radius * 2, button_radius * 2), move))
    return buttons

def draw_move_history():
    y_offset = 50 
    for move in move_history:
        screen.blit(medium_font.render(move, True, 'purple'), (520, y_offset))
        y_offset += 30  

def check_game_over():
    if not blue_pieces:
        return 'Red Wins!'
    if not red_pieces:
        return 'Blue Wins!'
    return None

def draw_main_menu():
    screen.fill('black')
    title_text = large_font.render("Hitwicket Game!", True, 'white')
    start_text = medium_font.render("Press Enter to Start", True, 'white')
    quit_text = medium_font.render("Press Q to Quit", True, 'white')
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - title_text.get_height()))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + start_text.get_height()))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + start_text.get_height() + 30))

def draw_game_over_screen(message):
    screen.fill('red')
    game_over_text = large_font.render(message, True, 'blue')
    home_text = medium_font.render("Press Enter to Return to Home", True, 'blue')
    quit_text = medium_font.render("Press Q to Quit", True, 'blue')
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height()))
    screen.blit(home_text, (WIDTH // 2 - home_text.get_width() // 2, HEIGHT // 2 + home_text.get_height()))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + home_text.get_height() + 30))


red_options, red_capture_moves = check_options(red_pieces, red_locations, 'red')
blue_options, blue_capture_moves = check_options(blue_pieces, blue_locations, 'blue')

while True:
    timer.tick(FPS)
    if in_main_menu:
        draw_main_menu()
    elif game_active:
        screen.fill('dark gray')
        draw_board()
        draw_pieces()

        if game_over:
            draw_game_over_screen(check_game_over())
        else:
            move_buttons=""
            status_text = "Blue's Turn" if turn_step == 0 else "Red's Turn"
            status_color = 'blue' if turn_step == 0 else 'red'
            screen.blit(medium_font.render(status_text, True, status_color), (520, 200))

            if selection != 100:
                valid_moves = check_valid_moves()
                if turn_step == 0:
                    hint_color = 'red' if any(move in red_locations for move in valid_moves) else 'black'
                    move_buttons = draw_move_buttons(valid_moves, blue_capture_moves, blue_pieces[selection], blue_locations[selection])
                else:
                    hint_color = 'red' if any(move in blue_locations for move in valid_moves) else 'black'
                    move_buttons = draw_move_buttons(valid_moves, red_capture_moves, red_pieces[selection], red_locations[selection])

            draw_move_history()  # Draw the move history on the screen

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
                    x_coord = event.pos[0] // 100
                    y_coord = event.pos[1] // 100

                    if x_coord < 5 and y_coord < 5:
                        if turn_step == 0:
                            if (x_coord, y_coord) in blue_locations:
                                selection = blue_locations.index((x_coord, y_coord))
                        else:
                            if (x_coord, y_coord) in red_locations:
                                selection = red_locations.index((x_coord, y_coord))

                    for button, move in move_buttons:
                        if button.collidepoint(event.pos):
                            if turn_step == 0:
                                direction = translate_move_to_direction(blue_pieces[selection], blue_locations[selection], move, 'blue')
                                update_move_history("Blue", blue_pieces[selection], direction)
                                blue_locations[selection] = move
                                if move in red_locations:
                                    index = red_locations.index(move)
                                    red_locations.pop(index)
                                    red_pieces.pop(index)
                                turn_step = 1
                                selection = 100
                            else:
                                direction = translate_move_to_direction(red_pieces[selection], red_locations[selection], move, 'red')
                                update_move_history("Red", red_pieces[selection], direction)
                                red_locations[selection] = move
                                if move in blue_locations:
                                    index = blue_locations.index(move)
                                    blue_locations.pop(index)
                                    blue_pieces.pop(index)
                                turn_step = 0
                                selection = 100

                            # Update move history and check for game over
                            red_options, red_capture_moves = check_options(red_pieces, red_locations, 'red')
                            blue_options, blue_capture_moves = check_options(blue_pieces, blue_locations, 'blue')
                            game_over = check_game_over()
                            break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if in_main_menu:
                    in_main_menu = False
                    game_active = True
                elif game_over:
                    in_main_menu = True
                    game_active = False
            elif event.key == pygame.K_q:
                pygame.quit()
                exit()

    pygame.display.flip()


