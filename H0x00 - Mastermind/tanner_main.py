"""

HW1 - Mastermind Game
Written by Noah Tanner
ME 405 - Professor Refvem
Fall 2023

"""

# imports
import random
import sys

# definitions and initialization
# set state into for state automatically
state = 1
win_amount = 0
loss_amount = 0
false_guess = 0
correctness = ''
prev_correctness = 0
rep = 0
first_run = 0
spoiled_mode = 0

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
        if first_run == 0: 
            print(start_text)
            while True:
                enter = input('')
                if not enter:
                    break
            first_run += 1

        state = 2                                                   # set next state
        guess_count = 0                                             # initialize the guess count to 0 guesses, used for printing board

        correct_code = ''.join(random.choices('012345', k = 4))     # generate the random code to be guessed

        if first_run == 1: 
            first_run += 1
            print("Press 1 to play game in spoiled mode, otherwise press any key...")
            while True:
                spoiled = input('')
                if spoiled == '1' :
                    spoiled_mode = 1
                    break
                else:
                    break

        # new game prints
        print(new_game)
        print(wins + ' ' + str(win_amount))
        print(losses + ' ' + str(loss_amount))
        print(empty_grid)
        

    # state 2 - guess
    if state == 2:

        while True: 
            enter = input('Enter a guess: ')
            for n in enter: 
                if n not in ['0', '1', '2', '3', '4', '5']:
                    false_guess += 1
                    True
            for n in enter: 
                if n in ['0', '1', '2', '3', '4', '5']:
                    false_guess = 0
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
        for idx in range(0,4):
            if idx == 0: 
                list_empty_grid[-42-(44*guess_count)-prev_correctness] = enter[0]
            if idx == 1: 
                list_empty_grid[-38-(44*guess_count)-prev_correctness] = enter[1]
            if idx == 2: 
                list_empty_grid[-34-(44*guess_count)-prev_correctness] = enter[2]
            if idx == 3: 
                list_empty_grid[-30-(44*guess_count)-prev_correctness] = enter[3]
        
        # append the correctness count on the right side
        correctness_list = [str(let) for let in correctness]
        if guess_count == 0:
            index_to_insert = -27
        elif guess_count > 0:
            index_to_insert = -27 - (44* guess_count) - prev_correctness
        for val in correctness_list:
            list_empty_grid.insert(index_to_insert, val)
        #list_empty_grid.insert(index_to_insert, '\n')
        new_grid_print = ''.join(list_empty_grid)
        if spoiled_mode == 1:
            print('Code to break: ' + str(correct_code))
        print(new_grid_print)
        guess_count += 1                                            # increment guess count after each print, first go needs to have 0!
        for val in correctness:
            prev_correctness += 1
        correctness = ''                                            # reset correctness for next guess
        state = 5                                                   # set next state

    # state 5 - win
    if state == 5:
        if enter == correct_code:
            win_amount += 1
            print('You win!\n')
            again = input('Play again? Enter (y) for yes: ')
            if again == ('y' or 'Y'):
                # reinitialize all the relevant state vars and reset state to 1
                state = 1
                false_guess = 0
                correctness = ''
                prev_correctness = 0
                correctness = ''
                rep = 0
                list_empty_grid = []
                for let in empty_grid:
                    list_empty_grid.append(let)
            else:
                print('Thanks for playing!\n')
                print(' Total wins: ' + str(win_amount) + '\n' )
                print(' Total losses: ' + str(loss_amount) + '\n' )
                while True:
                    exit_program = input('Press enter to exit... ')
                    if exit_program == '':
                        sys.exit()
                    else:
                        'Welcome to the backrooms...'
        else:
            state = 6

    # state 6 - lose
    if state == 6:
        if guess_count == 12 and enter != correct_code:
            loss_amount += 1
            # loss conditions
            print('You lose!\n')
            again = input('Play again? Enter (y) for yes: ')
            if again == ('y' or 'Y'):
                # reinitialize all the relevant state vars and reset state to 1
                state = 1
                false_guess = 0
                correctness = ''
                prev_correctness = 0
                correctness = ''
                rep = 0
                list_empty_grid = []
                for let in empty_grid:
                    list_empty_grid.append(let)
            else:
                print('Thanks for playing!\n')
                print(' Total wins: ' + str(win_amount) + '\n' )
                print(' Total losses: ' + str(loss_amount) + '\n' )
                while True:
                    exit_program = input('Press enter to exit... ')
                    if exit_program == '':
                        sys.exit()
                    else:
                        'Welcome to the backrooms...'
            pass
        else:
            state = 2
