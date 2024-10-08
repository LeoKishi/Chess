import tkinter as tk


class DragFrame(tk.Frame):
    def __init__(self, parent, *, drag:bool = True, **kwargs):
        '''Tkinter Frame with drag and drop functionality'''

        super().__init__(parent, **kwargs)
        self._parent = parent
        self._dragging = False
        self._offset = list()
        self._enabled = drag
        self.bind('<Button-1>', self._start_drag, add=True)
        self.bind('<ButtonRelease-1>', self._stop_drag, add=True)


    def bind_children_widgets(self):
        for i in self.winfo_children():
            i.bindtags((self,) + i.bindtags())


    def status(self) -> bool:
        return self._enabled


    def drag(self, status:bool):
        if status:
            self._enabled = True
        else:
            self._enabled = False


    def get_pos(self) -> tuple:
        x_center = self.winfo_x() + self.winfo_width()/2
        y_center = self.winfo_y() + self.winfo_height()/2
        return (x_center, y_center)


    def _start_drag(self, event):
        if self._enabled:
            self._offset = self._get_offset()
            self._dragging = True
            self._clock()
    

    def _stop_drag(self, event):
        if self._enabled:
            self._dragging = False


    def _clock(self):
        if self._dragging:
            self._draw()
            self.after(1000//60, self._clock)


    def _draw(self):
        x, y = self._check_border()
        self.place(x=x, y=y, anchor='center')


    def _check_border(self) -> tuple:
        height, width = self._parent.winfo_height(), self._parent.winfo_width()
        x_mouse, y_mouse = self._get_mouse_pos()
        x_edge, y_edge = self.winfo_width()//2, self.winfo_height()//2
        x_offset, y_offset = self._offset

        if (x_mouse - x_edge - x_offset) < 0:
            x_mouse = x_edge + x_offset
        elif (x_mouse + x_edge - x_offset) > width:
            x_mouse = width - x_edge + x_offset
        
        if (y_mouse - y_edge - y_offset) < 0:
            y_mouse = y_edge + y_offset
        elif (y_mouse + y_edge - y_offset) > height:
            y_mouse = height - y_edge + y_offset

        return (x_mouse-x_offset, y_mouse-y_offset)


    def _get_mouse_pos(self) -> tuple:
        x = self.winfo_pointerx() - self._parent.winfo_rootx()
        y = self.winfo_pointery() - self._parent.winfo_rooty()
        return (x, y)


    def _get_offset(self) -> tuple:
        x, y = self._get_mouse_pos()
        x_center, y_center = self.get_pos()
        return (x-x_center, y-y_center)