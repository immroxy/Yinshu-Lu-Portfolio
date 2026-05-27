from dorothy import Dorothy
from cv2 import circle, line
from PIL import Image
import numpy as np
import random

dot = Dorothy()

class MySketch:
    def __init__(self):
        self.line_style = 1
        dot.start_loop(self.setup, self.draw)

    def setup(self):
        #Import the audio
        file_path = "week5/audio/SSP_TOS_75_guitar_electric_vows_Amaj.wav"
        dot.music.start_file_stream(file_path, fft_size=512, buffer_size=512)
        #Import the image
        self.image = Image.open('week5/1.png')

    def draw(self):
        dot.background(dot.black)
        layer = dot.get_layer()

        #Plot audio spectrum
        for bin_num, bin_val in enumerate(dot.music.fft()[:256]):
            pt1 = (bin_num*5, dot.height)
            pt2 = (bin_num*5, dot.height-int(bin_val*200))

            #Random color generation
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            #Draw according to different styles
            if self.line_style == 1:
                line(dot.canvas,pt1,pt2,color,2)
            elif self.line_style == 2:
                circle(dot.canvas,pt2,2,color,-1)
        
        #Get the mouse position and paste the image to the mouse position
        layer = Image.fromarray(layer)
        image_x, image_y = dot.mouse_x, dot.mouse_y
        layer.paste(self.image, (image_x-self.image.width//2, image_y - self.image.height// 2), self.image)
        layer = np.array(layer)
        dot.draw_layer(layer)

MySketch()


