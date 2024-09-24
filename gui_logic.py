from game_state import GameState as game



class Drag:
    hover = None
    is_dragging = False

    @staticmethod
    def loop(root, x, y):
        if Drag.is_dragging:
            root.board_ui[x][y].move(*Util.get_mouse_pos(root))
            Drag.hover_highlight(root, *Util.get_mouse_pos(root, on_grid=True, invert=True))
            root.after(1000//60, Drag.loop, *(root, x, y))

    @staticmethod
    def start_drag(root, x, y):
        game.select(x, y)
        Drag.is_dragging = True
        Drag.loop(root, x, y)

    @staticmethod
    def stop_drag(root) -> bool:
        if Drag.is_dragging:
            Drag.is_dragging = False
            game.clear_selected()
            return True
    
    @staticmethod
    def hover_highlight(root, x, y):
        if Drag.hover == (x,y):
            return

        if Drag.hover:
            old_x, old_y = Drag.hover
            root.board_ui[old_x][old_y].set_hover('')

        Drag.hover = (x,y)
        root.board_ui[x][y].set_hover(root.hover_img)




class Draw:
    highlights = list()
    indicators = list()

    @staticmethod
    def draw_pieces(root):
        for x in range(8):
            for y in range(8):
                piece = game.get(x,y)
                root.board_ui[x][y].set_piece('' if piece is None else piece.image)
                root.board_ui[x][y].place(x*60, y*60)

    @staticmethod
    def draw_indicator(root):
        for x,y in Draw.indicators:
            root.board_ui[x][y].set_indicator('')

        if game.last_move:
            for x,y in game.last_move:
                root.board_ui[x][y].set_indicator(root.indicator_img)
                Draw.indicators.append((x,y))

    @staticmethod
    def draw_highlight(root):
        for x,y in Draw.highlights:
            root.board_ui[x][y].set_highlight('')

        if game.moves:
            for x,y in game.moves:
                root.board_ui[x][y].set_highlight(root.dot_img)
                Draw.highlights.append((x,y))

        if game.captures:
            for x,y in game.captures:
                root.board_ui[x][y].set_highlight(root.circle_img)
                Draw.highlights.append((x,y))

    @staticmethod
    def draw_last_move(root):
        old_pos, new_pos = game.last_move
        new_x, new_y = new_pos
        old_x, old_y = old_pos
    
        root.board_ui[new_x][new_y].set_piece(game.get(*new_pos).image)
        root.board_ui[old_x][old_y].set_piece('')

    @staticmethod
    def draw_elements(root):
        if Drag.hover:
            x, y = Drag.hover
            root.board_ui[x][y].set_hover('')
            Drag.hover = None
        Draw.draw_pieces(root)
        Draw.draw_highlight(root)
        Draw.draw_indicator(root)



class Util:

    @staticmethod
    def get_mouse_pos(root, on_grid=False, invert=False) -> tuple:
        x = root.canvas.winfo_pointerx() - root.canvas.winfo_rootx()
        y = root.canvas.winfo_pointery() - root.canvas.winfo_rooty()

        def clamp(n, minn, maxn):
            return max(min(maxn, n), minn)

        if on_grid:
            x, y = clamp(x//60, 0, 7), clamp(y//60, 0, 7)
        else:
            x, y = clamp(x, 0, 479), clamp(y, 0, 479)
        
        if invert:
            return (y, x)

        return (x, y)