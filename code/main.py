import time
import cv2
import numpy as np
from picamera2 import Picamera2

# This class handles all the camera work — simple and clean
class Camera:
    def __init__(self):
        self.picam2 = Picamera2()
        self.height = 480
        self.width = 480

        # Configuring the camera with proper resolution and format — no jugaad here
        self.config = self.picam2.create_video_configuration(
            main={"format": 'RGB888', "size": (self.height, self.width)},
        )
        self.picam2.configure(self.config)

        # Defining the range of pink color in HSV — our target ball color
        self.lower_pink = np.array([165, 150, 50])   # Lower limit of pink (dark shade)
        self.upper_pink = np.array([180, 255, 255])  # Upper limit of pink (light shade)

        self.picam2.start()
        print("Camera started successfully 🚀")

    # Function to capture one frame from the camera
    def take_pic(self):
        return self.picam2.capture_array()

    # Display video with optional ball position overlay
    def show_video(self, image, ball_position=None):
        img_display = image.copy()

        # Draw cross lines in the center — like a target
        cv2.line(img_display, (0, 240), (480, 240), (0, 0, 0), 2)
        cv2.line(img_display, (240, 0), (240, 480), (0, 0, 0), 2)

        # Mark the exact center point for easy reference
        cv2.circle(img_display, (240, 240), 5, (0, 255, 255), -1)

        # If ball is detected, draw a green circle around it
        if ball_position:
            (x, y, radius) = ball_position
            cv2.circle(img_display, (int(x), int(y)), int(radius), (0, 255, 0), 2)

        cv2.imshow("Ball Tracker", img_display)
        cv2.waitKey(1)

    # Function to detect the pink ball in the frame
    def find_ball(self, image):
        # Convert image from BGR to HSV — better for color detection
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Create a mask for pink color
        mask = cv2.inRange(image_hsv, self.lower_pink, self.upper_pink)

        # Find contours (edges) in the mask — basically the shapes
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # If we found any pink blob
        if contours:
            # Take the biggest blob — assuming it’s our ball
            largest_contour = max(contours, key=cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(largest_contour)
            area = cv2.contourArea(largest_contour)

            # Only return if it's big enough — ignore tiny noise
            if area > 200:
                return int(x), int(y), int(radius), int(area)
        return None  # Ball not found

    # Clean up everything when we’re done — good manners
    def clean_up_cam(self):
        self.picam2.stop()
        self.picam2.close()
        cv2.destroyAllWindows()
        print("Camera stopped and windows closed ✅")
