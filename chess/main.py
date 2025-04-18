import pygame
import time
from pieces import *
import threading

pygame.init()

size = 64
window = pygame.display.set_mode((8*size, 8*size))
clock = pygame.time.Clock()

black_squares = (6, 148, 39)
white_squares = (38, 201, 76)
highlight = 100
# highlight = (238, 245, 20)
# capture_move_highlight = (245, 27, 52)
# highlight_size = (size)//6


selected_piece = None
click = False
    
move = 'w'
lm = None
lm2 = None

check = []

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

def calculate_allowed_moves(selected_piece, defend = False):
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
        has_cp = bool(len(capture_moves)>0)
        for piece in pieces:
            if piece.position in selected_positions:
                if (not defend and piece.color == selected_piece.color) or has_cp:
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
                
    if len(capture_moves):
        c = []
        for moves in capture_moves:
            for piece in pieces:
                if piece.color != selected_piece.color and piece.position == moves:
                    c.append(moves)
        capture_moves = c
        
    return selected_positions, capture_moves

def check_for_check():
    check = []
    kings_positions = [king.position for king in kings]
    for piece in pieces:
        selected_positions, capture_moves = calculate_allowed_moves(piece)
        for king_pos in kings_positions:
            if king_pos in selected_positions or king_pos in capture_moves:
                check.append(piece.position)
    return check
    
def check_if_piece_defended(selected_piece):
    defended = False
    for piece in pieces:
        if piece.color == selected_piece.color and piece != selected_piece:
            selected_positions, capture_moves = calculate_allowed_moves(piece, defend=True)
            for pos in selected_positions:
                if pos[0] == selected_piece.position[0] and pos[1] == selected_piece.position[1]:
                    defended = True
            
    return defended
    
def reload_piece(s_piece):
    l = [s_piece]
    p = s_piece.position
    for piece in pieces:
        if p in piece.allowed_moves or p in piece.capture_moves:
            l.append(piece)
            
            
    for s_piece in l:
        selected_positions, capture_moves = calculate_allowed_moves(s_piece)
        
        
        if check:
            s = []
            og_pos = s_piece.position
            for moves in selected_positions:
                s_piece.position = moves
                if not len(capture_moves) and s_piece.position in check:
                    if s_piece.cost == 100:
                        for piece in pieces:
                            if piece.position == s_piece.position and piece != s_piece:
                                
                                if not check_if_piece_defended(piece):
                                    s.append(moves)
                    else:
                        s.append(moves) 
                elif not check_for_check():
                    #TODO make sure that the king can't eat a piece if it's protected
                    s.append(moves)

            s_piece.position = og_pos
            selected_positions = s
            
        s_piece.allowed_moves = selected_positions
        s_piece.capture_moves = capture_moves

def reload_pieces():
    for s_piece in pieces:
        selected_positions, capture_moves = calculate_allowed_moves(s_piece)
        
        
        if check:
            s = []
            og_pos = s_piece.position
            for moves in selected_positions:
                s_piece.position = moves
                if not len(capture_moves) and s_piece.position in check:
                    if s_piece.cost == 100:
                        for piece in pieces:
                            if piece.position == s_piece.position and piece != s_piece:
                                
                                if not check_if_piece_defended(piece):
                                    s.append(moves)
                    else:
                        s.append(moves) 
                elif not check_for_check():
                    #TODO make sure that the king can't eat a piece if it's protected
                    s.append(moves)

            s_piece.position = og_pos
            selected_positions = s
            
        s_piece.allowed_moves = selected_positions
        s_piece.capture_moves = capture_moves
    
#basic: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w
#testing: 2n1Q3/Ppppp3/pPP5/8/4P1p1/5B2/4p1P1/8 w
load_game('rnb1kppr/ppppp2p/7n/3q4/4P3/3P1Q2/1PP2QPP/RNB1KBNR w')

reload_pieces()

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
    if lm2 != lm:
        lm2 = lm
        print('reload moves')
        
        reload_piece(lm)
        
    if selected_piece:
        for s in selected_piece.allowed_moves:
            n = s[0]+s[1]
            c = 1 if n%2==0 else 0
            
            # pygame.draw.circle(window, highlight, ((s[0]*size)+(size//2), (s[1]*size)+(size//2)), highlight_size)
            
            if c==1:
                color = (white_squares[0], white_squares[1], white_squares[2]+highlight)
            else:
                color = (black_squares[0], black_squares[1], black_squares[2]+highlight)
            
            
            rect = pygame.Rect(s[0]*size, s[1]*size, size, size)
            pygame.draw.rect(window, color, rect)

        for s in selected_piece.capture_moves:
            for piece in pieces:
                if piece.position == s and piece.color != selected_piece.color:
                    n = s[0]+s[1]
                    c = 1 if n%2==0 else 0
                    
                    # pygame.draw.circle(window, capture_move_highlight, ((s[0]*size)+(size//2), (s[1]*size)+(size//2)), highlight_size)
                    
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
                    lm = selected_piece
                else:
                    pass
                    
            selected_piece = None
            
        click = True
    
    pieces.update()
    pieces.draw(window) 
    
    clock.tick(180)
    pygame.display.update()
    print(clock.get_fps())
    
pygame.quit()