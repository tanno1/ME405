'''
    @name           main.py
    @brief          main file for hw0x02 - fibonacci generator
    @author         noah tanner
    @date           november 4th, 2023
'''

import time

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
        yield fib_first                                     # return current fib val, using tuple unpack without needing to make a temp var
        fib_first, fib_sec = fib_sec, fib_first + fib_sec   # calc next fib val
        idx += 1                                            # increment idx                                                


if __name__ == '__main__':

    lentest0 = 100
    print(f'test0 with length {lentest0} \n')
    test0 = fibonacci_gen(lentest0)
    for idx in range(lentest0):
        print(next(test0))

    print('\n')

    lentest1 = 10
    print(f'test1 with length {lentest1} \n')
    test1 = fibonacci_gen(lentest1)
    for idx in range(lentest1):
        print(next(test1))

    print('\n')

    test2 = fibonacci_gen('a')                                      # type error
    try:
        print(next(test2))
    except TypeError as te:
        print(f'Test 2 - Type error in gen func: {te}')

    print('\n')
    
    test3 = fibonacci_gen(-10)                                      # value error                                  
    try:
        print(next(test3))
    except ValueError as ve:
        print(f'Test3 - Value error in gen funct with: {ve}')

    print('\n')

    # 3rd value summation
    length1     = 10
    sumtest1    = fibonacci_gen(length1)
    sumres1     = 0

    start_time = time.perf_counter()
    for idx in range(length1):
        val = next(sumtest1)
        if idx % 3 == 0:
            sumres1 += val
    end_time = time.perf_counter()
    diff_time = end_time - start_time

    print(f'Elapsed time of \'sumtest1\': {diff_time} s \n')
    print(f'Sum of \'sumtest1\': {sumres1} \n')

    # 3rd value summation long test
    length2     = 100000
    sumtest2    = fibonacci_gen(length2)
    sumres2     = 0
    start_time = time.perf_counter()
    for idx in range(length2):
        val = next(sumtest2)
        if idx % 3 == 0:
            sumres2 += val
    end_time = time.perf_counter()
    diff_time = end_time - start_time

    print(f'Elapsed time of \'sumtest2\': {diff_time} s \n')
    print(f'Sum of \'sumtest2\':\n {sumres2} \n')

