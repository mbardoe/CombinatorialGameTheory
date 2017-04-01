from combinatorialgametools import CombinatorialGame
from EndNim import EndNim
from igraph import *
try:
    from tinydb import TinyDB, Query
except:
    try:
        import sqlite3
    except:
        pass

class SpokeAndHub(CombinatorialGame, Graph):

    def __init__(self):
        self.__filename__="spokeandhub.db"
        super(SpokeAndHub,self).__init__(**{'filename': self.__filename__})

    def create(self, num_vertices, edges, piles):
        self.add_vertices(num_vertices)
        self.add_edges(edges)
        self.vs['piles']=list(piles)
        self.vs['names']=range(num_vertices)


    def __db_repr__(self):
        return str(self.__mod_prufer_code__())+str(self.vs['piles'])
        ## Prufer algorithm

    def __repr__(self):
        ### what about super when you inherit from 2 classes?
        return super.__repr__()

    def possible_moves(self):
        """Compute all other games that are possible moves from this position.

        Returns:
            A list of the games that are all the possible moves from the given
            game.
        """
        ## this needs to be tested
        moves=[]
        leaves = self.find_leaves()
        for leaf in leaves:
            for i in range(self.vs['piles'][leaf]):
                g=self.copy()
                #g.add_vertices(len(self.vcount()))
                #g.add_edges(self.get_edgelist())
                g.vs['piles'][leaf]=i
                g.__validate__()
                moves.append(g)
        return moves


    def __validate__(self):
        ## make sure that no piles are zero.
        ## this needs to be tested.
        try:
            newPiles = [i for i in self.vs['piles'] if i!=0]
            while len(newPiles)>self.vcount:
                ### remove the vertex... relabel the graph with smaller numbers
                index=self.vs['piles'].index(0)
                name=self.vs[index]['names']
                self.delete_vertices(index)
                fix_Names_Indices = [i for i in range(self.vcount()) if self.vs[i]['names']>=name]
                for i in fix_Names_Indices:
                    self.vs[i]['names']-=1
                newPiles = [i for i in self.vs['piles'] if i!=0]
        except:
            pass
        self.__rename_names__()

    def __eq__(self, other):
        return self.__db_repr__()==other.__db_repr__()

    # @property
    # def nim_value(self):
    #     '''Calculates the nim value of this game via a depth search
    #     of possible moves.
    #
    #
    #     :return: int that is the equivalent nim pile
    #     '''
    #     result=self.lookup_value()
    #     if result<0:
    #         ## Here will calculate the base cases by hand
    #         if self.linear():
    #             endnimgame=self.convert_To_EndNim()
    #             result = endnimgame.nim_value
    #         ## Here we will use a breadth search
    #         else:
    #             result = self.__tree_search__()
    #         self.__record_value__(self.__db_repr__(),result)
    #     return result

    ##### Graph Algorithms #######

    def find_leaves(self):
        return [i for i,val in enumerate(self.degree()) if val==1]

    def find_leaf_with_minimum_label(self):
        '''Returns the index of the vertex that is a leaf of minimal
        label.'''
        leaf_positions = self.find_leaves()
        labels_of_leaves = [self.vs[i]['piles'] for i in leaf_positions]
        return leaf_positions[labels_of_leaves.index(min(labels_of_leaves))]

    def __rename_names__(self):
        '''Changes the labelling of the vertices so that they correspond to
        smaller number indicate a leaf with small pile numbers.'''
        g=self.copy()
        #copy_g=mygraph.copy()
        while g.vcount()>1:
            leaf_position=g.find_leaf_with_minimum_label()
            curname=g.vs[leaf_position]['names']
            copy_g_leaf_position=self.vs['names'].index(curname)
            min_name=min(g.vs['names'])
            index_min=self.vs['names'].index(min_name)
            #if g.vs[leaf_position]['piles']==copy_g.vs[index_min]['piles']:

            self.vs[index_min]['names']=curname
            self.vs[copy_g_leaf_position]['names']=min_name
            g.vs[index_min]['names']=curname
            g.delete_vertices(leaf_position)
        #return copy_g

    def linear(self):
        '''determine if the graph is a linear graph. Returns a boolean.'''
        # this code is currently wrong.
        #return self.degree()[1]==2 and self.degree()[2]==self.vcount()-2
        return False

    def convert_To_EndNim(self):
        '''This method checks to see if a spoke and hub game is equivalent
        to a linear game, and then returns the equivalent EndNim game.

        '''
        if self.linear():

            current=self.find_leaves()[0];
            last=None
            ans=[current]
            while len(ans)<self.vcount():
                neigh=self.neighbors(current)
                if neigh[0] in ans:
                    ans.append(neigh[1])
                else:
                    ans.append(neigh[0])
            piles=[self.vs[i]['piles'] for i in ans]
            return EndNim(piles)

        else:
            return None

    def __mod_prufer_code__(self):
            """Returns with the Prufer code

            Returns
            -------
            With a Prufer code as a list of vertex names if
            the network is a tree, else with None.

            """
            #net = self.copy()
            g=self.copy()
            prufer_code = []
            # Check if it is a tree
            vc = g.vcount()
            ec = g.ecount()
            if ec == vc -1 and g.is_connected():
                # Now that we know it is a tree.
                while g.vcount() > 1:
                    ## find a leaf with minimum label.
                    # leaf = net.degree().index(1)
                    leaf = g.find_leaf_with_minimum_label()
                    neig = g.neighbors(leaf)[0]
                    name = int(g.vs[neig]["names"])
                    neig_info=(name,g.vs[neig]['piles'])
                    leaf_info=(int(g.vs[leaf]["names"]), g.vs[leaf]['piles'])
                    prufer_code.append((neig_info, leaf_info))
                    g.delete_vertices(leaf)
                return prufer_code

def main():
    x=SpokeAndHub()
    x.add_vertices(4)
    x.add_edges([(0,1),(0,2),(0,3)])
    x.vs['piles']=[3,3,3,3]
    x.vs['names']=[0,1,2,3]
    x.nim_value()


if __name__ == '__main__':
    main()