import pygame
pygame.init()

colors = {
    'board_light': 'black',
    'board_dark': 'black',
    'button_background': 'black',
    'button_border': 'white',
    'hint_color': 'black',
    'game_over': 'red',
    'status_text': 'black',
    'move_blue': 'blue',
    'move_red': 'red',
}
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Two-Player Pygame Chess!')
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()
fps = 60
FPS = 30


blue_pieces = ['hero1', 'hero2', 'hero3', 'pawn', 'pawn']
blue_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
blue_moved = [False, False, False, False, False]
red_pieces = ['hero1', 'hero2', 'hero3', 'pawn', 'pawn']
red_locations = [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]
red_moved = [False, False, False, False, False]
captured_pieces_white = []
captured_pieces_black = []

button_width = 240
button_height = 200
button_radius = 40
button_spacing = 20
medium_font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)
button_font = pygame.font.Font(None, 24)


turn_step = 0
selection = 100
valid_moves = []
move_history=[]
counter = 0
winner = ''
game_over = False
in_main_menu = True
game_active = False
global game_state


