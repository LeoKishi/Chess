from tkinter import Canvas, PhotoImage


class CircleImage(PhotoImage):
    def __init__(self, file='assets/circle.png'):
        super().__init__(file=file)


class DotImage(PhotoImage):
    def __init__(self, file='assets/dot.png'):
        super().__init__(file=file)


class IndicatorImage(PhotoImage):
    def __init__(self, file='assets/indicator.png'):
        super().__init__(file=file)


class LightSquareImage(PhotoImage):
    def __init__(self, file='assets/light_square.png'):
        super().__init__(file=file)


class DarkSquareImage(PhotoImage):
    def __init__(self, file='assets/dark_square.png'):
        super().__init__(file=file)


class HoverImage(PhotoImage):
    def __init__(self, file='assets/hover.png'):
        super().__init__(file=file)


class Square:
    def __init__(self, canvas):
        self.canvas = canvas

        def new_image():
            return canvas.create_image(60, 60, anchor='nw')

        self.bg = new_image()
        self.highlight = new_image()
        self.hover = new_image()
        self.piece = new_image()
        self.indicator = new_image()

        self.elements = [self.bg,
                         self.highlight,
                         self.indicator,
                         self.hover,
                         self.piece]
        


    def move(self, mouse_x, mouse_y):
        self.canvas.moveto(self.piece, mouse_x-30, mouse_y-30)

        
    def raise_piece(self):
        self.canvas.tag_raise(self.piece)


    def place(self, x, y):
        for elem in self.elements:
            self.canvas.moveto(elem, y, x)

    
    def set_bg(self, img):
        self.canvas.itemconfig(self.bg, image=img)


    def set_highlight(self, img):
        self.canvas.itemconfig(self.highlight, image=img)
        self.canvas.tag_raise(self.highlight)

    def set_indicator(self, img):
        self.canvas.itemconfig(self.indicator, image=img)


    def set_hover(self, img):
        self.canvas.itemconfig(self.hover, image=img)


    def set_piece(self, img):
        self.canvas.itemconfig(self.piece, image=img)

