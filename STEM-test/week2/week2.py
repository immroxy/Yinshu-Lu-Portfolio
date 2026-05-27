from dorothy import Dorothy
from cv2 import imread, resize

dot = Dorothy()

class MySketch:
    def __init__(self):
        self.image1 = self.load_and_resize("week2/images/CookieAnn.png")
        self.image2 = self.load_and_resize("week2/images/StellaLou.png")
        self.image3 = self.load_and_resize("week2/images/Olu Mel.png")
        self.image4 = self.load_and_resize("week2/images/LinaBell.png")
        self.highlight_image = self.load_and_resize("week2/images/choose.png")
        dot.start_loop(self.setup, self.draw)

    def load_and_resize(self, path):
        image = imread(path)
        if image is None:
            raise FileNotFoundError(f"Error: File '{path}' not found.")
        return resize(image,(dot.width//2, dot.height//2))

    def setup(self):
        pass

    def draw(self):
        dot.background(dot.white)
        #Top left
        if dot.mouse_x < dot.width//2 and dot.mouse_y < dot.height//2:
            dot.canvas[:self.highlight_image.shape[0], :self.highlight_image.shape[1]] = self.highlight_image
        else:
            dot.canvas[:self.image1.shape[0], :self.image1.shape[1]] = self.image1
        #Bottom left
        if dot.mouse_x < dot.width//2 and dot.mouse_y > dot.height//2:
            dot.canvas[dot.height//2:dot.height, :self.highlight_image.shape[1]] = self.highlight_image
        else:
            dot.canvas[dot.height//2:dot.height, :self.image2.shape[1]] = self.image2
        #Top Right
        if dot.mouse_x > dot.width//2 and dot.mouse_y < dot.height//2:
            dot.canvas[:self.highlight_image.shape[0], dot.width//2:] = self.highlight_image
        else:
            dot.canvas[:self.image3.shape[0], dot.width//2:] = self.image3
        #Bottom Right
        if dot.mouse_x > dot.width//2 and dot.mouse_y > dot.height//2:
            dot.canvas[dot.height//2:, dot.width//2:] = self.highlight_image
        else:
            dot.canvas[dot.height//2:, dot.width//2:] = self.image4

MySketch()
