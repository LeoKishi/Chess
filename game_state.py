
# TODO:
# start menu
# end menu
# play sounds for piece movement, capture, check and checkmate

# ====== extra ======
# timer
# stockfish bot


class GameState:
    board = [[None for row in range(8)] for col in range(8)]
    player = None
    selected = None
    moves = None
    captures = None
    last_move = None
    last_capture = None
    castle = None
    check = False
    check_mate = False
    en_passant = list()
    turn = 'White'
    threats = {'attack':list(),
               'checking':list(),
               'sight':list(),
               'w_pinned':list(),
               'b_pinned':list()}


    @classmethod
    def process_action(cls, x, y) -> bool:
        old_pos = cls.selected.pos
        cls.register_last_move(cls.selected, (x,y))
        cls.register_move(cls.selected, (x,y))

        if Info.is_in_check():
            cls.undo_register_move(x,y,old_pos)
            return False

        if Info.is_pinned(x, y, old_pos):
            cls.undo_register_move(x,y,old_pos)
            return False

        # check pawn promotion


        cls.register_castle(x,y,old_pos)
        cls.register_en_passant(x, y)
        cls.register_threats(x,y)
        if cls.try_check_mate():
            print('check mate')
            cls.check_mate = True
        cls.first_move_status(x,y)
        cls.new_turn()
        cls.clear_selected()
        return True

    @classmethod
    def undo_register_move(cls, x, y, old_pos):
        cls.register_move(cls.selected, old_pos)
        cls.clear_selected()
        if cls.last_capture:
            cls.register_move(cls.last_capture, (x,y))
        # BLINK KING TO SIGNAL CHECK OR PIN
        print('in check or pinned')

    @classmethod
    def register_last_move(cls, piece, new_pos:list|tuple):
        cls.last_piece = piece
        cls.last_move = (piece.pos, new_pos)
        cls.last_capture = Info.get(*new_pos)

    @classmethod
    def register_en_passant(cls, x, y):
        if cls.en_passant and (x,y) == cls.en_passant[-1] and Info.name(x,y,'Pawn'):
            if cls.selected.color == cls.player:
                cls.board[x+1][y] = None
            else:
                cls.board[x-1][y] = None
            cls.en_passant = list()
            print('en passant')

    @classmethod
    def register_castle(cls, x, y, old_pos):
        if Info.is_king(*cls.selected.pos):
            if (x,y) in cls.castle:
                cls.register_move(cls.selected, old_pos)
                if y < 4:
                    cls.register_move(Info.get(x,0), (x,3))
                    cls.register_move(cls.selected, (x,2))
                if y > 4:
                    cls.register_move(Info.get(x,7), (x,5))
                    cls.register_move(cls.selected, (x,6))

    @classmethod
    def clear_selected(cls):
        cls.selected = None
        cls.moves = None
        cls.captures = None

    @classmethod
    def select(cls, x, y):
        if Info.is_piece(x, y):
            cls.selected = Info.get(x,y)
            cls.register_possible_actions(x, y)

    @classmethod
    def register_move(cls, piece, new_pos:list|tuple):
        old_x, old_y = piece.pos
        new_x, new_y = new_pos
        piece.pos = new_pos
        cls.board[old_x][old_y] = None
        cls.board[new_x][new_y] = piece

    @classmethod
    def first_move_status(cls, x, y):
        piece = Info.get(x,y)
        if piece.name in ('Pawn', 'Rook', 'King'):
            piece.first_move = False
        if piece.name == 'Pawn' and x in {3, 4}:
            cls.en_passant = Find.find_en_passant(x, y)

    @classmethod
    def new_turn(cls):
        if cls.turn == 'White':
            cls.turn = 'Black'
        else:
            cls.turn = 'White'

    @classmethod
    def register_threats(cls, x, y):
        attack, checking, sight = Find.find_checks(Info.get(x,y))
        b_pinned, w_pinned = Find.find_all_pins()
        GameState.check = True if checking else False
        GameState.threats = {'attack':attack,
                             'checking':checking,
                             'sight':sight,
                             'w_pinned':w_pinned,
                             'b_pinned':b_pinned}

    @classmethod
    def try_check_mate(cls) -> bool:
        if not cls.check:
            return False

        can_move = True
        can_defend = False
        for x,y in Util.range2d():
            if not Info.is_enemy(cls.selected, (x,y)):
                continue

            if Info.is_king(x,y) and not Info.get(x,y).can_move():
                can_move = False
                continue

            for i in Info.get(x,y).can_move() + Info.get(x,y).can_capture():
                if i in Info.get_sight():
                    can_defend = True
                    return False

        if not can_move and not can_defend:
            return True

    @classmethod
    def set_player(cls, color):
        cls.player = color

    @classmethod
    def register_possible_actions(cls, x, y):
        GameState.moves = Info.get(x,y).can_move()
        GameState.captures = Info.get(x,y).can_capture()
        if Info.is_king(x, y):
            GameState.castle = Find.find_castle((x, y))
            GameState.moves += GameState.castle
        if Info.name(x, y, 'Pawn') and (x,y) in cls.en_passant:
            GameState.moves.append(cls.en_passant[-1])




class Find:

    @staticmethod
    def find_en_passant(x, y) -> list:
        side = list()
        for i in range(-1, 2, 2):
            if Info.name(x, y+i, 'Pawn') and Info.is_enemy(Info.get(x,y+i), (x,y)):
                side.append((x, y+i))
        if Info.color(x,y) == GameState.player:
            side.append((x+1, y))
        else:
            side.append((x-1, y))
        return side

    @staticmethod
    def find_castle(king_pos) -> list:
        x, y = king_pos
        right, left = [], []
        if not GameState.check:
            if not Info.is_castle_blocked(king_pos, Info.line_to_rook(king_pos,'right')):
                right = [(x, y+2)]
            if not Info.is_castle_blocked(king_pos, Info.line_to_rook(king_pos,'left')):
                left = [(x, y-2)]
        return right + left

    @classmethod
    def find_all_pins(cls) -> tuple:
        b_pinned = list()
        w_pinned = list()
        for x,y in Util.range2d():
            if not Info.is_piece(x,y):
                continue

            if Info.color(x,y) == 'White':
                b_pinned += Info.get(x,y).is_pinning()
            else:
                w_pinned += Info.get(x,y).is_pinning()

        return (b_pinned, w_pinned)

    @classmethod
    def find_pin(cls, piece, direction) -> list:
        x, y = piece.pos
        mod_x, mod_y = direction
        line = list()
        pinned = None

        while True:
            x += mod_x
            y += mod_y
            if not Info.is_inside(x,y):
                break
            line.append((x,y))

        for i in line:
            if not pinned and Info.is_piece(*i):
                pinned = i
            elif Info.is_enemy(piece, i):
                if Info.is_king(*i):
                    line.pop()
                    return [pinned, line]
                break
        return []

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




class Info:

    @staticmethod
    def is_pinned(x, y, old_pos) -> bool:
        color = Info.color(x,y)
        if old_pos in GameState.threats['w_pinned' if color == 'White' else 'b_pinned']:
            if not (x,y) in GameState.threats['b_pinned' if color == 'White' else 'w_pinned']:
                if (x,y) in GameState.threats['w_pinned' if color == 'White' else 'b_pinned'][1]:
                    return False
                else:
                    return True

    @classmethod
    def is_castle_blocked(cls, king_pos, line) -> bool:
        if not (Info.get(*king_pos).first_move):
            return True
        if not (Info.name(*line[-1], 'Rook')):
            return True
        if Info.get(*line.pop()).first_move:
            for i in line:
                if not (Info.is_empty(*i) and i not in Info.get_attacks()):
                    return True
        
    @classmethod
    def line_to_rook(cls, king_pos, side) -> list:
        x, y = king_pos
        mod = 1 if side == 'right' else -1
        line = list()
        i = 1
        while Info.is_inside(x, y+i*mod):
            line.append((x, y+i*mod))
            i += 1
        return line

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

    @staticmethod
    def get_player() -> str:
        return GameState.player

    @classmethod
    def name(cls, x, y, name) -> bool:
        return cls.is_piece(x, y) and cls.get(x, y).name == name

    @classmethod
    def get_king(cls, color) -> object:
        for x,y in Util.range2d():
            if cls.is_king(x,y) and cls.color(x,y) == color:
                return cls.get(x,y)



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