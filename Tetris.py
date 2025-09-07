import copy
import random
from copy import deepcopy

import pygame

"""
10 x 20 grid
play_height = 2 * play_width

tetriminos:
    0 - S - green
    1 - Z - red
    2 - I - cyan
    3 - O - yellow
    4 - J - blue
    5 - L - orange
    6 - T - purple
"""

pygame.font.init()

# global variables

col = 10  # 10 columns
row = 20  # 20 rows
s_width = 800  # window width
s_height = 750  # window height
play_width = 300  # play window width; 300/10 = 30 width per block
play_height = 300  # play window height; 300/10 = 30 height per block
block_size = 30  # size of block

up = (0, -1)
right = (1, 0)
left = (-1, 0)
down = (0, 1)

DIRECTION_NAMES = {
    (0, 1): "down",
    (0, -1): "up",
    (-1, 0): "left",
    (1, 0): "right"
    # Add diagonals if needed
}

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height - 300

filepath = './highscore.txt'
fontpath = './arcade.ttf'
fontpath_mario = './mario.ttf'

# shapes formats

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# index represents the shape
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# class to represent each of the pieces


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]  # choose color from the shape_color list
        self.rotation = 0  # chooses the rotation according to index


# initialise the grid
def create_grid(locked_pos={}):
    grid = [[(0, 0, 0) for x in range(col)] for y in range(row)]  # grid represented rgb tuples

    # locked_positions dictionary
    # (x,y):(r,g,b)
    for y in range(row):
        for x in range(col):
            if (x, y) in locked_pos:
                color = locked_pos[
                    (x, y)]  # get the value color (r,g,b) from the locked_positions dictionary using key (x,y)
                grid[y][x] = color  # set grid position to color

    return grid


def convert_shape_format(piece):
    positions = []
    shape_format = piece.shape[piece.rotation % len(piece.shape)]  # get the desired rotated shape from piece

    '''
    e.g.
       ['.....',
        '.....',
        '..00.',
        '.00..',
        '.....']
    '''
    for i, line in enumerate(shape_format):  # i gives index; line gives string
        row = list(line)  # makes a list of char from string
        for j, column in enumerate(row):  # j gives index of char; column gives char
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)  # offset according to the input given with dot and zero

    return positions


# checks if current position of piece in grid is valid
def valid_space(piece, grid):
    # makes a 2D list of all the possible (x,y)
    accepted_pos = [[(x, y) for x in range(col) if grid[y][x] == (0, 0, 0)] for y in range(row)]
    # removes sub lists and puts (x,y) in one list; easier to search
    accepted_pos = [x for item in accepted_pos for x in item]

    formatted_shape = convert_shape_format(piece)

    for pos in formatted_shape:
        if pos not in accepted_pos:
            if pos[1] >= 0:
                return False
    return True


# checks if piece is colliding with floor or another piece
def check_collision(piece, locked_pos):
    formatted = convert_shape_format(piece)
    for x, y in formatted:
        if y + 1 >= row or (x, y + 1) in locked_pos:
            return True
    return False


def out_the_sides(piece):
    piece_pos = convert_shape_format(piece)
    for x, y in piece_pos:
        if 0 > x or col <= x:
            return True
    return False


# check if piece is out of board
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape_rand():
    return Piece(5, 0, random.choice(shapes))

# chooses a shape randomly from shapes list
def get_shape(shape_index):
    shape_index = shape_index % len(shapes)
    shape = shapes[shape_index]
    return Piece(5, 0, shape)


# draws text in the middle
def draw_text_middle(text, size, color, surface):
    pygame.font.init()
    font = pygame.font.Font(fontpath, size)
    label = font.render(text, 1, color)

    surface.blit(label, (
        top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - (label.get_height() / 2)))


# draws the lines of the grid for the game
def draw_grid(surface):
    r = g = b = 0
    grid_color = (r, g, b)

    for i in range(row):
        # draw grey horizontal lines
        pygame.draw.line(surface, grid_color, (top_left_x, top_left_y + i * block_size),
                         (top_left_x + play_width, top_left_y + i * block_size))
        for j in range(col):
            # draw grey vertical lines
            pygame.draw.line(surface, grid_color, (top_left_x + j * block_size, top_left_y),
                             (top_left_x + j * block_size, top_left_y + play_height))


# clear a row when it is filled
def clear_rows(grid, locked):
    # need to check if row is clear then shift every other row above down one
    increment = 0
    for i in range(len(grid) - 1, -1, -1):  # start checking the grid backwards
        grid_row = grid[i]  # get the last row
        if (0, 0, 0) not in grid_row:  # if there are no empty spaces (i.e. black blocks)
            increment += 1
            # add positions to remove from locked
            index = i  # row index will be constant
            for j in range(len(grid_row)):
                try:
                    del locked[(j, i)]  # delete every locked element in the bottom row
                except ValueError:
                    continue

    # shift every row one step down
    # delete filled bottom row
    # add another empty row on the top
    # move down one step
    if increment > 0:
        # sort the locked list according to y value in (x,y) and then reverse
        # reversed because otherwise the ones on the top will overwrite the lower ones
        for key in sorted(list(locked), key=lambda a: a[1])[::-1]:
            x, y = key
            if y < index:  # if the y value is above the removed index
                new_key = (x, y + increment)  # shift position to down
                locked[new_key] = locked.pop(key)

    return increment


# draws the upcoming piece
def draw_next_shape(piece, surface):
    font = pygame.font.Font(fontpath, 30)
    label = font.render('Next shape', 1, (255, 255, 255))

    start_x = top_left_x + play_width + 50
    start_y = top_left_y + (play_height / 2 - 100)

    shape_format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, piece.color,
                                 (start_x + j * block_size, start_y + i * block_size, block_size, block_size), 0)

    surface.blit(label, (start_x, start_y - 30))

    # pygame.display.update()


# draws the content of the window
def draw_window(surface, grid, score=0, last_score=0):
    surface.fill((0, 0, 0))  # fill the surface with black

    pygame.font.init()  # initialise font
    font = pygame.font.Font(fontpath_mario, 65)
    label = font.render('TETRIS', 1, (255, 255, 255))  # initialise 'Tetris' text with white

    surface.blit(label, (
        (top_left_x + play_width / 2) - (label.get_width() / 2), 30))  # put surface on the center of the window

    # current score
    font = pygame.font.Font(fontpath, 30)
    label = font.render('SCORE   ' + str(score), 1, (255, 255, 255))

    start_x = top_left_x + play_width + 50
    start_y = top_left_y + (play_height / 2 - 100)

    surface.blit(label, (start_x, start_y + 200))

    # last score
    label_hi = font.render('HIGHSCORE   ' + str(last_score), 1, (255, 255, 255))

    start_x_hi = top_left_x - 240
    start_y_hi = top_left_y + 200

    surface.blit(label_hi, (start_x_hi + 20, start_y_hi + 200))

    # draw content of the grid
    for i in range(row):
        for j in range(col):
            # pygame.draw.rect()
            # draw a rectangle shape
            # rect(Surface, color, Rect, width=0) -> Rect
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    # draw vertical and horizontal grid lines
    draw_grid(surface)

    # draw rectangular border around play area
    border_color = (255, 255, 255)
    pygame.draw.rect(surface, border_color, (top_left_x, top_left_y, play_width, play_height), 4)

    # pygame.display.update()


# update the score txt file with high score
def update_score(new_score):
    score = get_max_score()

    with open(filepath, 'w') as file:
        if new_score > score:
            file.write(str(new_score))
        else:
            file.write(str(score))


# get the high score from the file
def get_max_score():
    with open(filepath, 'r') as file:
        lines = file.readlines()  # reads all the lines and puts in a list
        score = int(lines[0].strip())  # remove \n

    return score


class Move(object):
    def __init__(self, piece, rating, directions, grid_lockedpos):
        self.piece = piece
        self.rating = rating
        self.directions = directions
        self.grid_lockedpos = grid_lockedpos

    def __iter__(self):
        return iter((self.piece, self.rating, self.directions, self.grid_lockedpos))


def display_ghost_piece(moves):
    for move in moves:
        piece, score, directions, loc_pos = move
        display_ghost_piece_single(move, directions)


def display_ghost_piece_single(move, directions):
    grid = [['-' for _ in range(col)] for _ in range(row)]
    piece_pos = convert_shape_format(move.piece)

    for x, y in piece_pos:
        grid[y][x] = 'o'  # grid[row][col] → grid[y][x]

    for r in range(row):
        for c in range(col):
            print(grid[r][c], end=' ')
        print()
    print()
    print('row transitions: ', row_transitions(move), ' column transitions: ', column_transitions(move))

    readable = [DIRECTION_NAMES.get(d, str(d)) for d in directions]
    print(" ".join(readable))
    print("rating: ", move.rating, "orientation: ", move.piece.rotation)


def rate_dellacherie(move, grid):  # handtuned
    # rating = - piece.y + eroded_piece_cells(piece) - row_transitions(piece, grid, locked_pos) - column_transitions(piece, grid, locked_pos) - 4 * holes(
    # piece) - board_wells(piece)

    rating = random.randint(0, 100)
    return rating


def rate_weights(move, weights):  # weights = list of 6 weights
    rating = (weights[0] * (10-move.piece.y) +
              weights[1] * eroded_piece_cells(move.piece, move.grid_lockedpos) +
              weights[2] * row_transitions(move) +
              weights[3] * column_transitions(move) +
              weights[4] * holes(move.grid_lockedpos) +
              weights[5] * board_wells(move.grid_lockedpos))

    return rating


def check_cleared(locked_pos: dict):
    clear_lines = []
    coords = list(locked_pos.keys())
    for y in range(row):                     # use global row
        filled = sum(1 for pos in coords if pos[1] == y)
        if filled == col:                    # use global col
            clear_lines.append(y)
    return clear_lines



def eroded_piece_cells(piece, newlockedpos: dict):
    cleared_lines = check_cleared(newlockedpos)
    count = 0
    piece_pos = convert_shape_format(piece)
    for x, y in piece_pos:
        if y in cleared_lines:
            count += 1
    eroded_cells = len(cleared_lines) * count
    return eroded_cells



def row_transitions(move):
    transitions = 0
    new_grid = create_grid(move.grid_lockedpos)
    for y in range(row):
        prev_filled = True  # treat left border as filled
        for x in range(col):
            cur_filled = (new_grid[y][x] != (0, 0, 0))
            if cur_filled != prev_filled:
                transitions += 1
            prev_filled = cur_filled
        if not prev_filled:
            transitions += 1
    return transitions



def column_transitions(move):
    transitions = 0
    new_grid = create_grid(move.grid_lockedpos)
    for x in range(col):
        prev_filled = True  # top border treated as filled
        for y in range(row):
            cur_filled = (new_grid[y][x] != (0, 0, 0))
            if cur_filled != prev_filled:
                transitions += 1
            prev_filled = cur_filled
        if not prev_filled:
            transitions += 1
    return transitions



def colmaxheights(locked_pos: dict):  # returns dict of max heights of each col
    coords = list(locked_pos.keys())
    max_heights = {}
    for x in range(10):
        highest_pos = (x, 9)
        for pos in coords:
            if pos[0] == x and pos[1] < highest_pos[1]:  # col
                highest_pos = pos
        max_heights[highest_pos[0]] = highest_pos[1]
        # print(max_heights)
    return max_heights


def holes(locked_pos: dict):
    coords = list(locked_pos.keys())
    holes = 0
    for x in range(col):
        ys = [y for (xx, y) in coords if xx == x]
        if not ys:
            continue
        top_y = min(ys)
        height = row - top_y
        filled_count = len(ys)
        holes += max(0, height - filled_count)
    return holes



def col_heights(lockedpos, row=20):  # row = board height
    heights = []
    for x in range(10):
        ys = [y for (xx, y) in lockedpos if xx == x]
        if ys:
            top_y = min(ys)  # smallest y = topmost block
            heights.append(row - top_y)  # convert y to height
        else:
            heights.append(0)
    return heights


def board_wells(lockedpos, row=20):
    heights = col_heights(lockedpos, row)
    wells = 0
    for x in range(10):
        if x == 0:
            neighbor = heights[1]
            d = neighbor - heights[x]
        elif x == 9:
            neighbor = heights[8]
            d = neighbor - heights[x]
        else:
            neighbor = min(heights[x-1], heights[x+1])
            d = neighbor - heights[x]

        if d > 0:
            wells += d * (d + 1) // 2
    return wells


def possible_moves(grid, piece, locked_pos, weights):
    """
    Robust move generator:
      - For each rotation r
      - For each target column x in [0..col-1]
      - If the piece in that rotation at x is valid at spawn, simulate a drop
      - Create one Move for the landed position (with directions: horizontal moves + downs)
      - Deduplicate identical final grids
    Returns a list of unique Move objects.
    """
    moves = []
    spawn_x = piece.x  # usually 5 in your code
    cols = col         # uses your global `col`

    for rot in range(len(piece.shape)):
        # template piece for this rotation
        base = deepcopy(piece)
        base.rotation = rot % len(piece.shape)
        base.x = spawn_x
        base.y = 0

        for target_x in range(cols):
            ghost = deepcopy(base)
            ghost.x = target_x
            ghost.y = 0

            # skip impossible spawns (rotation + x causes immediate overlap/out-of-bounds)
            if not valid_space(ghost, grid):
                continue

            # simulate fall until collision (do NOT mutate external objects)
            placed = deepcopy(ghost)
            while True:
                # if placed would land here (next down would collide), record it
                if check_collision(placed, locked_pos):
                    # build directions from spawn to target_x then down to placed.y
                    dx = target_x - spawn_x
                    horiz = []
                    if dx > 0:
                        horiz = [(1, 0)] * dx   # right
                    elif dx < 0:
                        horiz = [(-1, 0)] * (-dx)  # left
                    downs = [(0, 1)] * placed.y     # drop down placed.y times (spawn y = 0)
                    move_dirs = horiz + downs

                    move_piece = deepcopy(placed)
                    move_grid = new_grid(locked_pos, move_piece)
                    new_move = Move(move_piece, 0, move_dirs, move_grid)
                    new_move.rating = rate_weights(new_move, weights)
                    moves.append(new_move)
                    break

                # move one step down and continue
                placed.y += 1
                # if it becomes invalid (shouldn't usually happen), abort this x
                if not valid_space(placed, grid):
                    break

    # Deduplicate by final locked positions (frozenset of occupied coordinates)
    unique_moves = []
    seen = set()
    for m in moves:
        key = frozenset(m.grid_lockedpos.keys())
        if key not in seen:
            seen.add(key)
            unique_moves.append(m)

    return unique_moves


def best_move(moves):  # returns best move
    best_move = max(moves, key=lambda move: move.rating)
    return best_move


def new_grid(locked_pos, piece):
    new_lockedpos = deepcopy(locked_pos)
    positions = convert_shape_format(piece)
    for pos in positions:
        p = (pos[0], pos[1])
        new_lockedpos[p] = piece.color
    return new_lockedpos


def drop(piece, directions, moves, locked_pos, grid, weights):
    ghost = deepcopy(piece)       # work on a local copy
    directions_down = []

    while True:
        if not valid_space(ghost, grid):  # if out of bounds or hitting walls
            break

        if check_collision(ghost, locked_pos):  # landed
            placed_piece = deepcopy(ghost)

            move_path = directions.copy() + directions_down.copy()
            new_move = Move(
                placed_piece,
                0,
                move_path,
                new_grid(locked_pos, placed_piece)
            )
            new_move.rating = rate_weights(new_move, weights)
            moves.append(new_move)
            return

        # keep falling
        ghost.y += 1
        directions_down.append(down)


def display_ghost_piece(moves):
    for move in moves:
        piece, score, directions, loc_pos = move
        display_ghost_piece_single(move)


def display_ghost_piece_single(move):
    grid = [['-' for _ in range(col)] for _ in range(row)]
    piece_pos = convert_shape_format(move.piece)

    for x, y in piece_pos:
        grid[y][x] = 'o'  # grid[row][col] -> grid[y][x]

    for r in range(row):
        for c in range(col):
            print(grid[r][c], end=' ')
        print()
    print()

    readable = [DIRECTION_NAMES.get(d, str(d)) for d in move.directions]
    print(" ".join(readable))
    print("rating: ", move.rating, "orientation: ", move.piece.rotation)


def get_ghost_position(piece, locked_pos, grid):
    ghost = Piece(piece.x, piece.y, piece.shape)
    ghost.rotation = piece.rotation

    while True:
        ghost.y += 1
        if check_collision(ghost, locked_pos):
            ghost.y -= 1
            break
    return convert_shape_format(ghost)


def execute_move(grid, move, piece):
    # move -> piece, rating, directions
    # display_ghost_piece_single(move)
    piece.rotation = move.piece.rotation
    for d in move.directions:
        piece.x += d[0]
        piece.y += d[1]
        if not valid_space(piece, grid):
            piece.x -= d[0]
            piece.y -= d[1]
            break


def main(window, weights):
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = get_shape_rand()
    possiblemoves = possible_moves(grid, current_piece, locked_positions, weights)
    next_piece = get_shape_rand()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.35
    level_time = 0
    score = 0
    last_score = get_max_score()

    ai_move_key = False

    while run:
        # need to constantly make new grid as locked positions always change
        grid = create_grid(locked_positions)

        # helps run the same on every computer
        # add time since last tick() to fall_time
        fall_time += clock.get_rawtime()  # returns in milliseconds
        level_time += clock.get_rawtime()

        clock.tick()  # updates clock

        if level_time / 1000 > 5:  # make the difficulty harder every 10 seconds
            level_time = 0
            if fall_speed > 0.15:  # until fall speed is 0.15
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                # since only checking for down - either reached bottom or hit another piece
                # need to lock the piece position
                # need to generate new piece
                change_piece = True

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    ai_move_key = True
                else:
                    ai_move_key = False

                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1  # move x position left
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1  # move x position right
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                elif event.key == pygame.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                elif event.key == pygame.K_SPACE:
                    # direct drop
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                elif event.key == pygame.K_UP:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

                # elif event.key == pygame.K_a:  ##AI MOVE
                #     # direct drop
                #     ai_move_key=True
                #     move = best_move(possiblemoves)
                #     execute_move(grid, move, current_piece)
                #     if not valid_space(current_piece, grid):
                #         current_piece.y -= 1

        if (ai_move_key == True):
            move = best_move(possiblemoves)
            execute_move(grid, move, current_piece)
            if not valid_space(current_piece, grid):
                current_piece.y -= 1

        piece_pos = convert_shape_format(current_piece)

        # draw the piece on the grid by giving color in the piece locations
        for i in range(len(piece_pos)):
            x, y = piece_pos[i]
            if y >= 0:
                grid[y][x] = current_piece.color

        if change_piece:  # if the piece is locked
            for pos in piece_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color  # add the key and value in the dictionary
            current_piece = next_piece
            next_piece = get_shape_rand()
            possiblemoves = possible_moves(grid, current_piece, locked_positions, weights)
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10  # increment score by 10 for every row cleared
            update_score(score)

            if last_score < score:
                last_score = score

        draw_window(window, grid, score, last_score)
        draw_next_shape(next_piece, window)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False


def main_menu(window, weights):
    run = True
    while run:
        draw_text_middle('Press any key to begin', 50, (255, 255, 255), window)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                score = main(window, weights)
                break
    pygame.quit()


if __name__ == '__main__':
    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption('Tetris')
    weights = [-20.337934738434768,0.025515123341488977,-8.97568007355699,-16.442502034587505,-8.216623851941582,-2.5364092317732645]
    main_menu(win, weights)  # start game


def main_menu_AI(window, weights, shape_pattern):
    run = True
    score = 0
    while run:
        pygame.display.update()
        score = main_AI(window, weights, run, shape_pattern)
        pygame.quit()
        break
    return score


def main_AI(window, weights, run_main, shape_pattern):
    locked_positions = {}
    shape_index = 0
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = get_shape(shape_pattern[shape_index])
    shape_index=shape_index+1
    possiblemoves = possible_moves(grid, current_piece, locked_positions, weights)
    next_piece = get_shape(shape_pattern[shape_index])
    shape_index=shape_index +1
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.35
    level_time = 0
    score = 0
    last_score = get_max_score()

    ai_move_key = True

    while run:
        # need to constantly make new grid as locked positions always change
        grid = create_grid(locked_positions)

        # helps run the same on every computer
        # add time since last tick() to fall_time
        fall_time += clock.get_rawtime()  # returns in milliseconds
        level_time += clock.get_rawtime()

        clock.tick()  # updates clock

        if level_time / 1000 > 5:  # make the difficulty harder every 10 seconds
            level_time = 0
            if fall_speed > 0.15:  # until fall speed is 0.15
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                # since only checking for down - either reached bottom or hit another piece
                # need to lock the piece position
                # need to generate new piece
                change_piece = True

        if (ai_move_key == True):
            move = best_move(possiblemoves)
            execute_move(grid, move, current_piece)
            if not valid_space(current_piece, grid):
                current_piece.y -= 1

        piece_pos = convert_shape_format(current_piece)

        # draw the piece on the grid by giving color in the piece locations
        for i in range(len(piece_pos)):
            x, y = piece_pos[i]
            if y >= 0:
                grid[y][x] = current_piece.color

        if change_piece:  # if the piece is locked
            for pos in piece_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color  # add the key and value in the dictionary
            current_piece = next_piece
            next_piece = get_shape(shape_pattern[shape_index])
            shape_index = (shape_index + 1) % len(shape_pattern)

            possiblemoves = possible_moves(grid, current_piece, locked_positions, weights)
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10  # increment score by 10 for every row cleared
            #update_score(score)

            if last_score < score:
                last_score = score

        draw_window(window, grid, score, last_score)
        draw_next_shape(next_piece, window)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False
            run_main = False
            pygame.display.quit()
    return score