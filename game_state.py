


class GameState:
    board = [[None for row in range(8)] for col in range(8)]
    selected = None
    moves = None
    captures = None
    last_move = None


    @classmethod
    def process_action(cls, x, y) -> bool:
        if (x,y) in cls.moves:
            cls.register(cls.selected, (x,y))

        elif (x,y) in cls.captures:
            cls.register(cls.selected, (x,y))

        else:
            cls.clear_selected()
            return False
        
        cls.clear_selected()
        return True


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
    def register(cls, piece, new_pos:list|tuple):
        old_x, old_y = piece.pos
        new_x, new_y = new_pos
        piece.pos = new_pos
        cls.board[old_x][old_y] = None
        cls.board[new_x][new_y] = piece

        cls.last_move = ((old_x, old_y), (new_x, new_y))
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

        if type(pos[0]) != tuple:
            pos = [pos]
        
        for x, y in pos:
            if not cls.is_inside(x, y):
                continue

            if cls.is_piece(x, y) and cls.color(x,y) == enemy_color:
                enemy_pos.append((x,y))

        return enemy_pos
    

    @classmethod
    def is_empty(cls, pos:list[tuple]) -> list:
        empty_pos = list()

        if type(pos[0]) != tuple:
            pos = [pos]

        for x, y in pos:
            if not cls.is_inside(x, y):
                continue

            if not cls.is_piece(x, y):
                empty_pos.append((x,y))

        return empty_pos


    @classmethod
    def is_blocked(cls, x, y) -> bool:
        return cls.is_inside(x, y) and cls.is_piece(x, y)


    @classmethod
    def find_possible_actions(cls, x, y):
        cls.moves = cls.get(x,y).can_move()
        cls.captures = cls.get(x,y).can_capture()


    @classmethod
    def find_path(cls, direction):
        x, y = cls.selected.pos
        mod_x, mod_y = direction
        path = list()
        while True:
            x += mod_x
            y += mod_y
            if cls.is_blocked(x, y) or not cls.is_inside(x, y):
                break
            else:
                path.append((x,y))
        return path


    @classmethod
    def find_captures(cls, direction):
        x, y = cls.selected.pos
        mod_x, mod_y = direction
        captures = list()
        while True:
            x += mod_x
            y += mod_y
            if not cls.is_inside(x,y):
                break
            if not cls.is_piece(x,y):
                continue
            if cls.is_enemy(cls.selected, (x,y)):
                captures.append((x,y))
            break    
        return captures


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
    def can_move(cls) -> list:
        possible_moves = list()

        if cls.moves is not None:
            possible_moves += cls.moves

        if cls.captures is not None:
            possible_moves += cls.captures

        return possible_moves


    @classmethod
    def color(cls, x, y) -> str:
        if cls.is_piece(x, y):
            return cls.board[x][y].color


    @classmethod
    def get(cls, x, y) -> object | None:
        return cls.board[x][y]









if __name__ == '__main__':
    pass