"""

HW1 - Mastermind Game
Written by Noah Tanner
ME 405 - Professor Refvem
Fall 2023

"""

# imports
import random

# definitions and initialization
# set state into for state automatically
state = 1
win_amount = 0
loss_amount = 0
false_guess = 0
correctness = ''
rep = 0

# print statements
empty_grid = """
    +−−−+−−−+−−−+−−−+
    |   |   |   |   |
    +−−−+−−−+−−−+−−−+
    |   |   |   |   |
    +−−−+−−−+−−−+−−−+
    |   |   |   |   |
    +−−−+−−−+−−−+−−−+
    |   |   |   |   |
    +−−−+−−−+−−−+−−−+
    |   |   |   |   |
    +−−−+−−−+−−−+−−−+
    |   |   |   |   |
    +−−−+−−−+−−−+−−−+
    |   |   |   |   |
    +−−−+−−−+−−−+−−−+
    |   |   |   |   |
    +−−−+−−−+−−−+−−−+
    |   |   |   |   |
    +−−−+−−−+−−−+−−−+
    |   |   |   |   |
    +−−−+−−−+−−−+−−−+
    |   |   |   |   |
    +−−−+−−−+−−−+−−−+
    |   |   |   |   |
    +−−−+−−−+−−−+−−−+
    """
list_empty_grid = []
for let in empty_grid:
    list_empty_grid.append(let)
wins = "wins: "
losses = "losses: "
start_text = """                    Welcome to the game of Mastermind!

            You will be the codebreaker. Try to break the secret code by entering 4-digit
            codes using the numbers 0-5. Your guesses will be marked with a (+) symbol for
            each correct value in the correct location and a (-) for each correct value in
            an incorrect location.

                                        Press enter to begin
            """
new_game = "Mastermind! Try to break the code. \n"


# grid layout for the beginning of the game

while True:
    if state == 1:
        # state 1 - setup
        # print starting text 
        print(start_text)
        
        while True:
            enter = input('')
            if not enter:
                break

        state = 2                                                   # set next state

        #correct_code = ''.join(random.choices('012345', k = 4))     # generate the random code to be guessed
        correct_code = '1024'
        

    # state 2 - guess
    if state == 2:
        # prints
        print(new_game)
        print(wins + ' ' + str(win_amount) + '\n')
        print(losses + ' ' + str(loss_amount) + '\n')
        print(empty_grid)

        while True: 
            enter = input('Enter a guess: ')
            for n in enter: 
                if n not in ['0', '1', '2', '3', '4', '5']:
                    false_guess += 1
                    True
            if false_guess != 0 or len(enter) != 4: 
                print('Invalid entry, try again')
            
            else:
                false_guess = 0
                break
        
        # start checking values now that we have a valid entry
        state = 3
                    
    # state 3 - first pass
    if state == 3:
        list_enter = [ val for val in enter ]
        list_correct_code = [ val for val in correct_code ]
        for idx in range(4):
            if list_enter[idx] == correct_code[idx]:
                correctness = correctness + '+'
                list_enter[idx] = 'X'                                   # set the idxs of temp lists to 'X' so they aren't reused later
                list_correct_code[idx] = 'X'
        state = 4

    # state 4 - second pass
    if state == 4:
        for i in range(4):
            for j in range(4):
                if list_enter[i] == list_correct_code[j] and list_enter[i] != 'X':
                    correctness = correctness + '-'
                    list_enter[idx] = 'X'                               # set the idxs of temp lists to 'X' so they aren't reused later
                    list_correct_code[idx] = 'X'

        # print results from second pass
        


    # state 5 - win
    if state == 5:
        pass

    # state 6 - lose
    if state == 6:
        pass
