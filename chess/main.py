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

test_pawn = Pawn('b')
test_pawn.locate((1, 1), size)

pawn = Pawn('b')
pawn.locate((0, 2), size)

pawn2 = Pawn('w')
pawn2.locate((1, 3), size)

knight = Knight('w')
knight.locate((2, 3), size)

queen = Queen('w')
queen.locate((5, 5), size)

selected_piece = None
click = False

move = 'w'

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
    
    #check for allowed moves and capture moves and highlight them
    if selected_piece:
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
                    
        selected_piece.allowed_moves = selected_positions
        selected_piece.capture_moves = capture_moves
        
        blocking_pos = []
        if selected_piece.can_be_blocked==False:
            remove_directions = []
            for piece in pieces:
                if piece.position in selected_positions:
                    if len(selected_piece.capture_moves)>0:
                        index = selected_positions.index(piece.position)
                        selected_positions.pop(index)
                    dir = (piece.position[0]-selected_piece.position[0], piece.position[1]-selected_piece.position[1])
                    dir = (-1 if dir[0] < 0 else 1, -1 if dir[1] < 0 else 1)
                    remove_directions.append((dir, piece.position))
                    blocking_pos.append(piece.position)
                    
            for dir, values in remove_directions:
                for pos in selected_positions:
                    if pos not in blocking_pos:
                        d = (pos[0]-selected_piece.position[0], pos[1]-selected_piece.position[1])
                        d = (-1 if dir[0] < 0 else 1, -1 if dir[1] < 0 else 1)
                        if d == dir:
                            r = True
                            if dir[0] == 1:
                                if values[0] > pos[0]:
                                    r = False
                            else:
                                if values[0] < pos[0]:
                                    r = False
                                    
                            if dir[1] == 1:
                                if values[1] > pos[1]:
                                    r = False
                            else:
                                if values[1] < pos[1]:
                                    r = False
                            if r:
                                index = selected_positions.index(pos)
                                selected_positions.pop(index)
                    
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
                        color = (white_squares[0], white_squares[1], white_squares[2]+highlight)
                    else:
                        color = (black_squares[0], black_squares[1], black_squares[2]+highlight)
                    
                    
                    rect = pygame.Rect(s[0]*size, s[1]*size, size, size)
                    pygame.draw.rect(window, color, rect)
    
    pieces.update()
    pieces.draw(window)
    
    clock.tick(180)
    pygame.display.update()
    #print(clock.get_fps())
    
pygame.quit()