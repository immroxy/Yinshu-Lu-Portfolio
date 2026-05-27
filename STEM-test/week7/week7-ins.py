import cv2
import numpy as np
from dorothy import Dorothy

dot = Dorothy()

class MySketch:
    
    def __init__(self):
        dot.start_loop(self.setup, self.draw)  

    def setup(self):
        print("setup")
        self.camera = cv2.VideoCapture(0)
        self.face_cascade=cv2.CascadeClassifier("week7/data/haarcascade_frontalface_default.xml")
        self.nose_image=cv2.imread("week7/images/Kitty3.png",cv2.IMREAD_UNCHANGED)
    
    def instagram_effects(self, image):
        #Blur effect
        image=cv2.GaussianBlur(image,(11, 11),0)
        #Adjust the tone and contrast
        image=cv2.convertScaleAbs(image,alpha=1.5,beta=10)
        #Adjusted saturation
        hsv=cv2.cvtColor(image,cv2.COLOR_RGB2HSV)
        hsv[...,1]=hsv[...,1]*1.5
        image=cv2.cvtColor(hsv,cv2.COLOR_HSV2RGB)
        #Increase brightness
        image=cv2.convertScaleAbs(image,alpha=1,beta=30)
        return image


    def overlay(self, background, overlay, x, y):
        #Adjust according to the size of the image
        height,width = overlay.shape[:2]
        if y + height> background.shape[0] or x + width > background.shape[1]:
            return background
        
        #Get Alpha channel
        alpha_channel=overlay[:,:,3]/255.0
        alpha_background=1.0-alpha_channel
        for c in range(0, 3):
            background[y:y+height,x:x+width,c]=(alpha_channel*overlay[:,:,c]+alpha_background*background[y:y+height,x:x+width,c])
        return background

    def draw(self):
        success, camera_feed = self.camera.read()
        if success:
            camera_feed = cv2.resize(camera_feed,(dot.width, dot.height))
            camera_feed = cv2.cvtColor(camera_feed, cv2.COLOR_BGR2RGB)
            camera_feed_grayscale = cv2.cvtColor(camera_feed, cv2.COLOR_RGB2GRAY)
            faces = self.face_cascade.detectMultiScale(camera_feed_grayscale, 1.1, 4)

            for face_x, face_y, face_w, face_h in faces:
                #Locate the bridge of the nose
                nose_x=face_x+face_w//2
                nose_y=face_y+face_h//4
                nose_width=face_w//2
                nose_height=int(nose_width * self.nose_image.shape[0] / self.nose_image.shape[1])
                resized_nose_image = cv2.resize(self.nose_image, (nose_width, nose_height))

                if resized_nose_image.shape[2] == 4:
                    #Extract RGB and Alpha channels
                    RGB_nose = resized_nose_image[:, :, :3]
                    Alpha_nose = resized_nose_image[:, :, 3]
                    RGB_nose = cv2.cvtColor(RGB_nose, cv2.COLOR_BGR2RGB)
                    resized_nose_image_with_alpha = np.dstack([RGB_nose, Alpha_nose])
                else:
                    resized_nose_image_with_alpha = resized_nose_image

                #Synthesize the image onto the camera frame
                camera_feed = self.overlay(camera_feed, resized_nose_image_with_alpha, nose_x - nose_width // 2, nose_y)
            
            camera_feed = self.instagram_effects(camera_feed)
            dot.canvas = camera_feed

MySketch()
