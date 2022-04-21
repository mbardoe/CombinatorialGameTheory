from combogames.classes.impartialgame import ImpartialGame

try:
    from tinydb import TinyDB, Query
except:
    try:
        import sqlite3
    except:
        pass


class TwoDimTopplingDominoes(ImpartialGame):

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
        self.find_connected_components()
        self._reduce()

    def _reduce(self):
        # self._repr=self.moves.copy()
        if len(self.moves) > 0:
            x_s = [s[0] for s in self.moves]
            y_s = [s[1] for s in self.moves]
            min_x = min(x_s)
            min_y = min(y_s)
            for move in self.moves:
                move = (move[0] - min_x, move[1] - min_y)

    def find_connected_components(self):  ##TODO: Fix and update to ImpartialGame
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

    def move(self, move, direction):  ##TODO: Fix and update to ImpartialGame
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

    # @property
    # def get_value(self) -> int: ##TODO: Fix and update to ImpartialGame
    #     if self._value:
    #         return self._value
    #
    #     else:
    #         if len(self.components) > 1:
    #             self._value = 0
    #             for component in self.components:
    #                 subgame = TwoDimTopplingDominoes(component)
    #                 self._value = self._value ^ subgame.get_value()
    #         else:
    #             if len(self.moves) == 0:
    #                 self.__record_value__(self.__db_repr__(), 0)
    #                 return 0
    #             else:
    #                 for move in big_subgame.moves:
    #                     for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
    #                         subgame = self.move(move, direction)
    #                         subgames.append(subgame.get_value())
    #                 self._value = mex(subgames)
    #     self.__record_value__(self.__db_repr__(), self._value)
    #
    #     return self._value

    def possible_moves(self):
        ans = set([])
        for move in self.moves:
            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                subgame = self.move(move, direction)
                ans.add(subgame)
        return ans

    @classmethod
    def generateRect(cls, dim):
        moves = []
        for i in range(dim[0]):
            for j in range(dim[1]):
                moves.append((i, j))
        return TwoDimTopplingDominoes(moves)

    @classmethod
    def generateL(cls, up, right):
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
    # for i in range(1,11):
    #     for j in range(1,11):
    #
    #         x = TwoDimTopplingDominoes.generateL(i,j)
    #         print(x)
    #         print(f"{i}, {j}, {x.nim_value})
    x = TwoDimTopplingDominoes.generateL(3, 2)
    print(x)
    for move in x.possible_moves():
        print(move)
        print(move.nim_value)
    # print(x.nim_value)
