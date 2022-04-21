import sys  #get rid of this...
import os

try:
    from tinydb import TinyDB, Query
except:
    try:
        import sqlite3
    except:
        pass


class CombinatorialGame:
    """A base class for investigating impartial combinatorial games.

        One goal of this class is create methods that allow for back searches
        of previously computed games. This class can utilize either tinyDB or
        sqlite3 to record the values of games that have been computed. The goal
        is to make the computation of larger games much faster. 

        Args:
            mylist: the list of integer piles sizes for the game

            filename: the path for the database file. To be saved in
            __filename__.
        """

    def __init__(self, **kwargs):

        #self.piles=list(mylist)
        if 'filename' in kwargs.keys():
            basepath = os.path.dirname(os.path.abspath(__file__))
            #print "combgame: "+path
            #basepath = os.path.dirname(os.getcwd())
            parentpath = os.path.dirname(os.path.dirname(basepath))
            #print 'parentpath= '+str(parentpath)
            #self.__filename__='../data/'+kwargs['filename']
            self.__filename__ = parentpath + '/data/' + kwargs['filename']
        else:
            raise SyntaxError('Need at least a filename argument')

        if 'tinydb' not in sys.modules:
            self.__filename__ = self.__filename__[:-3] + "SQL.db"
        #self.__validate__()
        #print os.path
        self.__get_dictionary__()

    def __get_dictionary__(self):
        """Set up the database file for this game. The path is stored
        as self.__filename__.
        """

    def lookup_value(self):
        """Looks up the value of a previously computed game.

        If the game has not been computed already, then the function may return
        None or -1. (Probably need to fix this in the future.)


        Returns:
            The value of the game that is list in the database or -1 if it
            can't be found in the database.

        """
        return None

    def __record_value__(self, game_id, ans):
        """Store values in the database.

        Args:
            game_id (str): is a string that can be used to uniquely
                identify each game.
            ans (int): is an integer that represents its the nim
                value of the game.
        """
        pass

    def __validate__(self):
        """This is make sure the form of the input is valid for this game.

        It also makes sure that the piles in a specific order.
        """
        pass


    def __db_repr__(self):
        """A string representation that will be unique and used as the lookup
        in the database.
        Returns:
            str: A unique string that identifies the game as an
                identification in the database
        """
        pass

    def possible_moves(self):
        """Compute all other games that are possible moves from this position.

        Returns:
            set: A set of the games that are all the possible moves from the
                given game."""

        return set([])

    def __repr__(self):
        '''How the game will be represented in python print statements.'''
        return str(self.__db_repr__())

    def __hash__(self):
        return hash(self.__db_repr__())

    def __eq__(self, other):
        return set(self.moves) == set(other.moves)

    def __str__(self):
        return str(self.moves)
