
# Balsync – Ball Balancing Robot using Raspberry Pi

This is my project for Hack Club Highways. I call it Balsync A  smart robotic platform that balances a ball in real-time using a Raspberry Pi, computer vision, and precise servo control. I designed and built this system to understand how software and hardware can work together to maintain balance dynamically, just like how we naturally adjust our hand to keep a marble from rolling off our palm.

In Balsync, I used a Raspberry Pi 4 Model B (4GB RAM) as the core controller. A 5MP camera is mounted above the platform and continuously tracks the position of a pink-colored ball. The platform itself is mounted on three MG995 metal gear servo motors. These motors are driven by a PCA9685 16-channel PWM module that receives instructions via I2C from the Raspberry Pi. By adjusting the angles of these three servos, I am able to tilt the platform in any direction.

The main task of Balsync is to keep the ball at the center of the platform. To achieve this, I used a PID control algorithm that continuously calculates how far the ball is from the center. The PID controller then outputs two values: the direction in which the platform should tilt, and how much it should tilt. These values are passed to an inverse kinematics function that calculates the required angles for the three servo motors. This way, the robot actively tries to cancel out any displacement of the ball.

<img width="664" height="211" alt="image" src="https://github.com/user-attachments/assets/befeb0cc-fbab-42b5-adeb-7dcc6e2a4a90" />


For ball detection, I used OpenCV with HSV color masking. I chose the pink color range since it was easily distinguishable in most lighting conditions. After masking, I applied contour detection to find the ball and calculate its position in the frame. This position is then converted into an error signal which feeds into the control logic.

To ensure responsiveness, I used Python's threading module to run the camera capture and robot movement functions in parallel. This allowed me to track the ball and move the servos simultaneously without lag. I also added frame-per-second counters to monitor the performance of both camera input and robot reaction speed.

All the hardware components I used were easily available in India. I sourced my Raspberry Pi, servo motors, camera, and electronics modules from platforms like Robocraze.in, Amazon.in, and Shaarvi Electronics. The full list includes the Raspberry Pi 4 (4GB), MG995 servo motors (x3), PCA9685 servo driver, Pi camera module, camera cable, 5V 2A power adapter, jumper wires, a barrel jack, and some mechanical components like ball joints and bearings. The total cost of the system was kept under ₹8500, making it an affordable and educational project.

<img width="407" height="415" alt="image" src="https://github.com/user-attachments/assets/f5a8e974-b12b-4694-9e40-ae41f37a92af" />


The codebase for Balsync is fully written in Python and currently structured into separate modules as part of the planning and simulation phase. The main logic is written in `main.py`, which coordinates camera input, control output, and posture commands. The image processing and ball detection logic are contained in `camera_module.py`. The mathematical calculations for inverse kinematics and servo actuation are organized in `robot_module.py`, and the PID control loop is implemented in `pid_module.py`. I have focused on writing clean, modular, and well-commented code that will help me and others understand and build upon this system more easily once the hardware phase begins.

As this project is part of my Hack Club Highways proposal, I have not yet physically built the robot. However, I have completed initial code development, logic design, and hardware research. Once the grant is approved, I will begin purchasing components and assembling the platform. The Raspberry Pi will be configured with I2C and camera interfaces enabled through raspi-config. I will use Python 3 to run the codebase, along with dependencies like `opencv-python`, `numpy`, and `picamera2`. A 5V 2A or 3A adapter will be used to power the servo motors through the PCA9685 module.

Through this proposal, I aim to bring together concepts from real-time computer vision, feedback control systems, and robotics. Even though I have not yet implemented the physical prototype, I have already learned a lot while writing and testing the logic, especially while tuning PID outputs, refining ball detection algorithms, and planning servo coordination using inverse kinematics. I believe Balsync has strong potential not only as a demonstration of robotics principles, but also as a scalable base for more advanced systems like gesture-controlled balancing platforms or predictive stabilization bots.

As part of my Hack Club Highways submission, I am excited to present Balsync as a technically feasible, impactful, and educational project. I hope it gets selected for the grant so that I can begin the hardware build, testing, and real-world validation. I also plan to expand the system in future iterations with machine learning-based ball prediction, smoother servo interpolation, and possibly remote control via mobile or web interfaces.

Images, progress documentation, and hardware assembly photos will be added to this repository after I begin building:






































---

## code structure

├── camera_module.py   ->      # Handles PiCamera input and ball detection via OpenCV

├── inverse_kinematics.py  ->  # Computes servo angles to tilt the platform

├── main.py       ->           # Main control loop integrating all modules

├── pid.py      ->             # Simple PID controller for smooth balancing

---

---
## BOM
| # | Component                                   | Qty | Source                          | Price (₹)         | Approx. Price (USD) | 
| - | ------------------------------------------- | --- | ------------------------------- | ----------------- | ------------------- | 
| 1 | Raspberry Pi 4 Model B (4 GB RAM)           | 1   | Robocraze.in                    | ₹5,546            |    $67              | 
| 2 | MG995 Metal‑Gear Servo Motor (180°)         | 3   | Robocraze.in                    | ₹550 × 3 = ₹1,650 |    $20              | 
| 3 | PCA9685 16‑Channel PWM Servo Driver Module  | 1   | Shaarvi Electronics             | ₹720              |    $8.70            | 
| 4 | Raspberry Pi 5 MP Camera Module (OV5647)    | 1   | Amazon.in                       | ₹339              |    $4.10            | 
| 5 | CSI Camera Ribbon Cable (  200 mm)          | 1   | Amazon.in                       | ₹120              |    $1.45            | 
| 6 | 5 V DC Power Adapter 2–3 A                  | 1   | Amazon.in                       | ₹350              |    $4.20            | 
| 7 | Female Barrel Jack Connector                | 1   | Robocraze.in                    | ₹40               |    $0.48            | 
| 8 | Jumper Wire Set (F‑F, F‑M)                  | 1   | Robocraze.in                    | ₹50               |    $0.60            | 
| 9 | Mechanical Hardware: Ball‑joints & Bearings | 3   | Amazon.in                       | ₹300              |    $3.60            | 

---
Total Estimated Cost
INR: ~₹8,245
USD: ~$99
---
