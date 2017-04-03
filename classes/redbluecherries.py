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
        self.__filename__=filename
        super(RedBlueCherries,self).__init__(**{'filename': self.__filename__})
        self.graph=nx.Graph()
        self.graph.add_nodes_from(range(num_nodes))
        self.graph.add_edges_from(edges)
        for i in range(num_nodes):
            self.graph.node[i]['piles']=piles[i]



    def __repr__(self):
        return "".join([str(self.graph.degree()),"\n", str(self.get_piles())])

    def __db_repr__(self):
        ### what about super when you inherit from 2 classes?
        return str(nx.incidence_matrix(self.graph))+str(self.get_piles())

    def get_piles(self):
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
        self.graph.remove_node(node)
        self.__validate__()

    def __validate__(self):
        ## make sure that no piles are zero.
        ## this needs to be tested.
        self.__rename_names__()

    def __eq__(self, other):
        nm = iso.categorical_node_match('piles',0)
        return nx.is_isomorphic(self.graph, other.graph, node_match=nm)

    @property
    def value(self):
        '''Calculates the nim value of this game via a depth search
        of possible moves.


        :return: int that is the equivalent nim pile
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

        degrees=self.graph.degree()
        min_degree=min(degrees.values())
        return [key for key in degrees.keys() if degrees[key]==min_degree]

    def degree(self):
        return self.graph.degree()

    def __rename_names__(self):
        '''Changes the labelling of the vertices so that they correspond to
        smaller number indicate a leaf with small pile numbers.'''
        self.graph = nx.convert_node_labels_to_integers(self.graph)



def main():
    x=RedBlueCherries(5, [(0,1),(1,2),(2,3),(3,4)], ['b','r','r','r','b'] )
    #x.nim_value()
    print x.find_min_nodes()
    print x.value


if __name__ == '__main__':
    main()