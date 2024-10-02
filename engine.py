from stockfish import Stockfish


class Engine:
    stockfish = Stockfish(path="stockfish-windows-x86-64-sse41-popcnt.exe")
    stockfish.update_engine_parameters({'Threads':2})
    stockfish.set_elo_rating(1400)
    #stockfish.set_depth(25)
    moves = list()

    @classmethod
    def new_move(cls, move):
        cls.moves.append(move)
        cls.stockfish.set_position(cls.moves)

    @classmethod
    def generate_move(cls) -> str:
       move = cls.stockfish.get_best_move()
       print(move)
       return move



if __name__ == '__main__':
    Engine.stockfish.set_skill_level(10)

    pass