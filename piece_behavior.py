from tkinter import PhotoImage
from game_state import Find
from game_state import Info
from sprite_loader import SpriteSheet


# TODO:
# redesign sprites in aseprite
# make the pawn sprite smaller
# add white outlines to the black pieces
# add a faint thin outline of the opposite color in every piece for better visibility


class Piece:
    def __init__(self, name:str, color:str, position:tuple):
        self.name = name
        self.color = color
        self.pos = position
        self.image = None

    
    def get_info(self) -> str:
        return f'{self.color}\n{self.name}\n{self.pos}'
    

    def __repr__(self):
        return f'{self.color}{self.name} {self.pos}'




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
            if Info.is_blocked(x+i*-1, y):
                break
            else:
                moves.append((x+i*-1, y))

        return moves


    def can_capture(self) -> list:
        x, y = self.pos
        return [(x-1,y+i) for i in range(-1,2,2) if Info.is_enemy(self, (x-1,y+i))]


    def is_attacking(self) -> list:
        x, y = self.pos
        return [(x-1,y+i) for i in range(-1,2,2) if Info.is_inside(x-1,y+i)]




class Rook(Piece):
    def __init__(self, color:str, position:tuple):
        super().__init__(name='Rook', color=color, position=position)
        loader = SpriteSheet(file='assets/ChessPiecesArray.png')
        w_rook = loader.get_sprite((60,60), (1,2))
        b_rook = loader.get_sprite((60,60), (0,2))
        self.image = w_rook if color == 'White' else b_rook
        self.directions = ((-1,0), (1,0), (0,-1), (0,1))


    def can_move(self) -> list:
        moves = list()
        for i in self.directions:
            moves += Find.find_path(self, i)
        return moves


    def can_capture(self) -> list:
        captures = list()
        for i in self.directions:
            captures += Find.find_captures(self, i)
        return captures


    def is_attacking(self) -> list:
        attacks = list()
        for i in self.directions:
            attacks += Find.find_attacks(self, i)
        return attacks



class Knight(Piece):
    def __init__(self, color:str, position:tuple):
        super().__init__(name='Knight', color=color, position=position)
        loader = SpriteSheet(file='assets/ChessPiecesArray.png')
        w_knight = loader.get_sprite((60,60), (1,3))
        b_knight = loader.get_sprite((60,60), (0,3))
        self.image = w_knight if color == 'White' else b_knight


    def jumps(self) -> tuple:
        x, y = self.pos
        return ((x-1,y-2), (x+1,y-2), (x+2,y-1), (x+2,y+1),
                (x+1,y+2), (x-1,y+2), (x-2,y-1), (x-2,y+1))


    def can_move(self) -> list:
        moves = list()
        for i in self.jumps():
            if Info.is_empty(i):
                moves.append(i)
        return moves


    def can_capture(self) -> list:
        return Info.is_enemy(self, self.jumps())


    def is_attacking(self) -> list:
        return [i for i in self.jumps() if Info.is_inside(*i)]




class Bishop(Piece):
    def __init__(self, color:str, position:tuple):
        super().__init__(name='Bishop', color=color, position=position)
        loader = SpriteSheet(file='assets/ChessPiecesArray.png')
        w_bishop = loader.get_sprite((60,60), (1,4))
        b_bishop = loader.get_sprite((60,60), (0,4))
        self.image = w_bishop if color == 'White' else b_bishop
        self.directions = ((-1,-1), (1,-1), (1,+1), (-1,+1))


    def can_move(self) -> list:
        moves = list()
        for i in self.directions:
            moves += Find.find_path(self, i)
        return moves


    def can_capture(self) -> list:
        captures = list()
        for i in self.directions:
            captures += Find.find_captures(self, i)
        return captures


    def is_attacking(self) -> list:
        attacks = list()
        for i in self.directions:
            attacks += Find.find_attacks(self, i)
        return attacks


class Queen(Piece):
    def __init__(self, color:str, position:tuple):
        super().__init__(name='Queen', color=color, position=position)
        loader = SpriteSheet(file='assets/ChessPiecesArray.png')
        w_queen = loader.get_sprite((60,60), (1,0))
        b_queen = loader.get_sprite((60,60), (0,0))
        self.image = w_queen if color == 'White' else b_queen
        self.directions = ((-1,-1), (1,-1), (1,+1), (-1,+1),
                           (-1,0), (1,0), (0,-1), (0,1))


    def can_move(self) -> list:
        moves = list()
        for i in self.directions:
            moves += Find.find_path(self, i)
        return moves


    def can_capture(self) -> list:
        captures = list()
        for i in self.directions:
            captures += Find.find_captures(self, i)
        return captures


    def is_attacking(self) -> list:
        attacks = list()
        for i in self.directions:
            attacks += Find.find_attacks(self, i)
        return attacks
    

class King(Piece):
    def __init__(self, color:str, position:tuple):
        super().__init__(name='King', color=color, position=position)
        loader = SpriteSheet(file='assets/ChessPiecesArray.png')
        w_king = loader.get_sprite((60,60), (1,1))
        b_king = loader.get_sprite((60,60), (0,1))
        self.image = w_king if color == 'White' else b_king
        self.first_move = True


    def directions(self):
        x, y = self.pos
        return ((x-1,y-1), (x+1,y-1), (x+1,y+1), (x-1,y+1),
                (x-1,y+0), (x+1,y+0), (x+0,y-1), (x+0,y+1))


    def can_move(self) -> list:
        return [i for i in self.directions() if Info.is_empty(i)]


    def can_capture(self) -> list:
        return Info.is_enemy(self, self.directions())


    def is_attacking(self) -> list:
        return [i for i in self.directions() if Info.is_inside(*i)]


if __name__ == '__main__':
    ...