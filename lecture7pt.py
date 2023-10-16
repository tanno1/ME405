def taskGenFun():

    state = 0
    count = 0

    # run forever!
    while True:
        if state == 0:
            # run state 0 code
            print(f"state = {state}")
            state = 1

        elif state == 1:
            # run state 1 code
            print(f"state = {state}")
            state = 2

        elif state == 2:
            # run state 2 code
            print(f"state = {state}")
            if count == 2:
                state = 1
                count = 0

        else:
            count += 1
            raise ValueError("Invalid State")

        yield state

# create task obj as generator object
task1 = taskGenFun()

while(True):
    next(task1)