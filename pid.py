# PID function , tweak based on the smoothness


import math
import time

class PID:
    def __init__(self, K_PID, k, alpha):
        self.kp, self.ki, self.kd = K_PID
        self.k = k
        self.alpha = alpha

        self.last_output_x = 0
        self.last_output_y = 0
        self.last_error_x = 0
        self.last_error_y = 0
        self.integral_x = 0
        self.integral_y = 0
        self.last_time = None

    def compute(self, goal, current):
        current_time = time.perf_counter()
        if self.last_time is None:
            self.last_time = current_time
            return 0, 0

        error_x = goal[0] - current[0]
        error_y = goal[1] - current[1]

        dt = current_time - self.last_time

        self.integral_x += error_x * dt
        self.integral_y += error_y * dt

        derivative_x = (error_x - self.last_error_x) / dt
        derivative_y = (error_y - self.last_error_y) / dt

        output_x = self.kp * error_x + self.ki * self.integral_x + self.kd * derivative_x
        output_y = self.kp * error_y + self.ki * self.integral_y + self.kd * derivative_y

        output_x = self.alpha * output_x + (1 - self.alpha) * self.last_output_x
        output_y = self.alpha * output_y + (1 - self.alpha) * self.last_output_y

        theta = math.degrees(math.atan2(output_y, output_x))
        if theta < 0:
            theta += 360
        phi = self.k * math.sqrt(output_x**2 + output_y**2)

        self.last_error_x = error_x
        self.last_error_y = error_y
        self.last_output_x = output_x
        self.last_output_y = output_y
        self.last_time = current_time

        return theta, phi
