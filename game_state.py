
# TODO:
# stop a pinned piece from moving if the king is behind it
# castling
# don't allow castling if a square in the path is being attacked
# en passant
# play sounds for piece movement, capture, check and checkmate


class GameState:
    board = [[None for row in range(8)] for col in range(8)]
    selected = None
    moves = None
    captures = None
    last_move = None
    check = False
    pinned = None
    threats = {'attack':list(), 'checking':list(), 'sight':list()}
    turn = 'White'


    @classmethod
    def process_action(cls, x, y):
        old_pos = cls.selected.pos
        cls.register_move(cls.selected, (x,y))

        if Info.is_in_check():
            cls.register_move(cls.selected, old_pos)
            cls.clear_selected()
            # BLINK KING TO SIGNAL CHECK
            print('in check')
            return
        
        cls.register_last_move(cls.selected, (x,y))
        cls.register_threats(x,y)

        if cls.check: cls.try_check_mate()

        cls.first_move_status(x,y)
        cls.new_turn()
        cls.clear_selected()



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
    def register_move(cls, piece, new_pos:list|tuple):
        old_x, old_y = piece.pos
        new_x, new_y = new_pos
        piece.pos = new_pos
        cls.board[old_x][old_y] = None
        cls.board[new_x][new_y] = piece

    @classmethod
    def register_last_move(cls, piece, new_pos:list|tuple):
        cls.last_move = (piece.pos, new_pos)

    @staticmethod
    def first_move_status(x, y):
        piece = Info.get(x,y)
        if piece.name in ('Pawn', 'King'):
            piece.first_move = False

    @classmethod
    def new_turn(cls):
        if cls.turn == 'White':
            cls.turn = 'Black'
        else:
            cls.turn = 'White'

    @classmethod
    def register_threats(cls, x, y):
        attack, checking, sight = Find.find_checks(Info.get(x,y))
        GameState.check = True if checking else False
        GameState.threats = {'attack':attack,
                             'checking':checking,
                             'sight':sight}

    @classmethod
    def try_check_mate(cls) -> bool:
        can_move = True
        can_defend = False
        for x,y in Util.range2d():
            if not Info.is_enemy(cls.selected, (x,y)):
                continue

            if Info.is_king(x,y) and not Info.get(x,y).can_move():
                can_move = False
                print('cannot move')
                continue

            for i in Info.get(x,y).can_move() + Info.get(x,y).can_capture():
                if i in Info.get_sight():
                    can_defend = True
                    return False

        if not can_move and not can_defend:
            print('check mate')

        


            



class Find:

    @classmethod
    def find_checks(cls, piece) -> tuple:
        attacks = list()
        checking = list()
        sight = list()
        for x,y in Util.range2d():
            if not (Info.is_piece(x,y) and Info.color(x,y) == piece.color):
                continue
            for line in Info.get(x,y).is_attacking():
                attacks += line
                if Info.is_in_sight(piece, line):
                    checking.append((x,y))
                    sight += [i for i in line if not Info.is_king(*i)] + [(x,y)]
        return (Util.unique(attacks), checking, sight)

    @staticmethod
    def find_attacks(piece, direction) -> list:
        x, y = piece.pos
        mod_x, mod_y = direction
        attacks = list()
        while True:
            x += mod_x
            y += mod_y
            if Info.is_inside(x, y):
                attacks.append((x,y))
            if not Info.is_empty(x, y):
                break
        return attacks

    @staticmethod
    def find_captures(piece, direction) -> list:
        x, y = piece.pos
        mod_x, mod_y = direction
        captures = list()
        while True:
            x += mod_x
            y += mod_y
            if Info.is_piece(x,y):
                if Info.is_enemy(piece, (x,y)):
                    captures.append((x,y))
                break
            elif not Info.is_inside(x,y):
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
    def is_in_sight(cls, piece, line) -> bool:
        for i in line:
            if not (cls.is_enemy(piece, i) and cls.is_king(*i)):
                continue
            return True

    @classmethod
    def is_in_check(cls) -> bool:
        if not GameState.check:
            return False

        for i in cls.get_checking():
            for j in tuple(set([i for item in Info.get(*i).is_attacking() for i in item])):
                if not Info.is_piece(*j):
                    continue
                if cls.get(*j).name == 'King' and cls.is_enemy(cls.get(*i), j):
                    return True

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
    
    @staticmethod
    def get_attacks() -> list:
        return GameState.threats['attack']

    @staticmethod
    def get_checking() -> list:
        return GameState.threats['checking']

    @staticmethod
    def get_sight() -> list:
        return GameState.threats['sight']

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

    @classmethod
    def is_king(cls, x, y) -> bool:
        if cls.is_piece(x, y) and cls.get(x,y).name == 'King':
            return True



class Util:
    
    @staticmethod
    def range2d():
        for x in range(8):
            for y in range(8):
                yield (x,y)

    @staticmethod
    def unique(pos_list) -> list:
        return list(set(pos_list))


if __name__ == '__main__':
    pass