from partizangame import PartizanGame
import networkx as nx
import networkx.algorithms.isomorphism as iso
import copy
try:
    from tinydb import TinyDB, Query
except:
    try:
        import sqlite3
    except:
        pass

class RedBlueCherries(PartizanGame):
    def __init__(self, num_nodes, edges, piles, filename="redbluecherries.db"):
        """Creates an instance of a game of Red Blue Cherries. Red Blue Cherries
        is played by defining a graph where the nodes are either red or blue. One
        player is red the other is blue. A player may move by removing a node of
        smallest degree that is their color. The game is over when one player
        does not have a move. That player is the loser.

        Agrs:
            num_nodes (int):    How many nodes will be in the graph.
            edges (list):   A list of tuples that define the edges of the graph.
            piles (list):   A list of strings ('r' and 'b') that define
                            the value of each node of the graph.
            filename (str):     The filename of the database file we use.

        Returns:
            RedBlueCherries object.

        """

        self.__filename__=filename
        super(RedBlueCherries,self).__init__(**{'filename': self.__filename__})
        self.graph=nx.Graph()
        self.graph.add_nodes_from(range(num_nodes))
        self.graph.add_edges_from(edges)
        for i in range(num_nodes):
            self.graph.node[i]['piles']=piles[i]



    def __repr__(self):
        """Creates a string to print out as a representation of the game.

        Returns:
            str: A string that describes the game.
        """
        return "".join([str(self.graph.degree()),"\n", str(self.get_piles())])

    def __db_repr__(self):
        """Creates the database representation of the game.

        Returns:
            str: A string that list the piles in increasing order.
        """
        ### what about super when you inherit from 2 classes?
        return str(nx.incidence_matrix(self.graph))+str(self.get_piles())

    def get_piles(self):
        """Returns a list indicating the value of each node.

        Returns:
            list: A list of strings ('r' and 'b').

        """
        piles_dict=nx.nx.get_node_attributes(self.graph,'piles')
        return [piles_dict[i] for i in range(self.graph.number_of_nodes())]

    def possible_moves(self):
        """Compute all other games that are possible moves from this position.

        Returns:
            A list of the games that are all the possible moves from the given
            game.
        """
        ## this needs to be tested
        moves={'left':[], 'right':[]}
        nodes = self.find_min_nodes()
        for node in nodes:
            edges=copy.deepcopy(self.graph.edges())
            piles=copy.deepcopy(self.get_piles())
            nodes=int(self.graph.number_of_nodes())
            g=RedBlueCherries(nodes,edges,piles)
            g.remove_node(node)
            if self.graph.node[node]['piles']=='r':
                moves['right'].append(g)
            else:
                moves['left'].append(g)
        return moves

    def remove_node(self, node):
        """Removes a node from the graph. The graph is also re-indexed.

         Args:
            node (int): The index of the node that needs to be removed.
        """
        self.graph.remove_node(node)
        self.__validate__()

    def __validate__(self):
        """Makes sure the graph is indexed from 0 to n-1. Where n is the number
         of nodes.
        """
        ## make sure that no piles are zero.
        ## this needs to be tested.
        self.__rename_names__()

    def __eq__(self, other):
        """ Determines if two redbluecherry games are equal.

        Args:
            other (RedBlueCherries object): Another Red Blue Cherries game.

        Returns:
            bool: True if the graphs are isomorphic and the labels are the same.
        """
        nm = iso.categorical_node_match('piles',0)
        return nx.is_isomorphic(self.graph, other.graph, node_match=nm)

    @property
    def value(self):
        '''Calculates the value of this game via a depth search
        of possible moves.


        :return: int that is the equivalent game.
        '''
        result=self.lookup_value()
        if result<0:
            ## Here will calculate the base cases by hand
            if self.graph.number_of_nodes()==1:
                if self.graph.node[0]['piles']=='r':
                    return -1
                else:
                    return 1
            ## Here we will use a breadth search
            else:
                result = self.__tree_search__()
            self.__record_value__(self.__db_repr__(),result)
        return result

    ##### Graph Algorithms #######

    def find_min_nodes(self):
        """Finds the nodes of minimal degree.

         Returns:
            list: A list of integers which are the indexes of nodes of minimal
                    degree.
        """

        degrees=self.graph.degree()
        min_degree=min(degrees.values())
        return [key for key in degrees.keys() if degrees[key]==min_degree]

    def degree(self):
        """ Returns the degrees of each node.

        Returns:
            dict: A dictionary index by node indexes and whose values are the
                degree of that node.
        """
        return self.graph.degree()

    def __rename_names__(self):
        """Changes the labelling of the vertices so that they correspond to
        smaller number indicate a leaf with small pile numbers.
        """
        self.graph = nx.convert_node_labels_to_integers(self.graph)



def main():
    x=RedBlueCherries(5, [(0,1),(1,2),(2,3),(3,4)], ['b','r','r','r','b'] )
    #x.nim_value()
    #print x.find_min_nodes()
    print x.value


if __name__ == '__main__':
    main()