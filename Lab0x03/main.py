# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 13:40:49 2023

@author: kozyt
"""

# Imports
#import L6206, Encoder, ClosedLoop

# Functions
def PromptEncoder():
    print("1 for Encoder 1, 2 for Encoder 2")
    choice = input('')
    if choice == ('1'):
        return ENC_A
    elif choice == ('2'):
        return ENC_B

def PromptMotor():
    print("1 for Motor 1, 2 for Motor 2")
    choice = input('')
    if choice == ('1'):
        return mot_a
    elif choice == ('2'):
        return mot_b

#Main
while True:
    key = input('')
    #Zero Encoder 1 or 2
    if key == ('Z' or 'z'):
        print("Zero Encoder 1 or 2?")
        PromptEncoder()
        
    #Print Position of Encoder 1 or 2
    if key == ('P' or 'p'):
        print("Print Position for Encoder 1 or 2?")
        PromptEncoder()
        
    #Print Delta of Encoder 1 or 2   
    if key == ('D' or 'd'):
        print("Print Delta for Encoder 1 or 2?")
        PromptEncoder()
        
    #Print Velocity of Encoder 1 or 2        
    if key == ('V' or 'v'):
        print("Print Velocity for Encoder 1 or 2?")
        PromptEncoder() 
        
    #Enter Duty Cycle for Motor 1 or 2    
    if key == ('M' or 'm'):
        print("Duty Cycle for Motor 1 or 2?")
        PromptMotor()
        
    #Collect Speed and Position Data for 30s of Encoder 1 or 2, then send data    
    if key == ('G' or 'g'):
        print("Collect Data for Encoder 1 or 2?")
        PromptEncoder()
        
    #Switch to Closed-Loop Mode    
    if key == ('C' or 'c'):
        
    #Choose closed-loop gains for Motor 1 or 2    
    if key == ('K' or 'k'):
        print("Choose Closed-loop Gain for Motor 1 or 2?")
        PromptMotor()
        
    #Choose velocity set point for Motor 1 or 2     
    if key == ('S' or 's'):
        print("Choose Velocity Set Point for Motor 1 or 2?")
        PromptMotor()
        
    #Trigger Step Response on Motor 1 or 2 then send data    
    if key == ('R' or 'r'):
        print("Trigger Step Response for Motor 1 or 2?")
        PromptMotor()
        
    #Switch to Open-Loop Mode    
    if key == ('o' or 'o'):
