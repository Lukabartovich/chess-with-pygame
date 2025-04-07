import pygame
import time
from pieces import *

pygame.init()

size = 64
window = pygame.display.set_mode((8*size, 8*size))
clock = pygame.time.Clock()

black_squares = (6, 148, 39)
white_squares = (38, 201, 76)
highlight = 100

selected_piece = None
click = False
    
move = 'w'

check = False

def load_game(string):
    global move
    
    string, move = string.split(' ')
    
    st = ''
    for char in string:
        if char.isdigit():
            n = int(char)
            st += ' '*n
        else:
            st += char
            
    string = st
    
    lines = string.split('/')
    for i, line in enumerate(lines):
        skip = 0
        for j, char in enumerate(line):
            if char == 'p':
                piece = Pawn('b')
            if char == 'b':
                piece = Bishop('b')
            if char == 'n':
                piece = Knight('b')
            if char == 'r':
                piece = Rook('b')
            if char == 'q':
                piece = Queen('b')
            if char == 'k':
                piece = King('b')
                
            if char == 'P':
                piece = Pawn('w')
            if char == 'B':
                piece = Bishop('w')
            if char == 'N':
                piece = Knight('w')
            if char == 'R':
                piece = Rook('w')
            if char == 'Q':
                piece = Queen('w')
            if char == 'K':
                piece = King('w')
                    
            if char != ' ':
                piece.locate((j, i), size)

def make_dirs(piece, selected_piece):
    dir = [piece.position[0]-selected_piece.position[0], piece.position[1]-selected_piece.position[1]]
    if dir[0] < 0:
        dir[0] = -1
    elif dir[0] > 0:
        dir[0] = 1
    else:
        dir[0] = 0
        
    if dir[1] < 0:
        dir[1] = -1
    elif dir[1] > 0:
        dir[1] = 1
    else:
        dir[1] = 0
    
    return dir

def calculate_allowed_moves(selected_piece):
    moves = selected_piece.moveset
    pos = selected_piece.position
    
    lines = moves.split('/')
    piece_line = 0
    piece_row = 0
    for i, line in enumerate(lines):
        if 'p' in line:
            for j, char in enumerate(line):
                if char=='p':
                    piece_row=j
            piece_line=i
            
            
    selected_positions = []
    capture_moves = []
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == 'x':
                position = (j+pos[0]-piece_row, i+pos[1]-piece_line)
                selected_positions.append(position)
            if char == 'c':
                position = (j+pos[0]-piece_row, i+pos[1]-piece_line)
                capture_moves.append(position)
    
    
    #Check if the currently selected moves are allowed by the rules of chess
    if selected_piece.can_be_blocked == False:
        dirs_blocking = []
        values = []
        has_cp = bool(len(selected_piece.capture_moves)>0)
        for piece in pieces:
            if piece.position in selected_positions:
                if piece.color == selected_piece.color or has_cp:
                    selected_positions.remove(piece.position)
                    
                dir = make_dirs(piece, selected_piece)
                dirs_blocking.append([dir, piece.position])
                    
        for dir, pos in dirs_blocking:
            if dir[0] != 0:
                row_x = [i for i in range(pos[0]+dir[0], 9*dir[0], dir[0])]
            else:
                row_x = [pos[0] for i in range(9)]
                
            if dir[1] != 0:
                row_y = [i for i in range(pos[1]+dir[1], 9*dir[1], dir[1])]
            else:
                row_y = [pos[1] for i in range(9)]
                
            if len(row_x) > len(row_y):
                row_x = row_x[:len(row_y)]
            elif len(row_y) > len(row_x):
                row_y = row_y[:len(row_x)]
                
            for i in range(len(row_x)):
                values.append((row_x[i], row_y[i]))
        s = []
        for moves in selected_positions:
            for value in values:
                if moves[0] == value[0] and moves[1] == value[1]:
                    pass
                else:
                    if value not in s:
                        s.append(value)
                        
        # THIS IS A MESS OF A SORT SYSTEM BUT IT WOTKS :D
        l = []
        for p in s:
            if p not in l:
                l.append(p)
                
        s = l
        li = []
        for p in selected_positions:
            if p not in l:
                li.append(p)
                
        selected_positions=li
    else:
        for piece in pieces:
            if piece.position in selected_positions and piece.color == selected_piece.color:
                selected_positions.remove(piece.position)
        
    return selected_positions, capture_moves

def check_for_check():
    check = False
    kings_positions = [king.position for king in kings]
    for piece in pieces:
        selected_positions, capture_moves = calculate_allowed_moves(piece)
        for king_pos in kings_positions:
            if king_pos in selected_positions or king_pos in capture_moves:
                check = True
    return check
                    
#basic: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w
#testing: 2n1Q3/Ppppp3/pPP5/8/4P1p1/5B2/4p1P1/8 w
load_game('rnb1kb1r/ppppp1pp/7n/3q1p2/4P3/3P4/PPP2PPP/RNBQKBNR w')

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    window.fill(black_squares)
    
    #draw the board
    step = True
    for y in range(8):  
        for x in range(8):
            if step:
                rect = pygame.Rect(x*size, y*size, size, size)
                pygame.draw.rect(window, white_squares, rect)
                
            step = not step
        step = not step
    
    #the click check
    if pygame.mouse.get_pressed()[0]==False and click==True:
        click = False
        clicked = False
    
    check = check_for_check()
    
    #check for allowed moves and capture moves and highlight them
    if selected_piece:
        selected_positions, capture_moves = calculate_allowed_moves(selected_piece)
        
        
        if check:
            s = []
            og_pos = selected_piece.position
            for moves in selected_positions:
                selected_piece.position = moves
                if not check_for_check():
                    s.append(moves)
                
            selected_piece.position = og_pos
            selected_positions = s
            
        selected_piece.allowed_moves = selected_positions
        selected_piece.capture_moves = capture_moves
                    
        for s in selected_positions:
            n = s[0]+s[1]
            c = 1 if n%2==0 else 0
            
            if c==1:
                color = (white_squares[0], white_squares[1], white_squares[2]+highlight)
            else:
                color = (black_squares[0], black_squares[1], black_squares[2]+highlight)
            
            
            rect = pygame.Rect(s[0]*size, s[1]*size, size, size)
            pygame.draw.rect(window, color, rect)

        for s in capture_moves:
            for piece in pieces:
                if piece.position == s and piece.color != selected_piece.color:
                    n = s[0]+s[1]
                    c = 1 if n%2==0 else 0
                    
                    if c==1:
                        color = (white_squares[0]+highlight, white_squares[1], white_squares[2])
                    else:
                        color = (black_squares[0]+highlight, black_squares[1], black_squares[2])
                    
                    
                    rect = pygame.Rect(s[0]*size, s[1]*size, size, size)
                    pygame.draw.rect(window, color, rect)
                    
                    
        #select a piece, check for captures and move pieces
    mouse_point = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] and click == False:
        clicked = False
        for piece in pieces:
            if piece.rect.collidepoint(mouse_point) and clicked == False and move == piece.color:
                clicked=True
                selected_piece = piece
                
        if clicked == False:
            if selected_piece:
                p = (mouse_point[0]//size, mouse_point[1]//size)
                if p in selected_piece.allowed_moves or p in selected_piece.capture_moves:
                    #check for captures
                    for piece in pieces:
                        if piece.position == p and piece.color != selected_piece.color:
                            if len(selected_piece.capture_moves):
                                if p in selected_piece.capture_moves:
                                    pieces.remove(piece)
                            else:
                                pieces.remove(piece)
                                
                    selected_piece.locate(p, size)
                    if move == 'w':
                        move = 'b'
                    else:
                        move = 'w'
                else:
                    pass
                    
            selected_piece = None
            
        click = True
    
    pieces.update()
    pieces.draw(window)
    
    clock.tick(180)
    pygame.display.update()
    #print(clock.get_fps())
    
pygame.quit()