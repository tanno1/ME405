# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 18:02:33 2023

@author: kozyt
"""
#Import
import random

#Variables and Messages
state = 0
wins = 0
losses = 0
replay_flag = False
grading_mode = False

start_mess = """                      Welcome to the game of Mastermind!

You will be the codebreaker. Try to break the secret code by entering 4-digit
codes using the numbers 0-5. Your guesses will be marked with a (+) symbol for
each correct value in the correct location and a (-) for each correct value in
an incorrect location.

                             Press any key, then enter, to begin"""

#Method for Filtering User Inputs
def number_filter(guess):
    if len(guess)!=4:
        return False
    for digit in guess:
        if not digit.isdigit() or int(digit)>5:
            return False
    return True

#Method for Checking Guess Accuracy
def check_guess(guess):
    global guess_feedback, plus_feedback, minus_feedback, secret_code, secret_code_check, win_flag
    

    for i in range(4):
        if guess[i] == secret_code_check[i]:
            plus_feedback += '+'
            guess[i] = 'X'
            secret_code_check[i]= 'X'
    for k in range(4):
        for j in range(4):      
            if guess[k] == secret_code_check[j] and guess[k]!= 'X':
                minus_feedback += '-'
                guess[k] = 'X'
                secret_code_check[j]= 'X'    
    guess_feedback = plus_feedback+minus_feedback
    secret_code_check = secret_code.copy()
    return guess_feedback

while True:
    #Initialize Game
    if state == 0:
        win_flag = False
        loss_flag = False
        attempts = 0
        invalid_guess = False
        grid = list("+---+---+---+---+\n|   |   |   |   |    \n+---+---+---+---+\n|   |   |   |   |    \n+---+---+---+---+\n|   |   |   |   |    \n+---+---+---+---+\n|   |   |   |   |    \n+---+---+---+---+\n|   |   |   |   |    \n+---+---+---+---+\n|   |   |   |   |    \n+---+---+---+---+\n|   |   |   |   |    \n+---+---+---+---+\n|   |   |   |   |    \n+---+---+---+---+\n|   |   |   |   |    \n+---+---+---+---+\n|   |   |   |   |    \n+---+---+---+---+\n|   |   |   |   |    \n+---+---+---+---+\n|   |   |   |   |    \n+---+---+---+---+\n")
        guess_feedback = ""
        plus_feedback = ""
        minus_feedback = ""
        secret_code = random.choices('012345', k = 4)
        secret_code_check = secret_code.copy()
        state = 1
    
    #Title Screen
    if state == 1:
        if not replay_flag:
            print(start_mess)
        
            while True:
                yes = input('')
                if yes:
                    break
            while True:
                print("Would you like to play the game in grading mode? \nPress y to enter grading mode or any other key for challenge mode.")
                yes = input('')
                if yes == ('y'):
                    grading_mode = True
                    break
                else:
                    break
                    
        state = 2
    
    #Wait for User Input/Display Grid
    if state == 2:
        print("Mastermind! Try to Break the Code.\n Wins: " + str(wins) + "\n Losses: " + str(losses))
        print("".join(grid))
        if invalid_guess:
            print("Input is Invalid")
            invalid_guess = False
        if grading_mode:
            print('Code to Break:'+ "".join(secret_code))

        print('\nEnter a 4-Digit Guess: ')
        
        while True:
            guess = input('')
            if guess:
                break
        if number_filter(guess):
            state = 3
            attempts += 1
        else:
            invalid_guess= True
    
    #Update Grid and Check Guess
    if state == 3:
        for i in range(4):
            location = 20+40*(12-attempts)+4*i
            grid[location] = guess[i]
        
        check_guess(list(guess))
        

        for j in range(len(guess_feedback)):
            location = 35+40*(12-attempts)+j
            grid[location] = guess_feedback[j]
            

        
        print("".join(grid))
        if guess_feedback == ('++++'):
            win_flag = True
        if attempts == 12 and guess_feedback != ('++++'):
            loss_flag = True
            
        guess_feedback = ""
        plus_feedback = ""
        minus_feedback = ""
        
        state = 4
        
    #Check Win/Loss    
    if state == 4:
        if win_flag:
            wins += 1
            print("You win! Press y to Play Again.")
            while True:
                yes = input('')
                if yes == ('y'):
                    state = 0
                    replay_flag = True
                    break
                else: 
                    state = 5
                    break
        elif loss_flag:
            losses += 1
            print("You lose! Press y to Play Again.")
            while True:
                yes = input('')
                if yes == ('y'):
                    state = 0
                    replay_flag = True
                    break
                else: 
                    state = 5
                    break
        else:
            state = 2
            
    #Exit Game        
    if state == 5:
        print("Thanks for Playing!\n Total Wins: " + str(wins) + "\n Total Losses: " + str(losses))
        break
