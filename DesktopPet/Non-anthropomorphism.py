import cv2
import tkinter as tk
import mediapipe as mp
import numpy as np
import threading
import time

class ControlPet:
    def __init__(self):
        self.window = None
        self.canvas = None
        self.pet_size = 120

        self.screen_width = 0
        self.screen_height = 0

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)

        self.init_window()

        self.camera_thread = threading.Thread(target=self.process_camera)
        self.camera_thread.daemon = True
        self.camera_thread.start()
        self.window.mainloop()

    def init_window(self):
        self.window = tk.Tk()
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', 1)
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.window.config(background="white")
        self.window.wm_attributes("-transparentcolor", "white")

        self.canvas = tk.Canvas(self.window, width=self.pet_size, height=self.pet_size, background='white', highlightthickness=0)
        self.canvas.pack()

        self.dialog = tk.Label(self.window, text="", font=('Arial', 12), background="white")
        self.dialog.pack()

    def update_dialog(self, text):
        self.dialog.config(text=text)

    def process_camera(self):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                continue

            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            results = self.hands.process(image)

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                self.handle_gesture(hand_landmarks)

    def handle_gesture(self, landmarks):
        tips = {'thumb': landmarks.landmark[4], 'index': landmarks.landmark[8], 'middle': landmarks.landmark[12]}
        thumb_index_dist = np.hypot(tips['thumb'].x - tips['index'].x, tips['thumb'].y - tips['index'].y)

        if thumb_index_dist < 0.05:
            self.window.after(0, self.on_ok_gesture)
        elif self.is_open_hand(landmarks):
            self.window.after(0, self.on_open_hand, tips['index'])
        elif self.is_closed_fist(landmarks):
            self.window.after(0, self.on_fist)

    def follow_hand(self, tip):
        screen_x = tip.x * self.screen_width
        screen_y = tip.y * self.screen_height
        pet_x = self.window.winfo_x()
        pet_y = self.window.winfo_y()
        new_x = pet_x+(screen_x-pet_x)*0.1
        new_y = pet_y+(screen_y-pet_y)*0.1
        self.window.geometry(f"+{int(new_x)}+{int(new_y)}")

    def is_open_hand(self, landmarks):
        distances = []
        for tip in [8, 12, 16, 20]:
            dx = landmarks.landmark[tip].x - landmarks.landmark[0].x
            dy = landmarks.landmark[tip].y - landmarks.landmark[0].y
            distances.append(np.hypot(dx, dy))
        return all(d > 0.3 for d in distances)

    def is_closed_fist(self, landmarks):
        distances = []
        for tip in [8, 12, 16, 20]:
            dx = landmarks.landmark[tip].x - landmarks.landmark[0].x
            dy = landmarks.landmark[tip].y - landmarks.landmark[0].y
            distances.append(np.hypot(dx, dy))
        return all(d < 0.15 for d in distances)

    def on_ok_gesture(self):
        self.update_dialog("Task completed.")

    def on_open_hand(self, tip):
        self.follow_hand(tip)
        self.update_dialog("Input received.")

    def on_fist(self):
        self.update_dialog("Error: Please try again.")

ControlPet()
