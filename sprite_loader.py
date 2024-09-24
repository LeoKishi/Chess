from PIL import ImageTk, Image


class SpriteSheet:
    def __init__(self, file:str):
        self.img = Image.open(file)


    def get_sprite(self, size:tuple[int, int], position:tuple[int, int]) -> ImageTk.PhotoImage:
        '''
        Returns the sprite at the specified position as a PhotoImage instance.\n
        Parameters:
            size
                tuple containing the height and width of the sprite in pixels
            position
                tuple containing the position (x,y) of the sprite in the spritesheet grid
        '''
        height, width = size[0], size[1]
        row, column = position[0], position[1]

        left = width * column
        top = height * row
        right = left + width
        bottom = top + height

        cropped_image = self.img.crop((left, top, right, bottom))
        return ImageTk.PhotoImage(cropped_image)
