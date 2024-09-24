import tkinter as tk
from SpriteLoader import SpriteSheet


class test(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.geometry('480x480')
        self.canvas = tk.Canvas(self, height=480, width=480, bg='pink')
        self.canvas.pack()

        self.grid = [[None for x in range(8)] for y in range(8)]
        self.piece_img = tk.PhotoImage(file='assets/white/w_queen.png')
        self.highlight_img = tk.PhotoImage(file='assets/circle.png')
        self.lightbg_img = tk.PhotoImage(file='assets/light_square.png')
        self.darkbg_img = tk.PhotoImage(file='assets/dark_square.png')

        self.load_images()

        self.draw_grid()


    def load_images(self):
        loader = SpriteSheet(file='assets/ChessPiecesArray.png')
        self.queen = loader.get_sprite((60,60), (1,2))



    def draw_grid(self):
        for x in range(8):
            for y in range(8):
                self.grid[x][y] = Square(self.canvas)
                self.grid[x][y].place(x*60, y*60)
                self.grid[x][y].set_piece(self.queen)
                self.grid[x][y].set_highlight(self.highlight_img)


                if (x+y) % 2 == 0:
                    self.grid[x][y].set_bg(self.lightbg_img)
                else:
                    self.grid[x][y].set_bg(self.darkbg_img)

                


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


    def place(self, x, y):
        for elem in self.elements:
            self.canvas.moveto(elem, x, y)


    
    def set_bg(self, img):
        self.canvas.itemconfig(self.bg, image=img)


    def set_highlight(self, img):
        self.canvas.itemconfig(self.highlight, image=img)


    def set_indicator(self, img):
        self.canvas.itemconfig(self.indicator, image=img)


    def set_hover(self, img):
        self.canvas.itemconfig(self.hover, image=img)


    def set_piece(self, img):
        self.canvas.itemconfig(self.piece, image=img)


test().mainloop()