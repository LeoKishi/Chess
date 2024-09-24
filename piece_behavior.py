from tkinter import PhotoImage
from game_state import Piece
from sprite_loader import SpriteSheet


# TODO:
# redesign sprites in aseprite
# make the pawn sprite smaller
# add white outlines to the black pieces
# add a faint thin outline of the opposite color in every piece for better visibility


class Pawn(Piece):
    def __init__(self, color:str, position:tuple):
        super().__init__(name='Pawn', color=color, position=position)
        loader = SpriteSheet(file='assets/ChessPiecesArray.png')
        w_pawn = loader.get_sprite((60,60), (1,5))
        b_pawn = loader.get_sprite((60,60), (0,5))
        self.image = w_pawn if color == 'White' else b_pawn
        self.first_move = True


    def can_move(self) -> list:
        x, y = self.pos
        moves = list()

        for i in range(1, 3 if self.first_move else 2):
            if self.is_blocked(x+i*-1, y):
                break
            else:
                moves.append((x+i*-1, y))

        return moves


    def can_capture(self) -> list:
        x, y = self.pos
        captures = list()

        for i in range(-1, 2, 2):
            if self.is_enemy(self, [(x-1, y+i)]):
                captures.append((x-1, y+i))

        return captures




class Rook(Piece):
    def __init__(self, color:str, position:tuple):
        super().__init__(name='Rook', color=color, position=position)
        loader = SpriteSheet(file='assets/ChessPiecesArray.png')
        w_rook = loader.get_sprite((60,60), (1,2))
        b_rook = loader.get_sprite((60,60), (0,2))
        self.image = w_rook if color == 'White' else b_rook



class Knight(Piece):
    def __init__(self, color:str, position:tuple):
        super().__init__(name='Knight', color=color, position=position)
        loader = SpriteSheet(file='assets/ChessPiecesArray.png')
        w_knight = loader.get_sprite((60,60), (1,3))
        b_knight = loader.get_sprite((60,60), (0,3))
        self.image = w_knight if color == 'White' else b_knight



class Bishop(Piece):
    def __init__(self, color:str, position:tuple):
        super().__init__(name='Bishop', color=color, position=position)
        loader = SpriteSheet(file='assets/ChessPiecesArray.png')
        w_bishop = loader.get_sprite((60,60), (1,4))
        b_bishop = loader.get_sprite((60,60), (0,4))
        self.image = w_bishop if color == 'White' else b_bishop



class Queen(Piece):
    def __init__(self, color:str, position:tuple):
        super().__init__(name='Queen', color=color, position=position)
        loader = SpriteSheet(file='assets/ChessPiecesArray.png')
        w_queen = loader.get_sprite((60,60), (1,0))
        b_queen = loader.get_sprite((60,60), (0,0))
        self.image = w_queen if color == 'White' else b_queen



class King(Piece):
    def __init__(self, color:str, position:tuple):
        super().__init__(name='King', color=color, position=position)
        loader = SpriteSheet(file='assets/ChessPiecesArray.png')
        w_king = loader.get_sprite((60,60), (1,1))
        b_king = loader.get_sprite((60,60), (0,1))
        self.image = w_king if color == 'White' else b_king
        self.first_move = True


if __name__ == '__main__':
    ...