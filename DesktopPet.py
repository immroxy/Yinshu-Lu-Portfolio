import cv2
import pygame
import tkinter as tk
import mediapipe as mp
import numpy as np
import threading
import time
import random

class DesktopPet:
    # Constructor that gets called when initialised
    def __init__(self):
        # Perform initial setup
        self.window = None
        self.canvas = None
        self.pet_size = 100

        # Add 5 different colours to pet
        self.colors = ["#F8EFD3", "#FF69B4", "#87CEEB", "#FF4500", "#9370DB"]
        # Current pet colour
        self.current_color_index = 0
        self.screen_width = 0
        self.screen_height = 0

        # Set initial mood happy
        self.current_mood = 0

        # Tests revealed that the sound effect would be triggered continuously, so a cooldown was set for the sound effect
        self.last_effect_time = 0
        self.effect_cooldown = 1.0

        # Set gesture recognition
        self.mp_hands = mp.solutions.hands
        # Maximum number of hands is 1
        self.hands = self.mp_hands.Hands(max_num_hands=1,min_detection_confidence=0.7,min_tracking_confidence=0.5)

        # Set up the interface and camera
        self.init_window()
        self.init_pet()
        self.init_audio()
        # Create a thread to process camera input
        self.camera_thread = threading.Thread(target=self.process_camera)
        # Set up threads
        self.camera_thread.daemon=True
        self.camera_thread.start()
        self.window.mainloop()

    def init_window(self):
        # Borderless windows created for an immersive experience
        self.window = tk.Tk()
        self.window.overrideredirect(True)
        # To make it easier to put the window on top so that the pet is always on the screen
        self.window.attributes('-topmost', 1)
        # Get screen size
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        # Set window background to transparent colour
        self.window.config(background="white")
        # Set the window transparency colour so that all parts of the window with a white background will be transparent
        self.window.wm_attributes("-transparentcolor", "white")
    
        # Create Canvas
        self.canvas = tk.Canvas(self.window,width=self.pet_size,height=self.pet_size,background='white',highlightthickness=0)
        self.canvas.pack()

        # Show current mood and set the font and appropriate size
        self.mood_label = tk.Label(self.window, text=f"Mood:{self.get_mood_text(self.current_mood)}", font=('Arial', 12))
        self.mood_label.pack()

    # Set mood text for pet
    def get_mood_text(self, mood_score):
        mood_texts = ["happy", "sad", "excitement", "calmness", "dynamic"]
        # Returns the corresponding mood text based on the mood's score
        return mood_texts[mood_score]

    # The pet's image is drawn here, including the body, head, ears, eyes and nose.
    def init_pet(self):
        self.current_color = self.colors[self.current_color_index]
        body = self.canvas.create_oval(20, 40, 80, 100, fill=self.current_color, outline="")
        head = self.canvas.create_oval(30, 10, 70, 50, fill=self.current_color, outline="")
        ear_left = self.canvas.create_oval(25, -10, 40, 30, fill=self.current_color, outline="")
        ear_right = self.canvas.create_oval(60, -10, 75, 30, fill=self.current_color, outline="")
        eye_left = self.canvas.create_oval(38, 25, 42, 29, fill="black")
        eye_right = self.canvas.create_oval(58, 25, 62, 29, fill="black")
        nose = self.canvas.create_oval(48, 35, 52, 39, fill="pink", outline="")
        # In order not to let the colour change block and affect the pet's features, the eyes and nose are removed from the parts
        self.pet_parts = [body, head, ear_left, ear_right]

    def init_audio(self):
        # Here i use pygame's audio module to play the pet's audio
        pygame.mixer.init()
        self.sounds = {'effect': pygame.mixer.Sound(r'audio/792879__klankbeeld__great-spotted-woodpecker-001-park-forest-haanwijk-1128-am-250306_1056.wav')}

    def process_camera(self):
        # Here OpenCV is used to open the camera and read the video
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                continue
            # Part of gesture recognition using mediapipe
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            results = self.hands.process(image)
            # Reacts if key points of the hand are recognised
            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                self.handle_gesture(hand_landmarks)

            cv2.waitKey(10)

    def handle_gesture(self, landmarks):
        # Obtain the corresponding coordinates of the key points of the hand
        tips = {'thumb': landmarks.landmark[4],'index': landmarks.landmark[8],'middle': landmarks.landmark[12]}
        # The logic of gesture judgement
        thumb_index_dist = np.hypot(
            tips['thumb'].x - tips['index'].x,
            tips['thumb'].y - tips['index'].y)
        
        # Performs different actions depending on the gesture
        # (For example, the OK gesture causes the pet's colour to change, an open palm causes the pet to follow the movement, and a clenched fist plays a sound effect and changes the pet's mood.)

        # OK gesture: change pet colour
        if thumb_index_dist < 0.05:
            self.window.after(0, self.change_color)
        # Open Palm: pet follows palm
        elif self.is_open_hand(landmarks):
            self.window.after(0, self.follow_hand, tips['index'])  
        # Shake your fist: play the audio and update the mood
        elif self.is_closed_fist(landmarks):
            current_time = time.time()
            if current_time - self.last_effect_time > self.effect_cooldown:
                self.last_effect_time = current_time
                self.window.after(0, lambda: self.sounds['effect'].play())
                self.window.after(0, self.update_mood)

    def change_color(self):
        # Cyclic colour switching
        # self.current_color_index is incremented and limited to the range of the self.colors list by % len(self.colors) for cyclic colour changes
        self.current_color_index = (self.current_color_index+1) % len(self.colors)
        self.current_color = self.colors[self.current_color_index]
        # Update all pet parts to change colours
        for part in self.pet_parts:
            self.canvas.itemconfig(part, fill=self.current_color)

    def follow_hand(self, tip):
        # Convert camera coordinates to screen coordinates
        screen_x = tip.x*self.screen_width
        screen_y = tip.y*self.screen_height
        # Get current pet location
        pet_x = self.window.winfo_x()
        pet_y = self.window.winfo_y()
        # Calculate the new position so that the pet moves smoothly and prevents transients
        new_x = pet_x+(screen_x-pet_x)*0.1
        new_y = pet_y+(screen_y-pet_y)*0.1
        # Updating the location of pets
        self.window.geometry(f"+{int(new_x)}+{int(new_y)}")

    def update_mood(self):
        # The pet can randomly change moods and have its own moods
        self.current_mood = (self.current_mood + random.randint(0, 1))%len(self.colors)
        # Update Mood Text
        self.mood_label.config(text=f"Mood:{self.get_mood_text(self.current_mood)}")
        # Colour change of pet
        self.current_color = self.colors[self.current_mood]
        for part in self.pet_parts:
            self.canvas.itemconfig(part, fill=self.current_color)

    def is_open_hand(self, landmarks):
        # Calculate whether the palm is open or not by the distance between the fingertips and the root of the palm
        distances = []
        # Fingertip Key Points
        for tip in [8, 12, 16, 20]: # 8: index finger, 12: middle finger, 16: ring finger, 20: little finger
            # Calculate the x-axis distance between the fingertip and the root of the palm
            dx = landmarks.landmark[tip].x-landmarks.landmark[0].x
            # Calculate the y-axis distance between the fingertip and the root of the palm
            dy = landmarks.landmark[tip].y-landmarks.landmark[0].y
            distances.append(np.hypot(dx, dy))
        # If all distances are greater than 0.3, the judgement is open-handed
        return all(d > 0.3 for d in distances)

    def is_closed_fist(self, landmarks):
        # Calculate whether to make a fist by the distance between the fingertips and the root of the palm
        distances = []
        for tip in [8, 12, 16, 20]:
            # x-axis
            dx = landmarks.landmark[tip].x-landmarks.landmark[0].x
            # y-axis
            dy = landmarks.landmark[tip].y-landmarks.landmark[0].y
            distances.append(np.hypot(dx, dy))
        # If the distances are all less than 0.15, the hand is considered to be a clenched fist
        return all(d < 0.15 for d in distances)
    
DesktopPet()
