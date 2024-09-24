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


    def can_move(self) -> list:
        moves = list()
        directions = ((-1,0), (1,0), (0,-1), (0,1))

        def walk(direction):
            x, y = self.pos
            mod_x, mod_y = direction
            path = list()
            while True:
                x += mod_x
                y += mod_y
                if self.is_blocked(x, y) or not self.is_inside(x, y):
                    break
                else:
                    path.append((x,y))
            return path
        
        for i in directions:
            moves += walk(i)

        return moves


    def can_capture(self) -> list:
        captures = list()
        directions = ((-1,0), (1,0), (0,-1), (0,1))

        def walk(direction):
            x, y = self.pos
            mod_x, mod_y = direction
            path = list()
            while True:
                x += mod_x
                y += mod_y
                if not self.is_inside(x,y):
                    break
                if not self.is_piece(x,y):
                    continue
                if self.is_enemy(self, (x,y)):
                    path.append((x,y))
                break    
            return path
        
        for i in directions:
            captures += walk(i)

        return captures




class Knight(Piece):
    def __init__(self, color:str, position:tuple):
        super().__init__(name='Knight', color=color, position=position)
        loader = SpriteSheet(file='assets/ChessPiecesArray.png')
        w_knight = loader.get_sprite((60,60), (1,3))
        b_knight = loader.get_sprite((60,60), (0,3))
        self.image = w_knight if color == 'White' else b_knight


    def can_move(self) -> list:
        x, y = self.pos
        moves = list()
        jumps = ((x-1,y-2), (x+1,y-2), 
                 (x+2,y-1), (x+2,y+1), 
                 (x+1,y+2), (x-1,y+2), 
                 (x-2,y-1), (x-2,y+1))
        
        for i in jumps:
            if self.is_inside(*i) and not self.is_blocked(*i):
                moves.append(i)

        return moves


    def can_capture(self) -> list:
        x, y = self.pos
        jumps = ((x-1,y-2), (x+1,y-2), 
                 (x+2,y-1), (x+2,y+1), 
                 (x+1,y+2), (x-1,y+2), 
                 (x-2,y-1), (x-2,y+1))

        return self.is_enemy(self, jumps)



class Bishop(Piece):
    def __init__(self, color:str, position:tuple):
        super().__init__(name='Bishop', color=color, position=position)
        loader = SpriteSheet(file='assets/ChessPiecesArray.png')
        w_bishop = loader.get_sprite((60,60), (1,4))
        b_bishop = loader.get_sprite((60,60), (0,4))
        self.image = w_bishop if color == 'White' else b_bishop


    def can_move(self) -> list:
        moves = list()
        directions = ((-1,-1), (1,-1), (1,+1), (-1,+1))

        def walk(direction):
            x, y = self.pos
            mod_x, mod_y = direction
            path = list()
            while True:
                x += mod_x
                y += mod_y
                if self.is_blocked(x, y) or not self.is_inside(x, y):
                    break
                else:
                    path.append((x,y))
            return path
        
        for i in directions:
            moves += walk(i)

        return moves


    def can_capture(self) -> list:
        captures = list()
        directions = ((-1,-1), (1,-1), (1,+1), (-1,+1))

        def walk(direction):
            x, y = self.pos
            mod_x, mod_y = direction
            path = list()
            while True:
                x += mod_x
                y += mod_y
                if not self.is_inside(x,y):
                    break
                if not self.is_piece(x,y):
                    continue
                if self.is_enemy(self, (x,y)):
                    path.append((x,y))
                break    
            return path
        
        for i in directions:
            captures += walk(i)

        return captures




class Queen(Piece):
    def __init__(self, color:str, position:tuple):
        super().__init__(name='Queen', color=color, position=position)
        loader = SpriteSheet(file='assets/ChessPiecesArray.png')
        w_queen = loader.get_sprite((60,60), (1,0))
        b_queen = loader.get_sprite((60,60), (0,0))
        self.image = w_queen if color == 'White' else b_queen


    def can_move(self) -> list:
        moves = list()
        directions = ((-1,-1), (1,-1), (1,+1), (-1,+1),
                      (-1,0), (1,0), (0,-1), (0,1))

        def walk(direction):
            x, y = self.pos
            mod_x, mod_y = direction
            path = list()
            while True:
                x += mod_x
                y += mod_y
                if self.is_blocked(x, y) or not self.is_inside(x, y):
                    break
                else:
                    path.append((x,y))
            return path
        
        for i in directions:
            moves += walk(i)

        return moves


    def can_capture(self) -> list:
        captures = list()
        directions = ((-1,-1), (1,-1), (1,+1), (-1,+1),
                      (-1,0), (1,0), (0,-1), (0,1))

        def walk(direction):
            x, y = self.pos
            mod_x, mod_y = direction
            path = list()
            while True:
                x += mod_x
                y += mod_y
                if not self.is_inside(x,y):
                    break
                if not self.is_piece(x,y):
                    continue
                if self.is_enemy(self, (x,y)):
                    path.append((x,y))
                break    
            return path
        
        for i in directions:
            captures += walk(i)

        return captures




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