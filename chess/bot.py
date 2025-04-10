import random

def change_move(move):
    if move == 'w':
        move = 'b'
    else:
        move = 'w'
    return move

def make_random_move(pieces, move, size):
    l = []
    for piece in pieces:
        if piece.color == move:
            l.append(piece)
            
    piece = random.choice(l)
    s, c = piece.allowed_moves, piece.capture_moves
    m = random.choice(s)
    piece.locate(m, size)
    move = change_move(move)
    return move