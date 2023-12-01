# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 13:29:26 2023

@author: kozyt
"""
import math

class Position_Tracker():
    def __init__(self):
        '''!@brief              initializes the position tracker
            @details
            @param
        '''
        self.wheelbase = 4
        self.current_heading = 0
        self.x = 0
        self.y = 0
        
    def track(self, R_right, R_left):
        '''!@brief              tracks robot location
            @details            calculates the changes in headings and distances in global x and y
            @param              distance traveled by right and left wheel
        '''
        # might need to be tuned to be if abs(R_right-R_left)>>>variance for straight line movement
        if R_right != R_left:
            heading_change = (R_right-R_left)/self.wheelbase
            
            
            # Calculate radius of the arc the robot is moving along
            radius = (R_right + R_left) / (2 * heading_change)

            # Calculate change in position for the center of the robot
            
            delta_x = radius * math.sin(heading_change)
            delta_y = radius * (1- math.cos(heading_change))
            self.current_heading = self.current_heading + heading_change
        else:
            delta_x = R_right * math.cos(self.current_heading)
            delta_y = R_right * math.sin(self.current_heading)
            
        self.x = self.x + delta_x
        self.y = self.y + delta_y
        
        