import tkinter as tk
from sprite_loader import SpriteSheet


class test(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('500x500')
        self.title('test')

        self.canvas = tk.Canvas(height=500, width=500, bg='pink')
        self.canvas.pack()

        self.a = Selector(self.canvas, 'White')
        self.a.place(150,340)






class Selector:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.color = color
        self.load_image(color)

        self.selector = self.new_image(self.selector_img)
        self.hover = self.new_image(self.hover_img)
        self.exit = self.new_image(self.exit_img)
        self.queen = self.new_image(self.w_queen)
        self.knight = self.new_image(self.w_knight)
        self.rook = self.new_image(self.w_rook)
        self.bishop = self.new_image(self.w_bishop)

        self.elements = [self.queen, self.knight, self.rook, self.bishop, self.exit]
        
        if color == 'Black':
            self.elements = self.elements[::-1]
        
        self.bind_events()

    def place(self, x, y):
        offset = 0
        self.canvas.moveto(self.selector, y-6, x-6)
        for elem in self.elements:
            self.canvas.moveto(elem, y, x+offset)
            if elem == 3 and self.color == 'Black':
                offset += 30
                continue
            offset += 60
        self.show()
    
    def load_image(self, color):
        loader = SpriteSheet(file='assets/ChessPiecesArray.png')
        row = 1 if color == 'White' else 0
        self.w_queen = loader.get_sprite((60,60), (row,0))
        self.w_knight = loader.get_sprite((60,60), (row,3))
        self.w_rook = loader.get_sprite((60,60), (row,2))
        self.w_bishop = loader.get_sprite((60,60), (row,4))
        self.selector_img = tk.PhotoImage(file='assets/selector.png')
        self.exit_img = tk.PhotoImage(file='assets/exit.png')
        self.hover_img = tk.PhotoImage(file='assets/selector_hover.png')
        self.hover_exit_img = tk.PhotoImage(file='assets/selector_exit_hover.png')

    def new_image(self, img):
        return self.canvas.create_image(0, 0, anchor='nw', image=img, state='hidden')

    def bind_events(self):
        for i in self.elements:
            self.canvas.tag_bind(i, '<Enter>', lambda event, i=i: self.show_hover(i))
            self.canvas.tag_bind(i, '<ButtonPress-1>', lambda event, i=i: self.action(i))

    def show_hover(self, elem):
        x, y = self.canvas.coords(elem)
        if elem == 3:
            self.canvas.itemconfigure(2, state='hidden')
            return
        self.canvas.moveto(self.hover, x, y)
        self.canvas.itemconfigure(2, state='normal')

    def action(self, option):
        if option == 3:
            self.hide()
            return
        print(option-4)

    def hide(self):
        for i in range(8):
            self.canvas.itemconfigure(i+1, state='hidden')

    def show(self):
        for i in self.elements + [1]:
            self.canvas.itemconfigure(i, state='normal')

test().mainloop()