import tkinter as tk
from image_loader import *
from game_state import GameState as game
from piece_behavior import *


class ChessBoard(tk.Tk):
    board_ui = [[None for x in range(8)] for y in range(8)]


    def __init__(self, player_color:str = 'White'):
        super().__init__()
        self.title('Chess')
        self.geometry('480x480')

        self.player = player_color
        self.highlights = list()
        self.indicators = list()
        self.hover = None
        self.is_dragging = False
        
        self.load_images()
        self.create_board()

        self.bind_functions()
        

    def load_images(self):
        self.lightbg_img = LightSquareImage()
        self.darkbg_img = DarkSquareImage()
        self.circle_img = CircleImage()
        self.dot_img = DotImage()
        self.indicator_img = IndicatorImage()
        self.hover_img = HoverImage()


    def create_board(self):
        self.canvas = tk.Canvas(self, height=480, width=480)
        self.canvas.pack()
        self.create_grid()
        self.populate_board()
        self.draw_squares()


    def bind_functions(self):
        self.bind('<ButtonPress-1>', lambda event: self.click_handler(event.y, event.x))
        self.bind('<ButtonRelease-1>', self.click_release)


    def click_handler(self, raw_x, raw_y):
        x, y = raw_x//60, raw_y//60

        if game.can_select(x, y) and game.color(x,y) == self.player:
            self.start_drag(x, y)

        elif game.selected == game.get(x,y):
            game.clear_selected()

        elif game.selected and game.is_same_color(x, y):
            if not self.stop_drag():
                self.start_drag(x, y)
            
        elif (x,y) in game.can_move():
            if game.process_action(x, y):
                self.draw_move()

        else:
            self.stop_drag()

        self.draw_elements()
        self.board_ui[x][y].raise_piece()


    def start_drag(self, x, y):
        game.select(x, y)
        self.is_dragging = True
        self.drag_piece(x, y)


    def stop_drag(self) -> bool:
        if self.is_dragging:
            self.is_dragging = False
            game.clear_selected()
            return True


    def click_release(self, event):
        if game.selected is None:
            return
        
        if game.selected.pos == self.get_mouse_pos(on_grid=True, invert=True):
            self.is_dragging = False
            self.draw_squares()
        else:
            self.click_handler(*self.get_mouse_pos(invert=True))


    def drag_piece(self, x, y):
        if self.is_dragging:
            self.board_ui[x][y].move(*self.get_mouse_pos())
            self.hover_highlight(*self.get_mouse_pos(on_grid=True, invert=True))
            self.after(1000//60, self.drag_piece, *(x, y))


    def hover_highlight(self, x, y):
        if self.hover == (x,y):
            return

        if self.hover:
            old_x, old_y = self.hover
            self.board_ui[old_x][old_y].set_hover('')

        self.hover = (x,y)
        self.board_ui[x][y].set_hover(self.hover_img)


    def draw_elements(self):
        if self.hover:
            x, y = self.hover
            self.board_ui[x][y].set_hover('')
            self.hover = None
        self.draw_squares()
        self.draw_highlight()
        self.draw_indicator()


    def draw_move(self):
        old_pos, new_pos = game.last_move
        new_x, new_y = new_pos
        old_x, old_y = old_pos
    
        self.board_ui[new_x][new_y].set_piece(game.get(*new_pos).image)
        self.board_ui[old_x][old_y].set_piece('')


    def draw_highlight(self):
        for x,y in self.highlights:
            self.board_ui[x][y].set_highlight('')

        if game.moves:
            for x,y in game.moves:
                self.board_ui[x][y].set_highlight(self.dot_img)
                self.highlights.append((x,y))

        if game.captures:
            for x,y in game.captures:
                self.board_ui[x][y].set_highlight(self.circle_img)
                self.highlights.append((x,y))


    def draw_indicator(self):
        for x,y in self.indicators:
            self.board_ui[x][y].set_indicator('')

        if game.last_move:
            for x,y in game.last_move:
                self.board_ui[x][y].set_indicator(self.indicator_img)
                self.indicators.append((x,y))


    def create_grid(self):
        for x in range(8):
            for y in range(8):
                self.board_ui[x][y] = Square(self.canvas)
                

    def draw_squares(self):
        for x in range(8):
            for y in range(8):
                piece = game.get(x,y)
                self.board_ui[x][y].set_piece('' if piece is None else piece.image)
                self.board_ui[x][y].place(x*60, y*60)


    def populate_board(self):
        player1 = self.player
        player2 = 'Black' if player1 == 'White' else 'White'
        self.set_board_color(player1)

        def new_piece(piece_type, color, pos):
            game.board[pos[0]][pos[1]] = piece_type(color, pos)

        for y in range(8):
            new_piece(Pawn, player2, (1,y))
            new_piece(Pawn, player1, (6,y))

        new_piece(Pawn, player2, (5,2))

        new_piece(Rook, player2, (0,0))
        new_piece(Rook, player2, (0,7))
        new_piece(Rook, player1, (7,0))
        new_piece(Rook, player1, (7,7))

        new_piece(Knight, player2, (0,1))
        new_piece(Knight, player2, (0,6))
        new_piece(Knight, player1, (7,1))
        new_piece(Knight, player1, (7,6))

        new_piece(Bishop, player2, (0,2))
        new_piece(Bishop, player2, (0,5))
        new_piece(Bishop, player1, (7,2))
        new_piece(Bishop, player1, (7,5))

        offset = 1 if player1 == 'Black' else 0

        new_piece(Queen, player2, (0,3+offset))
        new_piece(Queen, player1, (7,3+offset))

        new_piece(King, player2, (0,4-offset))
        new_piece(King, player1, (7,4-offset))
        

    def set_board_color(self, player1):
        offset = 1 if player1 == 'White' else 0

        for x in range(8):
            for y in range(8):
                if (x+y+offset) % 2 == 0:
                    self.board_ui[x][y].set_bg(self.lightbg_img)
                else:
                    self.board_ui[x][y].set_bg(self.darkbg_img)


    def get_mouse_pos(self, on_grid=False, invert=False) -> tuple:
        x = self.winfo_pointerx() - self.winfo_rootx()
        y = self.winfo_pointery() - self.winfo_rooty()

        if on_grid:
            x, y = self.clamp(x//60, 0, 7), self.clamp(y//60, 0, 7)
        else:
            x, y = self.clamp(x, 0, 479), self.clamp(y, 0, 479)
        
        if invert:
            return (y, x)

        return (x, y)
    

    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)