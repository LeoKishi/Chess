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



class ImageCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.indicator = self.create_image(27, 27, anchor='center')
        self.image = self.create_image(27, 25, anchor='center')
        self.highlight = self.create_image(27, 27, anchor='center')
        


    def set_image(self, img):
        self.itemconfig(self.image, image=img)


    def set_highlight(self, img):
        self.itemconfig(self.highlight, image=img)


    def set_indicator(self, img):
        self.itemconfig(self.indicator, image=img)


    def set_color(self, color):
        self.config(bg=color)