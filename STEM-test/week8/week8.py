from cv2 import rectangle
from dorothy import Dorothy
import numpy as np

dot = Dorothy()

class MySketch:

    thumbnail_size = (100,100)
    #Importing playing card images
    dataset = dot.get_images("week8/PNG", thumbnail_size)

    def __init__(self):
        dot.start_loop(self.setup, self.draw)  

    def setup(self):
        print("setup")
        #Add audio
        music_path = "week8/audio/SO_CT_100_songstarter_tusbesos_Cmin.wav"
        dot.music.start_file_stream(music_path)

    def draw(self):
        #Set the background to green 
        dot.background((0,128,0))
        #Drawing 54 faces
        num_faces = 54
        for i in range(num_faces):
            new_canvas = dot.get_layer()
            index = np.random.randint(len(self.dataset))
            to_paste = self.dataset[index]
            #Setting the initial position
            coords = (100,50)
            dot.paste(new_canvas, to_paste, coords)
            #How quickly to change?
            period = 25
            #Where are we in the cycle?
            factor = (dot.frame%period)/period
            #Get angle and factor in place in list (i)
            theta = (factor * (i/num_faces)) * 5 * np.pi 
            rotate = np.array([[np.cos(theta), -np.sin(theta)],
                            [np.sin(theta), np.cos(theta)]])
            
            #linear transform
            origin = (dot.width//2,dot.height//2)
            new_canvas = dot.transform(new_canvas, rotate, origin)
            #push it back onto layer stack
            dot.draw_layer(new_canvas)
        
MySketch()
