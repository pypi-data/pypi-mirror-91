"""
 paradec decorator removes the need for change the input type of a function when running concurrent.futures.
 
 IMPORTANT: the placement of your variables are still important
"""

import sys

def parallel(function=None):
    if function != None:
        def wrapper(all_inputs):
            input_length=len(all_inputs)
            input_names = function.__code__.co_varnames[:input_length]
            args = {i:j for i,j in zip(input_names, all_inputs)}
            return function(**args)
        return wrapper
    else:
        raise ValueError('Error: Paradec is decorator and need to be'
                         ' in front of a function to work.')

__all__ = [
    'parallel'
]