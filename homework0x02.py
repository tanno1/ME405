# -*- coding: utf-8 -*-
"""
Homework 0x02
@author: kozyt
"""
import time

def fibonacci(n):
    # Check for invalid seeds first
    if type(n) is not int:
        raise TypeError('Input must be an integer')
    if n < 1:
        raise ValueError('Input must be positive')
    
    a, b = 0, 1
    for value in range(n):
        yield a
        a, b = b, a + b
        
if __name__ == "__main__":
    values = [1, 5, 7, 7.5, -5, "asdf", 1000000]
    for n in values:
        try:
            for number in fibonacci(n):
                print(number)
        
            total_sum = 0
            start_time = time.perf_counter()
            for i, number in enumerate(fibonacci(n)):
                if i % 3 == 0:
                    total_sum += number
            end_time = time.perf_counter()           
            print("Sum of every third Fibonacci number: " + str(total_sum))
            print("Time Elapsed in seconds: " + str(end_time-start_time)+"\n")
            
        except (TypeError, ValueError) as e:
            print(f"Error for input {n}: {e}")