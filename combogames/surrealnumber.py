
class SurrealNumber(object):
    '''A class that represents a surreal number. Right now we will focus on
    surreal numbers that were born on a finite day.

    Attributes:
        left: (list) a list of the surreal numbers that are possible moves for
                    left.
        right: (list) a list fo the surreal numbers that are a possible move for
                right.

    Start with support for numbers, nimbers, and switches.
    '''

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def create_integer(cls,n):
        if n!=int(n):
            raise ValueError('{} is not an integer'.format(str(n)))
        if n<0:

            cls(right=[n+1])