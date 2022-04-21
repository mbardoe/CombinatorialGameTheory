from combogames.classes.redbluecherries import RedBlueCherries
import itertools


class RedBluePath(RedBlueCherries):
    ''' This class represents a Red-Blue Cherries where the structure of the
    graph is a path. When calculations are made sub-games are of the
    RedBlueCherries type.

    Example:
    g=RedBluePath('r','r','r','b','b','b')
    g.value
    0
    print(g)
    b---b---b---r---r---r
    -1  0   -1  1   0   1           0
    '''

    def __init__(self, *args):
        path_length = len(args)
        path_edges = []
        for i in xrange(path_length - 1):
            path_edges.append((i, i + 1))

        piles = list(args)
        super(RedBluePath, self).__init__(path_length, path_edges, piles)


    def __str__(self):
        '''This string method displays the path and the value of the entire
        game, and the value of each game formed by taking any node.'''
        ans = ''
        moves_dict = self.move_dict()
        for node in self.get_piles():
            ans += '{:-<5}'.format(node)
        ans = ans[:-4]
        ans += '\n'
        end_node = len(self.get_piles()) - 1
        # for n in [0,end_node]:
        #     ans+='{:<'+str(end_node*5)+'}'.format(moves_dict[n])
        ans += str(moves_dict[0]).ljust(5 * end_node) + str(
            moves_dict[end_node])
        #ans+=str(moves_dict[0]+'{:<')
        ans += '{:>20}'.format(self.value)
        return ans

    def move_dict(self):
        '''Returns a dictionary keyed on the number of each node and the value
        of the game that is returned by removing that node.

        Returns:
            dictionary: a dictionary keyed on the labelling of the node with
                        the value of the game formed by returning that node.
        '''
        ans = {}
        g = self.copy()
        g.remove_node(0)
        #print(g.value)
        ans[0] = g.value
        end_node = len(self.graph.node) - 1
        g = self.copy()
        g.remove_node(end_node)
        #print(g.value)
        ans[end_node] = g.value
        return ans

        # @staticmethod
        # def all_games(n):
        #     '''Static method that creates a list of games of particular length. Not
        #     a very efficient algorithm. Tests about 2^(n-3) options to find all the
        #     various possibilities.
        #
        #     Args:
        #         n (int): The length of the path.
        #
        #     Returns:
        #         list: A list of of all games of the given size.
        #
        #     '''
        #     piles=['b' for i in xrange(n)]
        #     games=[RedBluePath(*piles)]
        #     piles[-1]='r'
        #     new_piles=n*['b']
        #     for num_red in xrange(n/2):
        #         places=itertools.combinations(xrange(1,n-1),num_red)
        #         for spots in places:
        #             #print spots
        #             for i in xrange(n):
        #                 if i in spots or i==n-1:
        #                     new_piles[i]='r'
        #                 else:
        #                     new_piles[i]='b'
        #             g=RedBluePath(*new_piles)
        #             #print("Trying "+str(g))
        #             if g not in games:
        #                 #print('adding')
        #                 games.append(g)
        #     return games


def main():
    g = RedBluePath('r', 'b', 'r', 'r', 'r', 'b')
    print(g)


if __name__ == '__main__':
    main()