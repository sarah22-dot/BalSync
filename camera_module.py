# for tracking through rasp camera


import cv2
import numpy as np
from picamera2 import Picamera2

class Camera:
    def __init__(self):
        self.picam2 = Picamera2()
        self.height = 480
        self.width = 480
        self.config = self.picam2.create_video_configuration(
            main={"format": 'RGB888', "size": (self.height, self.width)},
        )
        self.picam2.configure(self.config)

        # Color range for pink object
        self.lower_pink = np.array([165, 150, 50])
        self.upper_pink = np.array([180, 255, 255])
        self.picam2.start()

    def take_pic(self):
        return self.picam2.capture_array()

    def show_video(self, image, position=None):
        img = image.copy()
        cv2.line(img, (0, 240), (480, 240), (0, 0, 0), 2)
        cv2.line(img, (240, 0), (240, 480), (0, 0, 0), 2)
        cv2.circle(img, (240, 240), 5, (0, 255, 255), -1)

        if position:
            x, y, r = position
            cv2.circle(img, (int(x), int(y)), int(r), (0, 255, 0), 2)

        cv2.imshow("Ball Tracker", img)
        cv2.waitKey(1)

    def find_ball(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_pink, self.upper_pink)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest = max(contours, key=cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(largest)
            area = cv2.contourArea(largest)
            if area > 200:
                return int(x), int(y), int(radius), int(area)
        return -1, -1, 0, 0

    def clean_up(self):
        self.picam2.stop()
        self.picam2.close()
        cv2.destroyAllWindows()
