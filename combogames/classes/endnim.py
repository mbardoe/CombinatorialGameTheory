from impartialgame import ImpartialGame

try:
    from tinydb import TinyDB, Query
except:
    try:
        import sqlite3
    except:
        pass


class EndNim(ImpartialGame):
    """ A class that will represent an EndNim Game.
	It has takes in an ordered list [a,b,c,...,z]
	and makes it into a game of the form
	a--b--c---...---z.


    Arguments:

        piles (list): a list integers of sizes of piles

        filename (str): string of the path of the database

    Returns:
        ImpartialGame: An EndNim game object
    """

    def __init__(self, *args, **kwargs):

        if args and len(kwargs) == 1:
            self.piles = list(args[0])
            self.__filename__ = str(kwargs['filename'])
        elif len(args) == 2:
            self.piles = list(args[0])
            self.__filename__ = str(args[1])
        elif 'filename' in kwargs.keys() and 'piles' in kwargs.keys():
            self.__filename__ = str(kwargs['filename'])
            self.piles = list(kwargs['piles'])
        elif len(args) == 1 and len(kwargs.keys()) == 0:
            self.piles = list(args[0])
            self.__filename__ = "endNim.db"
        kwargs = {'filename': self.__filename__}
        args = []
        if len(args) == 1:
            self.piles = list(*args[0])
        super(EndNim, self).__init__(**{'filename': self.__filename__})
        self.__validate__()


    def __validate__(self):
        newlist = [x for x in self.piles if x != 0]
        self.piles = newlist

    def __len__(self):
        """ Calculates the number of piles.

        Returns:
            (int): the number of piles.
        """
        return len(self.piles)

    def possible_moves(self):
        """Creates a list of possible moves from the given game.

        Returns:
            set: A set of the possible moves.
        """
        ans = set([])

        mylist = list(self.piles)
        originalFront = mylist[0]
        for i in range(self.piles[0]):
            mylist[0] = i
            #print "Test front"+str(mylist)
            ans.add(EndNim(mylist))
        mylist[0] = originalFront
        for i in range(self.piles[-1]):
            mylist[-1] = i
            #print "Test back"+str(mylist)
            ans.add(EndNim(mylist))
        return ans

    def __repr__(self):
        """Creates a string to print out as a representation of the game.

        Returns:
            str: A string that describes the game.
        """
        ans = ""
        for i in range(len(self.piles) - 1):
            ans += str(self.piles[i])
            ans += "---"
        ans += str(self.piles[-1])
        return ans

    def __db_repr__(self):
        """Creates the database representation of the game.

        Returns:
            str: A string that list the piles in increasing order.
        """
        if self.piles[0] > self.piles[-1]:
            self.piles.reverse()
        return self.__repr__()

    def __eq__(self, other):
        """Determine if to GalesNim games are equivalent.

            Args:
                other: Another GalesNim game.

            Result:
                bool: This gives a boolean describing if the two games are equal.
        """
        return (
            self.piles == other.piles or self.piles.reverse() == other.piles)


    @property
    def nim_value(self):
        """Calculates the nim value of this game via a depth search
            of possible moves.


            Returns:
                int: an integer that is the equivalent nim pile
            """
        result = self.lookup_value()
        if result < 0:
            if len(self) == 1:
                result = self.piles[0]

            elif len(self) == 2:
                result = self.piles[0] ^ self.piles[1]

            else:
                result = self.__tree_search__()
        self.__record_value__(self.__db_repr__(), result)
        return int(result)


def main():
    m = 15
    for i in range(10):
        x = EndNim([1, m, i + 1])
        print str(x) + "  " + str(x.nim_value)


if __name__ == '__main__':
    main()
