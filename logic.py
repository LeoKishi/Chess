from tkinter import PhotoImage
from game_state import GameState


# TODO:
# possible actions highlighted in the GUI after selecting piece



class Piece(GameState):
    def __init__(self, name:str, color:str, position:tuple):
        self.name = name
        self.color = color
        self.pos = position
        self.image = None

    
    def get_info(self) -> str:
        return f'{self.color}\n{self.name}\n{self.pos}'
    

    def __repr__(self):
        return f'{self.color}{self.name}'




class Pawn(Piece):
    def __init__(self, color:str, position:tuple):
        super().__init__(name='Pawn', color=color, position=position)
        self.first_move = True
        self.white_img = PhotoImage(file='assets/white/w_pawn.png')
        self.black_img = PhotoImage(file='assets/black/b_pawn.png')


    def can_move(self) -> list:
        x, y = self.pos
        path = -1 if self.color == 'White' else 1
        empty = list()

        for i in range(1, 3 if self.first_move else 2):
            if self.is_blocked(x+i*path, y):
                break
            else:
                empty.append((x+i*path, y))

        return empty


    def can_capture(self) -> list:
        x, y = self.pos
        path = -1 if self.color == 'White' else 1
        empty = list()

        for i in range(-1, 2, 2):
            if self.is_enemy(self, [(x+path, y+i)]):
                empty.append((x+path, y+i))

        return empty




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