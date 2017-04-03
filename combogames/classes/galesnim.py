from impartialgame import ImpartialGame

try:
    from tinydb import TinyDB, Query
except:
    try:
        import sqlite3
    except:
        pass


class GalesNim(ImpartialGame):
    def __init__(self, *args, **kwargs):
        """

        :param args: piles, num_zero_piles, k, filename
        :param kwargs: piles, num_zero_piles, k, filename
        """
        self.number_Of_zero_piles = 0
        self.k = 1
        self.__filename__ = 'galesnim.db'

        if len(args) > 0:
            self.piles = list(args[0])
        if len(args) > 1:
            self.number_Of_zero_piles = int(args[1])
        if len(args) > 2:
            self.k = int(args[2])
        if len(args) > 3:
            self.__filename__ = str(args[3])


        if 'piles' in kwargs.keys():
            self.piles = kwargs['piles']
        if 'num_zero_piles' in kwargs.keys():
            self.number_Of_zero_piles = kwargs['num_zero_piles']
        if 'k' in kwargs.keys():
            self.k = kwargs['k']

        #self.piles = list(mylist)
        #self.number_Of_zero_piles = number_of_zero_piles
        #self.k = k
        super(GalesNim, self).__init__(**{'filename':self.__filename__})
        self.__validate__()
        #self.__filename__ = "galesnim.db"
        #self.__get_dictionary__()

    def __validate__(self):
        """__validate is designed to take the zeroes out of the piles. Should we
		keep the zeroes, or keep track of how many zero piles there are."""
        newPiles = [x for x in self.piles if x != 0]
        self.number_Of_zero_piles += len(self.piles) - len(newPiles)
        self.piles = newPiles

    @property
    def nim_value(self):
        """A method to find the nim value of the game"""
        result = self.lookup_value()
        if result < 0:
            if len(self.piles) - self.k == 0:
                result = 0
            else:
                result = self.__tree_search__()
            self.__record_value__(self.__db_repr__(), result)
        return result

    def possible_moves(self):
        """Compute all other games that are possible moves from this position.

        Returns:
            A set of the games that are all the possible moves from the given
            game.
        """
        ans = set([])
        for i in range(len(self.piles)):
            for j in range(self.piles[i]):
                new_piles = list(self.piles)
                new_piles[i] = j
                ans.add(GalesNim(new_piles, self.number_Of_zero_piles, self.k))
        return ans


    def __repr__(self):
        ans = "Game ends when all but " + str(self.k) + " are empty.\n"
        for i in range(len(self.piles)):
            ans += str(self.piles[i]) + "  "
        for i in range(self.number_Of_zero_piles):
            ans += "0  "
        return ans.strip()


    def __db_repr__(self):
        ans = str(self.k) + "_"
        new_Piles = list(self.piles)
        new_Piles.sort()
        for value in new_Piles:
            ans += str(value) + "_"
        #for i in range(self.number_Of_Zero_Piles):
        #	ans+="0 "
        return ans.strip()


    def __eq__(self, other):
        """Determine if to GalesNim games are equivalent.

            Args:
                other: Another GalesNim game.

            Result:
                This gives a boolean describing if the two games are equal.
            """
        myPiles = list(self.piles)
        theirPiles = list(other.piles)
        myPiles.sort()
        theirPiles.sort()
        return self.k == other.k and self.number_Of_zero_piles == \
                        other.number_Of_zero_piles and myPiles == theirPiles


def main():
    game = GalesNim([3, 4, 5], 0, 1)
    print game
    possMoves = game.possible_moves()
    for mygame in possMoves:
        print mygame


if __name__ == '__main__':
    main()