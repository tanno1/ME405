"""

HW1 - Mastermind Game
Written by Noah Tanner
ME 405 - Professor Refvem
Fall 2023

"""

# definitions and initialization
# set state into for state automatically
state = 1
win_amount = 0
loss_amount = 0
false_guess = 0

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

        state = 2                           # set next state

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
                if n not in [0, 1, 2, 3, 4, 5] == True:
                    false_guess += 1
                    True
            if false_guess != 0: 
                print('Invalid entry, try again')
            if n in [0, 1, 2, 3, 4, 5] and len(enter) == 4:
                 False

    # state 3 - invalid guess
    if state == 3:
        pass

    # state 4 - correct value
    if state == 4:
        pass

    # state 5 - wrong value
    if state == 5:
        pass

    # state 6 - misplaced value
    if state == 6:
        pass

    # state 7 - win
    if state == 7:
        pass

    # state 8 - lose
    if state == 8:
        pass