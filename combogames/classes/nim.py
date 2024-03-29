from combogames.classes.impartialgame import ImpartialGame


class Nim(ImpartialGame):
    """An object that gives a Nim Game. Nim is a piles game where players
    alternate moves. Each player can take as much as they want from any one
    pile. The game is over when there are no piles left. The winner is the
    player that removes the last pile.

    Args:
        piles (list): The first parameter which is a list of pile sizes.

        filename (str): what filename would you like to store results.

    Returns:
        Nim (object)
        """

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 1:
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
            self.__filename__ = "nim.db"
        kwargs = {'filename': self.__filename__}
        args = []
        super(Nim, self).__init__(**kwargs)
        self.__validate__()

    def __validate__(self):
        """This is make sure the form of the input is valid for this game.

		It also makes sure that the piles in a specific order.
		"""
        ## remove zeros from piles
        new_piles = [x for x in self.piles if x != 0]
        new_piles.sort()
        self.piles = list(new_piles)

    def __db_repr__(self):
        """
        A string representation that will be unique and used as the lookup in the database.

        Returns:
            A unique string that identifies the game as an identification in the database
        """
        ans = 0
        for i in range(len(self.piles)):
            ans += self.piles[i] * 10 ** i
        return str(ans)

    @property
    def nim_value(self):
        """
		Utilize a database of previously constructed values to speed computation.

		When the database does not have the answer it uses a depth search of other games
		to compute the value of the game.

		Returns:
			Then nim value of the game. If it can't find the value in the database it
			tries to find the value by calculating the nim values of all possible moves
			from the given game.
		"""

        game_id = self.__db_repr__()
        result = self.lookup_value()
        if result > 0:
            #print("Used database")
            ans = result
        else:

            ans = 0
            for i in self.piles:
                ans = ans ^ i
            self.__record_value__(game_id, ans)
        return ans

    def possible_moves(self):
        """Compute all other games that are possible moves from this position.

		Returns:
			A set of the games that are all the possible moves from the given
			game."""

        ans = set([])
        for i in range(len(self.piles)):
            for j in range(self.piles[i]):
                newPiles = list(self.piles)
                newPiles[i] = j
                ans.add(Nim(newPiles))
        return ans

