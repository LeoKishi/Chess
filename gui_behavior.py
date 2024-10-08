from game_state import GameState as game
from game_state import Info
from game_state import Util


class Command:

    @staticmethod
    def try_process(root, x, y) -> bool:
        if game.process_action(x, y):
            Draw.draw_last_move(root)
            Draw.draw_indicator(root)
            root.board_ui[x][y].raise_piece()
            if game.check_mate:
                Draw.draw_elements(root)
                root.unbind_functions()
                return True
        else:
            Draw.undo_draw_last_move(root)




class Drag:
    hover = None
    is_dragging = False

    @staticmethod
    def loop(root, x, y):
        if Drag.is_dragging:
            root.board_ui[x][y].move(*Mouse.get_mouse_pos(root))
            Drag.hover_highlight(root, *Mouse.get_mouse_pos(root, on_grid=True, invert=True))
            root.after(1000//60, Drag.loop, *(root, x, y))

    @staticmethod
    def start_drag(root, x, y):
        game.select(x, y)
        Drag.is_dragging = True
        Drag.loop(root, x, y)

    @staticmethod
    def stop_drag() -> bool:
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
    attacks = list()

    @staticmethod
    def draw_selector(root, x, y):
        Draw.draw_elements(root)

        if Info.color(*game.selected.pos) == game.player:
            selector = root.w_selector if game.player == 'White' else root.b_selector
            offset = 0
        else:
            selector = root.b_selector if game.player == 'White' else root.w_selector
            offset = 3

        selector.place(x-offset, y)
        selector.set_pos(x, y)
        root.unbind_functions()

    @staticmethod
    def draw_pieces(root):
        for x, y in Util.range2d():
            piece = Info.get(x,y)
            root.board_ui[x][y].set_piece('' if piece is None else piece.image)
            root.board_ui[x][y].place((x*60)+4, (y*60)+4)

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
        root.board_ui[new_x][new_y].set_piece(Info.get(*new_pos).image)
        root.board_ui[old_x][old_y].set_piece('')

    @staticmethod
    def undo_draw_last_move(root):
        old_pos, new_pos = game.last_move
        new_x, new_y = new_pos
        old_x, old_y = old_pos
        root.board_ui[old_x][old_y].set_piece(Info.get(*old_pos).image)
        root.board_ui[new_x][new_y].set_piece('')

    @staticmethod
    def draw_elements(root):
        if Drag.hover:
            x, y = Drag.hover
            root.board_ui[x][y].set_hover('')
            Drag.hover = None
        Draw.draw_pieces(root)
        Draw.draw_highlight(root)

    @staticmethod
    def reset_lists():
        Draw.highlights = list()
        Draw.indicators = list()




class Mouse:

    @staticmethod
    def get_mouse_pos(root, on_grid=False, invert=False) -> tuple:
        x = root.canvas.winfo_pointerx() - root.canvas.winfo_rootx()
        y = root.canvas.winfo_pointery() - root.canvas.winfo_rooty()

        def clamp(n, minn, maxn):
            return max(min(maxn, n), minn)

        if on_grid:
            x, y = clamp((x-4)//60, 0, 7), clamp((y-4)//60, 0, 7)
        else:
            x, y = clamp(x, 4, 483), clamp(y, 4, 483)
        
        if invert:
            return (y, x)

        return (x, y)

    @staticmethod
    def is_in_bounds(x, y):
        return 4 <= x < 484 and 4 <= y < 484