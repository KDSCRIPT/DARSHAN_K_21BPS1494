import pygame
import socket
import threading
import json
import time
import sys
from game_functions import *  
from constants import *     
import random
pygame.init()


start_time = time.time()
game_state = {
    "turn_step": 0,
    "blue_pieces": ['hero1', 'hero2', 'hero3', 'pawn', 'pawn'],
    "blue_locations": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
    "red_pieces": ['hero1', 'hero2', 'hero3', 'pawn', 'pawn'],
    "red_locations": [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4)],
    "move_history": []
}

def get_elapsed_time():
    elapsed_seconds = int(time.time() - start_time)
    minutes, seconds = divmod(elapsed_seconds, 60)
    return f"{minutes:02}:{seconds:02}"

def receive_from_server(sock):
    global game_state
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            game_state = json.loads(data)
        except ConnectionResetError:
            break

def send_to_server(sock, data):
    sock.send(json.dumps(data).encode())

def connect_to_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('192.168.1.5', 65432))
    threading.Thread(target=receive_from_server, args=(sock,)).start()
    return sock


sock = connect_to_server()


def ai_move(pieces, locations, turn):
    valid_moves, capture_moves = check_options(pieces, locations, turn)
    
    if not valid_moves:
        return None
    
    piece_index = random.randint(0, len(pieces) - 1)
    piece = pieces[piece_index]
    piece_location = locations[piece_index]
    
    piece_valid_moves = valid_moves[piece_index]
    
    if not piece_valid_moves:
        return None
    
    move = random.choice(piece_valid_moves)
    
    return piece_index, move

# Main game loop
while True:
    timer.tick(FPS)
    if in_main_menu:
        draw_main_menu()
    elif game_active:
        screen.fill('dark gray')
        draw_board()
        draw_pieces()
        draw_move_history()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    # Handle return to home action
                    pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not game_over:
                    x_coord = event.pos[0] // 100
                    y_coord = event.pos[1] // 100

                    if x_coord < 5 and y_coord < 5:
                        if game_state["turn_step"] == 0:
                            if (x_coord, y_coord) in game_state["blue_locations"]:
                                selection = game_state["blue_locations"].index((x_coord, y_coord))
                        else:
                            if (x_coord, y_coord) in game_state["red_locations"]:
                                selection = game_state["red_locations"].index((x_coord, y_coord))

                    for button, move in move_buttons:
                        if button.collidepoint(event.pos):
                            if game_state["turn_step"] == 0:
                                direction = translate_move_to_direction(game_state["blue_pieces"][selection], game_state["blue_locations"][selection], move, 'blue')
                                update_move_history("Blue", game_state["blue_pieces"][selection], direction)
                                game_state["blue_locations"][selection] = move
                                if move in game_state["red_locations"]:
                                    red_index = game_state["red_locations"].index(move)
                                    game_state["red_pieces"].pop(red_index)
                                    game_state["red_locations"].pop(red_index)
                                game_state["turn_step"] = 1
                                selection = 100
                                
                                # Send move to server
                                move_command = {
                                    "action": "move",
                                    "piece": game_state["blue_pieces"][selection],
                                    "start": game_state["blue_locations"][selection],
                                    "end": move
                                }
                                send_to_server(sock, move_command)

                            else:
                                direction = translate_move_to_direction(game_state["red_pieces"][selection], game_state["red_locations"][selection], move, 'red')
                                update_move_history("Red", game_state["red_pieces"][selection], direction)
                                game_state["red_locations"][selection] = move
                                if move in game_state["blue_locations"]:
                                    blue_index = game_state["blue_locations"].index(move)
                                    game_state["blue_pieces"].pop(blue_index)
                                    game_state["blue_locations"].pop(blue_index)
                                game_state["turn_step"] = 0

                                # Send move to server
                                move_command = {
                                    "action": "move",
                                    "piece": game_state["red_pieces"][selection],
                                    "start": game_state["red_locations"][selection],
                                    "end": move
                                }
                                send_to_server(sock, move_command)

        pygame.display.flip()
