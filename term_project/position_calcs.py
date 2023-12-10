# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 14:58:53 2023

@author: kozyt
"""

import math


# Given distances traveled by the right and left wheels for quarter arcs of 9-unit and 7-unit radii
R_right = math.pi #5 * math.pi *.5  # Distance traveled by the right wheel (quarter of a 9-unit radius)
R_left = -math.pi #* 5 * math.pi *.5  # Distance traveled by the left wheel (quarter of a 5-unit radius)
wheelbase = 4
current_heading = 0
heading_change = 0
print("initial heading:", current_heading*180/(math.pi))

x = 0
y = 0





# Calculate change in position for the center of the robot

#radius about centerpoint of arc



if R_right != R_left:
    heading_change = (R_right-R_left)/wheelbase
    
    
    # Calculate radius of the arc the robot is moving along
    radius = (R_right + R_left) / (2 * heading_change)

    # Calculate change in position for the center of the robot
    
    delta_x = radius * math.sin(heading_change)
    delta_y = radius * (1- math.cos(heading_change))
    current_heading = current_heading + heading_change
else:
    delta_x = R_right * math.cos(current_heading)
    delta_y = R_right * math.sin(current_heading)

print("heading change:", heading_change*180/(math.pi))
print("final heading:", current_heading*180/(math.pi))
print("Change in x:", delta_x)
print("Change in y:", delta_y)
print("New position in x:", x + delta_x)
print("New position in y:", y + delta_y)