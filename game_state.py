from typing import Type


class GameState:
    board = [[None for row in range(8)] for col in range(8)]
    selected = None
    moves = None
    captures = None


    @classmethod
    def process_action(cls, x, y):
        if cls.selected is None:
            return

        if (x,y) in cls.moves:
            cls.register(cls.selected, (x,y))

        elif (x,y) in cls.captures:
            cls.register(cls.selected, (x,y))
        
        cls.clear_selected()


    @classmethod
    def clear_selected(cls):
        cls.selected = None
        cls.moves = None
        cls.captures = None


    @classmethod
    def select(cls, x, y):
        if cls.is_piece(x, y):
            cls.selected = cls.board[x][y]
            cls.find_possible_actions(x, y)


    @classmethod
    def can_select(cls, x, y) -> bool:
        return cls.selected is None and cls.is_piece(x, y)


    @classmethod
    def can_change_selection(cls, x, y) -> bool:
        if cls.selected is not None:
            return cls.is_piece(x, y) and cls.is_same_color(x, y)


    @classmethod
    def register(cls, piece, new_pos:list|tuple):
        old_x, old_y = piece.pos
        new_x, new_y = new_pos
        piece.pos = new_pos
        cls.board[old_x][old_y] = None
        cls.board[new_x][new_y] = piece

        cls.first_move_status(*new_pos)


    @classmethod
    def first_move_status(cls, x, y):
        piece = cls.board[x][y]
        if piece.name in ('Pawn', 'King'):
            piece.first_move = False


    @classmethod
    def is_enemy(cls, piece, pos:list[tuple]) -> list:
        enemy_color = 'Black' if piece.color == 'White' else 'White'
        enemy_pos = list()

        for x, y in pos:
            if not cls.is_inside(x, y):
                continue

            if cls.is_piece(x, y) and cls.color(x,y) == enemy_color:
                enemy_pos.append((x,y))

        return enemy_pos


    @classmethod
    def is_blocked(cls, x, y) -> bool:
        return cls.is_inside(x, y) and cls.is_piece(x, y)


    @classmethod
    def find_possible_actions(cls, x, y):
        cls.moves = cls.get(x,y).can_move()
        cls.captures = cls.get(x,y).can_capture()


    @classmethod
    def is_inside(cls, x, y) -> bool:
        return (0 <= x < 8) and (0 <= y < 8)


    @classmethod
    def is_piece(cls, x, y) -> bool:
        return cls.board[x][y] is not None


    @classmethod
    def is_same_color(cls, x, y) -> bool:
        if cls.is_piece(x, y):
            return cls.color(x,y) == cls.selected.color


    @classmethod
    def color(cls, x, y) -> str:
        if cls.is_piece(x, y):
            return cls.board[x][y].color


    @classmethod
    def get(cls, x, y) -> Type['Piece'] | None:
        return cls.board[x][y]




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




if __name__ == '__main__':
    a = GameState.is_inside(5,1)
    print(a)