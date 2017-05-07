from redbluecherries import RedBlueCherries
import itertools


class RedBlueCycle(RedBlueCherries):
    ''' This class represents a Red-Blue Cherries where the structure of the
    graph is a cycle.
    '''

    def __init__(self, *args):

        cycle_length=len(args)
        cycle_edges=[]
        for i in xrange(cycle_length-1):
            cycle_edges.append((i,i+1))
        cycle_edges.append((0,cycle_length-1))
        piles=list(args)
        super(RedBlueCycle, self).__init__(cycle_length,cycle_edges,piles)


    def __str__(self):
        ans='---'
        moves_dict=self.move_dict()
        for node in self.get_piles():
            ans+='{:-<4}'.format(node)
        ans+='\n'
        for n in xrange(len(self.get_piles())):
            ans+='{:>4}'.format(moves_dict[n])
        ans+='{:>20}'.format(self.value)
        return ans

    def move_dict(self):
        ans={}
        for n in xrange(len(self.graph.node)):
            g=self.make_copy()
            g.remove_node(n)
            #print(g.value)
            ans[n]=g.value
        return ans



    @property
    def value(self):
        '''Calculates the value of this game via a depth search
        of possible moves.


        :return: int that is the equivalent game.
        '''
        result=self.lookup_value()
        if result is None:
            ## Here will calculate the base cases by hand
            if self.graph.number_of_nodes()==1:
                if self.graph.node[0]['piles']=='r':
                    return -1
                else:
                    return 1
            ## Here we will use a breadth search
            else:
                result = self.__tree_search__()
            #self.__record_value__(self.__db_repr__(),result)
        return result

    @staticmethod
    def all_games(n):
        piles=['b' for i in xrange(n)]
        games=[RedBlueCycle(*piles)]
        piles[-1]='r'
        new_piles=n*['b']
        for num_red in xrange(n/2):
            places=itertools.combinations(xrange(1,n-1),num_red)
            for spots in places:
                #print spots
                for i in xrange(n):
                    if i in spots or i==n-1:
                        new_piles[i]='r'
                    else:
                        new_piles[i]='b'
                g=RedBlueCycle(*new_piles)
                #print("Trying "+str(g))
                if g not in games:
                    #print('adding')
                    games.append(g)
        return games

def main():
    x=RedBlueCycle('b','b','b','r','r','r')
    #x.nim_value()
    print( x)
    print x.move_dict()
    print x.value
    y=x.possible_moves()
    for g in y['right']:
        print(g.value)
    print("left")
    for g in y['left']:
        print(g.value)
    print(x.simplest_between(0,0))
    y=RedBlueCycle('b','b','r','r','r','b')
    print (x==y)
    for g in RedBlueCycle.all_games(12):
        print(g)
        print('\n')
if __name__ == '__main__':
    main()