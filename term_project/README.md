# Girlfriend #2 - Term Project
#### Designed, Created by Noah Tanner and Kosimo Tonn
#### ME 405, Professor Charlie Refvem
#### California Polytechnic State University, San Luis Obispo

## Overview
Girlfriend #2 is a line following robot designed to follow a course designed specifically for the term project competition. Our design emphasizes simplicity and minimalism, as we have found that complexity in mechatronics projects should be avoided if there is a simpler solution. The specific requirements for the project can be found in the [references](#references) section

*INSERT PHOTO OF ROBOT*

## Hardware Setup and Design
The components that we were provided with were the following: 
- [Romi robot kit](https://www.pololu.com/category/202/romi-chassis-and-accessories)
- [Motor Driver and Power Distribution Board]( https://www.pololu.com/product/3543)
- [Romi Encoder Pair Kit](https://www.pololu.com/product/3542)
- [Nucleo-L476RG](https://www.st.com/en/evaluation-tools/nucleo-l476rg.html)
- Shoe of Brian (Designed by Professor Ridgley)
- Assembly Items
    | Quantity | Name |
    |----------|------|
    | 4x | M2.5 x 8mm Standoff |
    | 4x | M2.5 x 8mm Standoff |
    | 4x | M2.5 x 10mm Standoff |
    | 4x | M2.5 x 30mm Standoff |
    | 4x | M2.5 x 6mm Socket Head Cap Screw |
    | 4x | M2.5 x 8mm Socket Head Cap Screw |
    | 4x | M2.5 x 10mm Socket Head Cap Screw |
    | 8x | M2.5 Nylon Lock Nuts |
    | 8x | M2.5 Nylon Washer |
    | 1x | Acrylic Romi-to-Shoe Adapter |
    | 1x | Romi-to-shoe Power Cable |
    | 2x | Romi-to-Shoe Encoder Cable |
    | 2x | Romi-to-shoe Motor Cable |
- BNO055 IMU Breakout Board

Prior to the addition of our other components, the base model of the robot was assembled based on the instructions that can be found in the [references](#references) section.

With the base of the project built, in order to complete the term project requirements of line following, object avoidance, and homing, we purchased the following items:
- [QTR Reflectance Sensor QTR-HD-11A](https://www.pololu.com/product/4211)
- [QTR Relectance Sensor QTR-HD-1A](https://www.pololu.com/product/4201)
- [Snap-Action Switch with Roller](https://www.pololu.com/product/1404)
- [Duracell AA battery x40](https://www.costco.com/duracell-coppertop-alkaline-aa-batteries%2C-40-count.product.100836545.html)

The Reflectance sensors were attatched using 3 leftover M2.5 x 8mm standoffs, and 3 M2.5 Nylon Lock Nuts. They were directly fastened into holes on the Romi Chasis on the front. For the snap-action switch implementation, a custom 3D printed part was designed to hold the switch out front of the robot. Various cables for sensor outputs and power were made from wire and pin headers that were provided by professor Refvem. A detailed wiring layout can be found in the [excel](#references) sheet.

## Software Setup and Design
Table 1 shows the files required to run our robot and a short description of what each file does. 
#### Table 1.
| File Name | Description |
|-----------|-------------|
| ```encoder_class.py``` | encoder class to operate the romi encoders |
| ```controls.py``` | robot operation file to control movement and function of the reflectance sensors |
| ```romi_driver.py``` | motor driver class to operate the romi motor drivers |
| ```imu_driver.py``` | BNO055 driver class used to get euler angle data from the imu |
| ```position_calcs.py``` | calcuation file to determine the global positioning of the robot |
| ```position_tracker.py``` | file to track and record the global positioning of the robot as it moves through the course |
| ```term_main.py``` | main file that sets up and runs each generator function cooperatively
| ```controls_gen.py``` | generator implementation of the controls file |
| ```obj_gen.py``` | object handling generator function to avoid the wall |
| ```cotask.py``` | task scheduler file written by Professor Ridgley |
| ```cal_coeff.txt``` | calibration coefficient file for the imu |

Girlfriend #2 works through the usage of 3 different generator functions, and 8 support files that are scheduled in a main file using ```cotask.py```. Each generator function is designed as a finite state machine that runs cooperatively, yielding its current state after each execution, switching between states when certain conditions have been met. Through testing, task frequencies were determined. Finite state machines 
#### Task Diagram

#### Finite State Machines

## Demonstration

## Calculations

## Analysis

## References
1. [Term Project Assignment](./ME405_2238_Lab_0x06.pdf)
2. [Romi Assembly Instructions](./ME405_2238_Romi_Assembly.pdf)
3. [Wiring Spreadsheet](./wiring.xlsx)


