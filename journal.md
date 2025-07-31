## 17th July  (3.5 hours)

The journey began with a vision to create a robotic platform capable of balancing a ball in real-time. I called it **Balsync**, a fusion of "Balance" and "Synchronization." My goal was to explore how real-time feedback, control theory, and mechanical design could be merged into one responsive machine. I wanted the platform to feel almost alive, reacting fluidly like a human hand adjusting to a marble's position.

<img width="403" height="370" alt="image" src="https://github.com/user-attachments/assets/0dbee017-c9f9-42b1-a304-2f129cbb170f" />

I opened Fusion 360 with a fresh project and began blocking out the mechanical structure. I decided that the system would be built in layers. I began studying how each part would support the others. This base would house the Raspberry Pi 4 (4GB), my central controller. Using digital calipers, I ensured the CAD model had cutouts aligned with the Pi’s ports including GPIO header, micro-HDMI, USB, and SD card.

<img width="903" height="630" alt="image" src="https://github.com/user-attachments/assets/fe3a1136-9b78-4014-975a-eee5b55ce266" />


## 18th July  ( 1 hour)

On the second day, I focused on the Middle Base.step file. This part was designed primarily for structural spacing and support. It provided the necessary vertical clearance between the bottom base and the top platform. More importantly, it ensured that there was enough room between the servo motors to avoid mechanical interference. While it did not directly hold any active components, it acted as a physical spacer, stabilizing the vertical stack and creating proper gaps for servo horns to operate freely.I revised the model twice to ensure that the servo bodies would not clash with the surrounding geometry. The middle base also added extra stiffness to the assembly and helped guide wiring through clean slots. I exported the model for laser cutting in the same 3mm acrylic. Once cut and mounted, it created a precise vertical stack that set the stage for servo placement above.

<img width="877" height="464" alt="image" src="https://github.com/user-attachments/assets/72704260-0846-463c-8ba7-02214fb78ebf" />


## 19th July  (0.5 hours)

The third day was spent working on the servo connector file. These linkages connect each servo horn to the top platform, converting the rotational motion of the servos into a linear displacement that tilts the plate.
I printed these links in PLA and added metal bushings at the pivot points to reduce long-term wear and ensure smoother operation. It was crucial for the links to maintain rigidity while being lightweight. I reviewed some basic concepts of robotic linkages to confirm that my length and angular clearance were correct.Once ready, I attached these links to the servo horns with screws and verified their freedom of movement.

<img width="713" height="534" alt="image" src="https://github.com/user-attachments/assets/2d5e8bd2-6f9a-43a9-abf4-a1aa86175d1d" />


## 19th and 20th July  (5 hours)

Today, I shifted to designing the TOP Base, which is the moving platform that will support the ball. This plate had to be light yet rigid, as it needed to tilt responsively to the ball’s position.
The design included three equidistant holes to attach the servo links. I counter-sunk the mounting holes from underneath for a clean finish and made sure the arms would have enough torque to tilt the platform.
After assembling it with the links, I manually rotated each servo and observed the movement of the platform. It was satisfying to see that even without any code, the structure moved fluidly in response to servo input.

<img width="676" height="497" alt="image" src="https://github.com/user-attachments/assets/8243a04f-4ec5-4586-a009-3cb977d03ed7" />
<img width="339" height="626" alt="image" src="https://github.com/user-attachments/assets/c1afb48c-4c51-49d2-af2f-2aae2c661567" />



## 21st July  (1.5 hours)

Next, I tackled the camera system. I placed it above the top base in Fusion 360 to simulate the camera’s field of view.The camera mount was designed to hold a 5MP Raspberry Pi camera vertically above the top platform. It needed to be rigid and vibration-free for accurate image tracking.

<img width="853" height="547" alt="image" src="https://github.com/user-attachments/assets/3d6969bc-962a-4320-a225-d7d21c563611" />




## 22nd July  (2.5 hours)

The ring was a circular structural brace that tied together the midpoint of the three servo arms. It was meant to prevent excessive wobble and ensure that each arm contributed equally to the tilt.I will increase the infill so that during 3D printing to make it stronger and more rigid. I used M3 standoffs to mount it onto the arms. This ring essentially acted like a stabilizing skeleton for the whole tilt mechanism.

<img width="641" height="411" alt="image" src="https://github.com/user-attachments/assets/14051f5d-10aa-47a2-a418-286cf2b36b7d" />
<img width="729" height="412" alt="image" src="https://github.com/user-attachments/assets/a034e9e2-2fe0-42e5-ae38-e73a07500209" />


## 23rd July  (7 hours)

With all mechanical elements in place, I began Assembling. The servos would be powered via a 5V 3A UBEC, connected to the PCA9685 16-channel PWM controller. The PCA module would be interfaced to the Raspberry Pi via I2C.

<img width="725" height="704" alt="image" src="https://github.com/user-attachments/assets/3c6fd185-8706-4656-a335-c5f706f5c091" />
<img width="678" height="715" alt="image" src="https://github.com/user-attachments/assets/ecb351ec-2780-48ab-b52a-1615c341a195" />


## 24th July  (7 hours)

Today, I moved into software territory. Even though I had not yet tested the hardware, I wanted to write the entire codebase to reinforce what I had learned.

I created a Python environment on the Raspberry Pi using `venv`. Then I installed `opencv-python`, `adafruit-circuitpython-servokit`, and `numpy`. My goal was to write the logic in modules so I could test them one by one.


<img width="1254" height="648" alt="image" src="https://github.com/user-attachments/assets/6c5efadf-af0e-40f9-9cdf-2e3085f55a4a" />


best video for understanding pid:https://www.youtube.com/watch?v=UR0hOmjaHp0


Coding Module 1: ServoControl.py — This module used the Adafruit ServoKit library to control individual servos via the PCA9685. I wrote a function `set_angles(theta1, theta2, theta3)` to send target angles to each servo. This helped decouple the control logic from hardware access.

Coding Module 2: PID.py — I implemented a basic PID controller class with tunable parameters. Even without testing it physically, I simulated it using mock error values. The formula was:

```
output = kp * error + ki * integral + kd * derivative
```

I added methods to reset and tune the PID on the fly. I studied how each parameter including proportional (P), integral (I), and derivative (D) would influence the system’s stability and response time.

Given a desired tilt in X and Y, it calculated the required change in Z-height at each servo arm and converted it into servo angles. I used triangle-based trigonometric equations and servo geometry to derive an approximation. It was amazing to translate a theoretical vector into three coordinated servo actions. Understanding inverse kinematics helped me realize how robotic arms, hexapods, and humanoid legs operate.


<img width="843" height="596" alt="image" src="https://github.com/user-attachments/assets/d882e590-bc2e-460a-9e48-4e19e6c138fa" />


[arm2 (1).pdf](https://github.com/user-attachments/files/21533732/arm2.1.pdf)


Referred this pdf for implementing Inverse kinematics


Source:https://youtu.be/-1pX518wlu8?si=4Z-6UjNNJS6UV36Q

Coding Module 4: BallTracker.py — I used OpenCV to apply HSV filtering and track a pink object in the video stream. I added morphological operations like erosion and dilation to clean the mask. Using `cv2.moments`, I extracted the centroid coordinates and printed them for validation.



<img width="1336" height="851" alt="image" src="https://github.com/user-attachments/assets/84db9897-691f-4ccb-9658-a81292c8962a" />



I went through the entire video to understand basics of opencv and how i can implement in my project.


Although I did not test any modules on real hardware yet, writing this code helped me understand the complete workflow. I now had a clear software framework that I could iterate on once testing began.

Would you like me to continue from 25th July onward with PID tuning sessions, ball tracking debugging, and final integration?

