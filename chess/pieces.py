import pygame

pieces = pygame.sprite.Group()

class Piece(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.image = pygame.image.load('images/w_King.png')
        self.rect = self.image.get_rect()
        self.moveset = ""
        self.moved = False
        self.position = (0, 0)
        self.cost = 1
        self.allowed_moves = []
        
        pieces.add(self)
        
    def locate(self, position, size):
        self.moved = True
        self.position = position
        self.rect.topleft = (position[0]*size, position[1]*size)
        self.update_moveset()
        
    def update_moveset(self):
        pass
        
        
class Pawn(Piece):
    def __init__(self, color='w'):
        super().__init__()
        
        self.image = pygame.image.load(f'images/{color}_Pawn.png')
        self.color=color
        
        
    def update_moveset(self):
        if self.color == 'w':
            if self.position[1] == 6:
                self.moveset = "x/x/p"
            else:
                self.moveset = "x/p"
        else:
            if self.position[1] == 1:
                self.moveset = "p/x/x"
                print('pawn can move 2')
            else:
                self.moveset = "p/x"