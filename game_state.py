


class GameState:
    board = [[None for row in range(8)] for col in range(8)]
    selected = None
    moves = None
    captures = None
    attacks = None
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
        if Info.is_piece(x, y):
            cls.selected = Info.get(x,y)
            Find.find_possible_actions(x, y)

    @classmethod
    def register(cls, piece, new_pos:list|tuple):
        old_x, old_y = piece.pos
        new_x, new_y = new_pos
        piece.pos = new_pos
        cls.board[old_x][old_y] = None
        cls.board[new_x][new_y] = piece

        cls.last_move = ((old_x, old_y), (new_x, new_y))
        cls.first_move_status(*new_pos)
        Find.find_checks(Info.get(*new_pos))

    @staticmethod
    def first_move_status(x, y):
        piece = Info.get(x,y)
        if piece.name in ('Pawn', 'King'):
            piece.first_move = False




class Find:

    @staticmethod
    def find_checks(piece):
        attacks = list()
        for x,y in Util.range2d():
            if Info.is_piece(x,y) and Info.color(x,y) == piece.color:
                attacks += Info.get(x,y).is_attacking()
        GameState.attacks = list(set(attacks))

    @staticmethod
    def find_attacks(piece, direction) -> list:
        x, y = piece.pos
        mod_x, mod_y = direction
        attacks = list()
        while True:
            x += mod_x
            y += mod_y
            if not Info.is_inside(x, y):
                break
            elif not Info.is_empty(x, y):
                attacks.append((x,y))
                break
            attacks.append((x,y))
        return attacks

    @staticmethod
    def find_captures(piece, direction) -> list:
        x, y = piece.pos
        mod_x, mod_y = direction
        captures = list()
        while True:
            x += mod_x
            y += mod_y
            if Info.is_enemy(GameState.selected, (x,y)):
                captures.append((x,y))
            elif Info.is_inside(x,y):
                continue
            break
        return captures
    
    @staticmethod
    def find_path(piece, direction) -> list:
        x, y = piece.pos
        mod_x, mod_y = direction
        path = list()
        while True:
            x += mod_x
            y += mod_y
            if not Info.is_empty(x, y):
                break
            path.append((x,y))
        return path

    @staticmethod
    def find_possible_actions(x, y):
        GameState.moves = Info.get(x,y).can_move()
        GameState.captures = Info.get(x,y).can_capture()




class Info:

    @classmethod
    def is_enemy(cls, piece, pos:list[tuple]) -> list:
        enemy_color = 'Black' if piece.color == 'White' else 'White'
        enemy_pos = list()

        if type(pos[0]) != tuple:
            pos = [pos]
        
        for x, y in pos:
            if cls.is_piece(x, y) and cls.color(x,y) == enemy_color:
                enemy_pos.append((x,y))

        return enemy_pos
    
    @classmethod
    def is_empty(cls, x, y) -> list:
        if cls.is_inside(x, y) and Info.get(x,y) is None:
            return True

    @staticmethod
    def possible_moves() -> list:
        possible_moves = list()

        if GameState.moves is not None:
            possible_moves += GameState.moves

        if GameState.captures is not None:
            possible_moves += GameState.captures

        return possible_moves     

    @staticmethod
    def is_inside(x, y) -> bool:
        return (0 <= x < 8) and (0 <= y < 8)

    @staticmethod
    def get(x, y) -> object | None:
        return GameState.board[x][y]

    @classmethod
    def color(cls, x, y) -> str | None:
        if cls.is_piece(x, y):
            return GameState.board[x][y].color

    @classmethod
    def can_select(cls, x, y) -> bool:
        return GameState.selected is None and cls.is_piece(x, y)

    @classmethod
    def is_piece(cls, x, y) -> bool:
        if not cls.is_inside(x, y):
            return False
        return GameState.board[x][y] is not None
    
    @classmethod
    def is_blocked(cls, x, y) -> bool:
        if not cls.is_inside(x, y):
            return True
        return cls.is_piece(x, y)

    @classmethod
    def is_same_color(cls, x, y) -> bool:
        if cls.is_piece(x, y):
            return cls.color(x,y) == GameState.selected.color




class Util:

    @staticmethod
    def range2d():
        for x in range(8):
            for y in range(8):
                yield (x,y)



if __name__ == '__main__':
    pass