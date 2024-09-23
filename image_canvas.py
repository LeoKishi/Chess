from tkinter import Canvas, Label, PhotoImage


class BlankImage(PhotoImage):
    def __init__(self, file='assets/empty.png'):
        super().__init__(file=file)


class ImageCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.image = self.create_image(35, 35, anchor='center')


    def set_image(self, img):
        self.itemconfig(self.image, image=img)


    def set_color(self, color):
        self.config(bg=color)