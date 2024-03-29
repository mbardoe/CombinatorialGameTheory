from impartialgame import ImpartialGame
import networkx as nx
import networkx.algorithms.isomorphism as iso
import copy
import matplotlib.pyplot as plt

try:
    from tinydb import TinyDB, Query
except:
    try:
        import sqlite3
    except:
        pass


class SpokeAndHub(ImpartialGame):
    """Spoke and Hub Game object. It allows computations with this game.

    Args:

        num_nodes (int):    How many nodes will be in the graph.

        edges (list):   A list of tuples that define the edges of the graph.

        piles (list):   A list of integers that define the size of the pile at
                each node of the graph.

        filename (str):     The filename of the database file we use.

        Returns:

            SpokeAndHub object.
        """

    def __init__(self, num_nodes, edges, piles, filename="spokeandhub.db"):


        self.__filename__ = filename
        super(SpokeAndHub, self).__init__(**{'filename': self.__filename__})
        #print self.__filename__
        self.graph = nx.Graph()
        self.graph.add_nodes_from(range(num_nodes))
        self.graph.add_edges_from(edges)
        for i in range(num_nodes):
            self.graph.node[i]['piles'] = piles[i]


    def __repr__(self):
        """Creates a string to print out as a representation of the game.

        Returns:
            str: A string that describes the game.
        """
        return "".join([str(self.graph.degree()), "\n", str(self.get_piles())])

    def __db_repr__(self):
        """Creates the database representation of the game.

        Returns:
            str: A string that list the piles in increasing order.
        """
        ### what about super when you inherit from 2 classes?
        return str(nx.incidence_matrix(self.graph)) + str(self.get_piles())

    def get_piles(self):
        """A method to report the size of the pile for each node of the graph.

         Returns:
            list: A list of integers with the pile sizes.
        """
        piles_dict = nx.nx.get_node_attributes(self.graph, 'piles')
        return [piles_dict[i] for i in range(self.graph.number_of_nodes())]

    def possible_moves(self):
        """Compute all other games that are possible moves from this position.

        Returns:
            A list of the games that are all the possible moves from the given
            game.
        """
        moves = []
        leaves = self.find_leaves()
        for leaf in leaves:
            for i in range(self.graph.node[leaf]['piles']):
                edges = copy.deepcopy(self.graph.edges())
                piles = copy.deepcopy(self.get_piles())
                nodes = int(self.graph.number_of_nodes())
                g = SpokeAndHub(nodes, edges, piles)
                g.graph.node[leaf]['piles'] = i
                g.__validate__()
                if g not in moves:
                    moves.append(g)
        return moves

    def __validate__(self):
        """Makes sure that if the pile size is zero we remove that node.
        """
        ## make sure that no piles are zero.
        ## this needs to be tested.
        try:
            for node in self.graph.nodes():
                if self.graph.node[node]['piles'] == 0:
                    self.graph.remove_node(node)
        except:
            pass
        self.__rename_names__()

    def __eq__(self, other):
        nm = iso.categorical_node_match('piles', 0)
        return nx.is_isomorphic(self.graph, other.graph, node_match=nm)

    @property
    def nim_value(self):
        '''Calculates the nim value of this game via a depth search
        of possible moves.


        Returns:
            int: An integer that is the equivalent nim pile.
        '''
        result = self.lookup_value()
        if result < 0:
            ## Here will calculate the base cases by hand
            if self.graph.number_of_nodes() == 2:
                piles = self.get_piles()
                result = piles[0] ^ piles[1]
            ## Here we will use a breadth search
            else:
                result = self.__tree_search__()
            self.__record_value__(self.__db_repr__(), result)
        return result

    ##### Graph Algorithms #######

    def find_leaves(self):
        """Finds the leaves of the graph. A leaf is a node with degree 1.

        Returns:
            list: A list of integers which are labels of nodes that are leaves.
        """

        degrees = self.graph.degree()
        return [key for key in degrees.keys() if degrees[key] == 1]

    def degree(self):
        """Calculates the dictionary of degrees of the various vertices of the
        graph.

        Returns:
            dict: A dictionary of the degrees of the nodes.
        """
        return self.graph.degree()

    def __rename_names__(self):
        """This function makes sure that the labels of the nodes are a list from
        0 to n-1. Where n is the number of nodes.
        """
        self.graph = nx.convert_node_labels_to_integers(self.graph)

    def show_graph(self):
        labels={}
        piles=self.get_piles()
        G = self.graph
        pos = nx.spring_layout(G)  # positions for all nodes
        for i in xrange(len(piles)):
            labels[i]=str(piles[i])

        pos_higher = {}
        # y_off = .1  # offset on the y axis
        # for k, v in pos.items():
        #     pos_higher[k] = (v[0], v[1] + y_off)
        nx.draw_networkx_labels(G, pos, labels, font_color='k')
        # nodes
        nx.draw_networkx_nodes(G, pos,
                               node_size=700,
                               alpha=0.8)
        #edges
        nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
        plt.axis('off')
        plt.show()  # display



def main():
    g = SpokeAndHub(6, [(0, 1), (1, 2), (2, 3), (3, 4), (3, 5)],
                    [1, 1, 1, 1, 1, 1])
    # x.nim_value()
    print(g.possible_moves())
    print(g.nim_value)
    g = SpokeAndHub(4, [(0, 1), (0, 2), (0, 3)], [9, 1, 6, 7])
    print(g)
    print(g.nim_value)


if __name__ == '__main__':
    main()