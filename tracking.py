# u need to tweak lower_pink and upper_pink based on lighting and actual object colour
# balls position is drawn in green and axes are drwan for reference
import cv2
import numpy as np
from picamera2 import Picamera2
import time

class Camera:
    def __init__(self):
        self.picam2 = Picamera2()
        self.height = 480
        self.width = 480
        self.config = self.picam2.create_video_configuration(
            main={"format": 'RGB888', "size": (self.height, self.width)},
        )
        self.picam2.configure(self.config)

        # Pink color range (adjust as needed)
        self.lower_pink = np.array([165, 150, 50]) 
        self.upper_pink = np.array([180, 255, 255])

        self.picam2.start()

    def take_pic(self):
        return self.picam2.capture_array()

    def show_video(self, image, ball_position=None):
        img_display = image.copy()
        cv2.line(img_display, (0, 240), (480, 240), (0, 0, 0), 2)
        cv2.line(img_display, (240, 0), (240, 480), (0, 0, 0), 2)
        cv2.circle(img_display, (240, 240), 5, (0, 255, 255), -1)
        
        if ball_position:
            (x, y, radius) = ball_position
            cv2.circle(img_display, (int(x), int(y)), int(radius), (0, 255, 0), 2)

        cv2.imshow("Ball Tracker", img_display)
        cv2.waitKey(1)

    def find_ball(self, image):
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(image_hsv, self.lower_pink, self.upper_pink)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(largest_contour)
            area = cv2.contourArea(largest_contour)

            if area > 200:
                return int(x), int(y), int(radius), int(area)
        return None

    def clean_up_cam(self):
        self.picam2.stop()
        self.picam2.close()
        cv2.destroyAllWindows()


def main():
    cam = Camera()
    try:
        while True:
            image = cam.take_pic()
            ball_data = cam.find_ball(image)
            if ball_data:
                x, y, r, area = ball_data
                print(f"Ball found at (x={x}, y={y}), radius={r}, area={area}")
                cam.show_video(image, (x, y, r))
            else:
                print("Ball not found")
                cam.show_video(image)
    finally:
        cam.clean_up_cam()


if __name__ == "__main__":
    main()
