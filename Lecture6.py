# lecture 6 notes on classes
# noah tanner
# fall 2023

'''
doc strings, used to document speciric entities, files, class def, func def, attributes, etc...
'''

class dog:
    '''!@brief (brief description of class) - dog class implementation
        @details (details of class) - dog class
    '''

    def __init__(self, dogName, dogWeight, dogAge)
        ''' !@brief
            @details
            @param dogName - [ description of dogName param ]
            @param dogWeight - [ description of dogWeight param ]
            @param dogAge - [ description of dogAge param ]
        '''

        # if we want to keep access to these class attributes, must store them by copying input param to attributes
        self.name = dogName
        self.weight = dogWeight
        self.age = dogAge