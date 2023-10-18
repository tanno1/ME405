# generator functions

def collatz(n: int):
    if type(n) is not int:
        raise TypeError("input must be an integer")
    if n < 1:
        raise ValueError("input must be positive")
    
    # start by yielding the initial seed value to start sequence
    yield n
    
    # apply general case until hitting stop condition
    while n != 1:

        # even values of n
        if n % 2 == 0:
            n //= 2          # integer divide
        
        # odd values of n
        else: 
            n = 3*n + 1
        
        # yield after each operation
        yield n
    return None

# create collatz sequence through instancing (obj)
myseq = collatz(24)

# print each val throughout the gen function
for myVal in myseq:
    print(myVal)

my_list = list(collatz(39))
print(my_list)