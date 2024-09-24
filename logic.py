from tkinter import PhotoImage
from game_state import Piece



class Pawn(Piece):
    def __init__(self, color:str, position:tuple):
        super().__init__(name='Pawn', color=color, position=position)
        self.first_move = True
        self.white_img = PhotoImage(file='assets/white/w_pawn.png')
        self.black_img = PhotoImage(file='assets/black/b_pawn.png')


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
        self.white_img = PhotoImage(file='assets/white/w_rook.png')
        self.black_img = PhotoImage(file='assets/black/b_rook.png')




class Knight(Piece):
    def __init__(self, color:str, position:tuple):
        super().__init__(name='Knight', color=color, position=position)
        self.white_img = PhotoImage(file='assets/white/w_knight.png')
        self.black_img = PhotoImage(file='assets/black/b_knight.png')




class Bishop(Piece):
    def __init__(self, color:str, position:tuple):
        super().__init__(name='Bishop', color=color, position=position)
        self.white_img = PhotoImage(file='assets/white/w_bishop.png')
        self.black_img = PhotoImage(file='assets/black/b_bishop.png')




class Queen(Piece):
    def __init__(self, color:str, position:tuple):
        super().__init__(name='Queen', color=color, position=position)
        self.white_img = PhotoImage(file='assets/white/w_queen.png')
        self.black_img = PhotoImage(file='assets/black/b_queen.png')




class King(Piece):
    def __init__(self, color:str, position:tuple):
        super().__init__(name='King', color=color, position=position)
        self.white_img = PhotoImage(file='assets/white/w_king.png')
        self.black_img = PhotoImage(file='assets/black/b_king.png')
        self.first_move = True


if __name__ == '__main__':
    for i in range(-1, 2, 2):
        print(i)