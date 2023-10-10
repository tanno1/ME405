'''!@file                       main.py
    @brief                      main file for lab0x02 in me405
    @details                    cal poly, san luis obispo me405 lab project
    @author                     noah tanner, kosimo tonn
    @date                       october, 2023
'''

class Encoder:
    '''!@brief                  interface with quadrature encoders
        @details
    '''

    def __init(self):
        '''!@brief              creates an encoder object
            @details
            @param
        '''
        pass

    def update(self):
        '''!@brief              updates encoder position and delta
            @details
        '''
        pass

    def get_position(self):
        '''!@brief              gets the most recent encoder position
            @details
            @return
        '''
        pass

    def get_delta(self):
        '''!@brief              gets the most recent encoder delta
            @details
            @return
        '''
        pass

    def zero(self):
        '''!@brief              resets the encoder position to zero
            @details
        '''
        pass