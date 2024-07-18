import pygame as pg
import random
from constants import *
pg.font.init()
win = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
"""
Notes for James:
  Keep all coordinates as (y,x) and grid should be accessed as grid[y][x] or grid[row][col] or grid[j][i] don't mess this up 
  (*) are used to indicate filled blocks for your shape rotations states
  TOP_LEFT is the top left portion of the game grid and is stored as (x,y)
"""

def generate_grid(existing_blocks: dict = {}):
    """Generates and returns a 10x20 array with (0,0,0) color code
        Also accepts <existing_blocks> which stores keys as a grid coordinate and a color as the corresponding value
        Colors from <existing_blocks> are placed onto the array at the correct position
    """
    grid = []
    for i in range(GRID_HEIGHT//BLOCK_SIZE):
        row = []
        for j in range(GRID_WIDTH//BLOCK_SIZE):
            if (i, j) in existing_blocks:
                row.append(existing_blocks[(i,j)])
            else:
                row.append((0,0,0))
        grid.append(row)
    return grid

def get_rotation_positions(tetri):
    """Converts the 5x5 array shape rotation format to the corresponding positions of each block of the Tetrimino on the game grid"""
    positions = []
    rotation_state = tetri.shape[tetri.r_state % tetri.num_r_state]
    # print(rotation_state)
    # print(len(rotation_state))

    for i in range((len(rotation_state))):
        for j in range(len(rotation_state[i])):
            if rotation_state[i][j] == "*":
                positions.append((tetri.x + j-2, tetri.y + i-4))
    return positions

def valid_space(shape: Game_piece, grid: []) -> bool:
    """Reads current position of shape and ensures that no more than one color occupies on position on the game grid"""
    accepted_pos = set()

    for i in range(GRID_HEIGHT//BLOCK_SIZE):
        for j in range(GRID_WIDTH//BLOCK_SIZE):
            if grid[i][j] == (0,0,0):
                accepted_pos.add((j,i))
            
    rotation_positions = get_rotation_positions(shape)

    for pos in rotation_positions:
        if pos not in accepted_pos and pos[1] > -1:
            return False
    return True

def check_end_condition(positions: dict) -> bool:
    """Checks if any blocks have been stacked past the top of the game grid
        Serves as an indicator to end the main game loop"""
    for pos in positions:
        if pos[0] < 0:
            return True
    return False

def clear_rows(grid: [], existing_blocks: dict) -> int:
    """Clears any full rows on the game grid, returns how many rows were cleared in one instance"""
    cleared_rows = 0
    
    for i in range(len(grid)-1,-1,-1):
        if (0,0,0) not in grid[i]:
            cleared_rows += 1
            index = i
            for j in range(len(grid[i])):
                #removes blocks that are in full rows
                del existing_blocks[(i, j)]

    if cleared_rows > 0:
        #Sort blocks by their y value
        sort_blocks = sorted(list(existing_blocks))
        for block in sort_blocks[::-1]:
            y, x = block
            if y < index: # Shift above rows down if y value is above a certain index 
                existing_blocks[(y + cleared_rows, x)] = existing_blocks.pop(block) 
    return cleared_rows

def draw_window(win, grid, score = 0):
    """Displays the game grid, score and title for Tetris"""
    win.fill((0, 0, 0))

    pg.font.init()
    font = pg.font.SysFont("Arial", 40)
    label = font.render("Tetris", 1, (255,255,255))

    #Title Label
    win.blit(label, (TOP_LEFT[0] + GRID_WIDTH/2 - (label.get_width()/2), 30))

    #Fills in each individual block on game grid
    for row in range(GRID_HEIGHT//BLOCK_SIZE):
        for col in range(GRID_WIDTH//BLOCK_SIZE):
            pg.draw.rect(win, grid[row][col],  (TOP_LEFT[0] + col * 25, TOP_LEFT[1] + row * 25, 25, 25), 0)

    #Draws the lines of the game grid
    for row in range(GRID_HEIGHT//BLOCK_SIZE):
        pg.draw.line(win,(112,128,144),(TOP_LEFT[0], row*BLOCK_SIZE + TOP_LEFT[1]), (TOP_LEFT[0]+GRID_WIDTH, row*BLOCK_SIZE + TOP_LEFT[1]))

    for col in range(GRID_WIDTH//BLOCK_SIZE):
        pg.draw.line(win, (112,128,144),(TOP_LEFT[0] + col*BLOCK_SIZE, TOP_LEFT[1]), (TOP_LEFT[0] + col*BLOCK_SIZE, TOP_LEFT[1] + GRID_HEIGHT))


    #Draws surrounding border of game grid
    pg.draw.rect(win, (255,255,255), (TOP_LEFT[0]-1, TOP_LEFT[1], GRID_WIDTH+1, GRID_HEIGHT+1), 1)
    
    #Displays the sccore
    font = pg.font.SysFont("Arial", 30)
    label = font.render("Score: " + str(score), 1, (255,255,255))
    win.blit(label, (TOP_LEFT[0] - 160, TOP_LEFT[1] + 300))

def run(win,test_mode=False):
    #Testing mode to ensure that tetriminos are in the same order everytime
    if test_mode:
        random.seed(0)
    
    existing_blocks = {}
    new_piece = False
    run = True
    
    cur_tetri = Game_piece()
    clock = pg.time.Clock()
    tetrimino_time = 0

    # lower game_speed makes the game faster
    game_speed = 0.07
    stopped_fall = False
    stopped_time = 0
    score = 0
    while run:
        grid = generate_grid(existing_blocks)
        tetrimino_time += clock.get_rawtime()
        # level_time += clock.get_rawtime()s
        clock.tick(90)
       
        # print(cur_tetri.y)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                
            #User input, if an action is invalid then the system will undo that action
            if event.type == pg.KEYDOWN:
                # Case for when the Tetrimino has stopped falling and this allows the user to have a bit of extra time to finalize their tetrimino placement
                if stopped_fall: 
                    stopped_time -= 0.1

                if event.key == pg.K_LEFT:
                    cur_tetri.x -= 1

                    if not valid_space(cur_tetri, grid):
                        cur_tetri.x += 1

                if event.key == pg.K_RIGHT:
                    cur_tetri.x += 1
                    
                    if not valid_space(cur_tetri, grid):
                        cur_tetri.x -= 1
                
                if event.key == pg.K_SPACE:
                    while valid_space(cur_tetri, grid):
                        cur_tetri.y += 1
                        if not valid_space(cur_tetri, grid):
                            cur_tetri.y -= 1
                            break
                    # Set stopped_time to a high value to instantly lock it
                    stopped_time = 5    
                if event.key == pg.K_DOWN:
                    cur_tetri.y += 1
                    if not valid_space(cur_tetri, grid):
                        cur_tetri.y -= 1

                if event.key == pg.K_UP: 
                    cur_tetri.r_state += 1
                    # print("up")
                    if not valid_space(cur_tetri, grid):
                        cur_tetri.r_state -= 1

        # Periodicly the game will lower the tetrimino
        if 1000 * game_speed < tetrimino_time:
            tetrimino_time = 0
            cur_tetri.y += 1
            if new_piece:
                stopped_fall = True
            if stopped_fall:
                stopped_time += 1
          
            # Case for when the Tetrimino overshoots and a new tetrimino should be generated
            if not (valid_space(cur_tetri, grid)) and cur_tetri.y > 0:
                cur_tetri.y -= 1
                new_piece = True
            elif (valid_space(cur_tetri, grid)) and cur_tetri.y > 0:
                new_piece = False

            stopped_fall = False

        shape_pos = get_rotation_positions(cur_tetri)

        #Adding the block to the grid
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = cur_tetri.color

        # Locks in a tetrimino after it stops falling after a certain amount of time and generates a new tetrimino
        if new_piece and stopped_time > 3:
            for pos in shape_pos:
                p = (pos[1], pos[0])
                existing_blocks[p] = cur_tetri.color

            score += clear_rows(grid, existing_blocks) * 5            

            #Reseeting flags and counters
            cur_tetri = Game_piece()
            new_piece = False
            stopped_fall = False 
            stopped_time = 0

        
        draw_window(win, grid, score)
        pg.display.update()
        if check_end_condition(existing_blocks):
            label = pg.font.SysFont('arial', 20, bold = True).render("You Lost", 1, (255,255,255))
            win.blit(label, (TOP_LEFT[0] + GRID_WIDTH//2 - (label.get_width()/2), TOP_LEFT[1] + GRID_HEIGHT//2 - label.get_height()))
            pg.display.update()
            pg.time.delay(1500)

