"""

HW1 - Mastermind Game
Written by Noah Tanner
ME 405 - Professor Refvem
Fall 2023

"""

# definitions and initialization
# set state into for state automatically
state = 1

# print statements
# start text for the beginning of the game
start_text = """
                            Welcome to the game of Mastermind!

        You will be the codebreaker. Try to break the secret code by entering 4-digit
        codes using the numbers 0-5. Your guesses will be marked with a (+) symbol for
        each correct value in the correct location and a (-) for each correct value in
        an incorrect location.

                                    Press enter to begin
        """
# grid layout for the beginning of the game
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

while True:
    if state == 1:
        # state 1 - setup
        # this state will print the starting game message, and await for an 'enter' value in order to move onto the next state and start the game

        print(start_text)


    # state 2 - guess

    # state 3 - invalid guess

    # state 4 - correct value 

    # state 5 - wrong value

    # state 6 - misplaced value

    # state 7 - win

    # state 8 - lose