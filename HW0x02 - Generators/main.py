'''
    @name           main.py
    @brief          main file for hw0x02 - fibonacci generator
    @author         noah tanner
    @date           november 4th, 2023
'''

def fibonacci_gen(length):
    # check for invalid lengths
    if type(length) is not int:
        raise TypeError("Length value must be an integer.")
    
    if length < 0:
        raise ValueError("Length must be a non-negative number.")

    # apply fib function
    fib_first   = 0
    fib_sec     = 1
    sum         = 0
    idx         = 0

    while idx < length:
        yield fib_first                                     # return current fib val
        fib_first, fib_sec = fib_sec, fib_first + fib_sec   # calc next fib val
        idx += 1                                            # increment idx                                                

test1 = fibonacci_gen(10)
for idx in range(10):
    print(next(test1))

test2 = fibonacci_gen('a')                                  # uncomment to test TypeError
try:
    print(next(test2))
except TypeError as te:
    print(f'Test 2 - Type error in gen func: {te}')

test3 = fibonacci_gen(-10)                                  # uncomment to test ValueError
try:
    print(next(test3))
except ValueError as ve:
    print(f'Test3 - Value error in gen funct with: {ve}')

# 3rd value summation

