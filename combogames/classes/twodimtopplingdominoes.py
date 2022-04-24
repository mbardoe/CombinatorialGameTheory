from combogames.classes.impartialgame import ImpartialGame
from combogames.classes.tools import mdGridMaker

try:
    from tinydb import TinyDB, Query
except:
    try:
        import sqlite3
    except:
        pass


class TwoDimTopplingDominoes(ImpartialGame):
    """
    Two Dimensional Toppling Dominoes is an impartial game played on a grid of dominoes. Players take
    turns knocking down a domino in one of the cardinal directions and all dominos that are adjacent to that
    domino in a line fall down. The winner is the player to remove the last domino.
    """

    def __init__(self, *args, **kwargs):
        self.connected = False
        self.__filename__ = 'twodimtopplingdominoes.db'
        if len(args) > 0:
            self.moves = list(args[0])
        if 'moves' in kwargs.keys():
            self.moves = kwargs['moves']
        if 'connected' in kwargs.keys():
            self.connected = kwargs['moves']
        # self.nim_value = None
        super(TwoDimTopplingDominoes, self).__init__(**{'filename': self.__filename__})
        self.__validate__()

    def __validate__(self):
        """__validate__ is designed to find the connected components of the dominoes. There is
        also a goal of reducing the numbers to make it so that they are small as possible."""
        self.find_connected_components()
        self.__reduce__()

    def __reduce__(self):
        """__reduce__ is designed to reduce the numbers of the moves so that they are as small as possible but
        positive."""
        # self._repr=self.moves.copy()
        min_x, min_y, max_x, max_y = self.boundingBox()
        for move in self.moves:
            move = (move[0] - min_x, move[1] - min_y)

    def find_connected_components(self):
        """find_connected_components used to find connected components of the game."""
        self.components = []
        moves = self.moves.copy()
        current_component = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for move in moves:
            current_component.append(move)
            for move in current_component:
                for direction in directions:
                    neighbor = (move[0] + direction[0], move[1] + direction[1])
                    if neighbor in self.moves and not neighbor in current_component:
                        current_component.append(neighbor)
                        if neighbor in moves:
                            moves.remove(neighbor)
            self.components.append(current_component.copy())
            current_component = []

    def move(self, move, direction):
        """move is used to create a new game based on a particular move and a particular direction.

        Returns:
            TwoDimTopplingDominoes: the game you get when you move in the given way."""
        if move not in self.moves:
            raise ValueError
        else:
            moves = self.moves.copy()
            while move in moves:
                moves.remove(move)
                move = (move[0] + direction[0], move[1] + direction[1])
            ans = TwoDimTopplingDominoes(moves)
            # print(ans)
            # ans.get_value()
        return ans

    @property
    def nim_value(self):
        """Utilize a database of previously constructed values to speed computation.

                When the database does not have the answer it uses a depth search of other games
                to compute the value of the game.

                Returns:
                    int: Then nim value of the game. If it can't find the value in the database it
                        tries to find the value by calculating the nim values of all possible moves
                        from the given game.
                """
        result = self.lookup_value()
        if result < 0:
            if len(self.moves) == 0:
                result = 0
            else:
                if len(self.components) > 1:
                    result = 0
                    for component in self.components:
                        subgame = TwoDimTopplingDominoes(moves=component, connected=True)
                        result = result ^ subgame.nim_value
                else:
                    result = self.__tree_search__()
            self.__record_value__(self.__db_repr__(), result)
        return result

    def __str__(self) -> str:
        result = ""
        minx, miny, maxx, maxy = self.boundingBox()
        for height in range(maxy, miny - 1, -1):
            for width in range(minx, maxx + 1, 1):
                if (width, height) in self.moves:
                    result += "\u20DE"
                else:
                    result += " "
            result += "\n"
        return result

    def boundingBox(self):
        if len(self.moves) == 0:
            return 0, 0, 0, 0
        xes = [x[0] for x in self.moves]
        yes = [x[1] for x in self.moves]
        return min(xes), min(yes), max(xes), max(yes)

    def possible_moves(self):
        """Compute all other games that are possible moves from this position.

                Returns:
                    set: A set of the games that are all the possible moves from the given
                    game.
                """
        ans = set([])
        for move in self.moves:
            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                subgame = self.move(move, direction)
                ans.add(subgame)
        return ans

    @classmethod
    def generateRect(cls, dim):
        """Creates a TwoDimTopplingDominoes Game where there are a rectangle dominoes.
                        Args:
                            dim (tuple): How many rows and how many columns.
                            right (int): How many dominoes to the right.

                        Returns:
                            str: A string that list the piles in increasing order.
                        """

        moves = []
        for i in range(dim[0]):
            for j in range(dim[1]):
                moves.append((i, j))
        return TwoDimTopplingDominoes(moves)

    @classmethod
    def generateL(cls, up, right):
        """Creates a TwoDimTopplingDominoes Game where there are a line of _up_ dominoes going up
          and _right_ dominoes to the right in an L formation.
                Args:
                    up (int): How many dominoes up..
                    right (int): How many dominoes to the right.

                Returns:
                    str: A string that list the piles in increasing order.
                """
        moves = []
        for i in range(up):
            moves.append((0, i))
        for j in range(right):
            moves.append((j + 1, 0))
        return TwoDimTopplingDominoes(moves)

    def __db_repr__(self):
        return str(self.moves)

    def __repr__(self):
        return self.__db_repr__()


if __name__ == "__main__":
    ans = []
    max_size = 6
    for j in range(1, max_size):
        ans.append([TwoDimTopplingDominoes.generateL(i, j).nim_value for i in range(1, max_size)])
    print(mdGridMaker(range(1, max_size), range(1, max_size), ans))
    x = TwoDimTopplingDominoes.generateL(2, 3)
    print(x)
    print(x.nim_value)

    # for i in range(1, max_size):
    #     ans.append([])
    #     for j in range(1, max_size):
    #         x = TwoDimTopplingDominoes.generateRect((i, j))
    #         #         print(x)
    #         #         print(f"{i}, {j}, {x.nim_value})
    #         ans[i - 1].append(x.nim_value)
    # result = "| row/col |"
    # for i in range(1, max_size):
    #     result += f" {i} |"
    # result += "\n"
    # for i in range(1, max_size):
    #     result += f"| {i} |"
    #     for j in range(1, max_size):
    #         result += f" {ans[j - 1][i - 1]}|"
    #     result += "\n"
    # print(result)
    # # x=TwoDimTopplingDominoes.generateL(3,6)
    # # print(x)
    # # for move in x.possible_moves():
    # #     print(move)
    # #     print(move.nim_value)
    # #     #print(x.nim_value)
