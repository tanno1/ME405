import time

S0_INIT = 0
S1_RUN = 1
S2_RUN_THRICE = 2

def taskGenFun():
    state = 0
    count = 0
    yield state

    # run forever!
    while True:
        if state == S0_INIT:
            # run state 0 code
            print(f"state = {state}")
            state = S1_RUN

        elif state == S1_RUN:
            # run state 1 code
            print(f"state = {state}")
            state = S2_RUN_THRICE

        elif state == S2_RUN_THRICE:
            # run state 2 code
            print(f"state = {state}")
            if (count == 2):
                state = S1_RUN
                count = 0

            else:
                count += 1
    
        else:
            raise ValueError("Invalid State")

        yield(state)

# create task obj as generator object
task1 = taskGenFun()

while(True):
    next(task1)