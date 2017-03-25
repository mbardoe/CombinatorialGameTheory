from igraph import *
try:
	from tinydb import TinyDB, Query 
except:
	try:
		import sqlite3 
	except:
		pass

class SpokeAndHub(Graph, CombinatorialGame):

	def __init__(self):
		self.__filename__="spokeandhub.db"
		self.__get_dictionary__()
		


	def __db_repr__(self):
		pass
		## Prufer algorithm 

	def __repr__(self):
		pass

	def possible_Moves(self):
		pass

	def __validate__(self):
		self.__rename_names__()


	def __eq__(self, other):
		pass

	def find_Nim_Value(self):
		result=self.lookup_Value()
		if result<0:
			## Here will calculate the base cases by hand 
			pass
			result=0
			## Here we will use a breadth search

			#else:
			#	result = self.__tree_search__()
			#self.__record_value__(self.__db_repr__(),result)
		return result
	##### Graph Algorigthms

	def find_leaves(self):
    	return [i for i,val in enumerate(self.degree()) if val==1]

    def find_leaf_with_minimum_label(g):
	    '''returns the index of the vertex that is a leaf of minimal 
	    label.'''
	    leaf_positions = self.find_leaves()
	    labels_of_leaves = [g.vs[i]['piles'] for i in leaf_positions]
	    return leaf_positions[labels_of_leaves.index(min(labels_of_leaves))]

	def __rename_names__(self):
		'''Changes the labelling of the vertices so that they correspond to 
		smaller number indicate a leaf with small pile numbers.'''
	    g=mygraph.copy()
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
	 	return g.degree()[1]==2 and g.degree()[2]=g.vcount()-2

	 def convert_To_EndNim(self):
	 	if self.linear():
	 		
	 		current=self.find_leaves()[0];
	 		last=None
	 		ans=[start]
	 		while len(ans)<self.vcount():
	 			neigh=g.neighbors(current)
	 			if neigh[0] in ans:
	 				ans.append(neigh[1])
	 			else:
	 				ans.append(neigh[0])
	 		piles=[g.vs[i]['piles'] for i in ans]
	 		return EndNim(piles)

	 	else:
	 		return None

def main():
	x=SpokeAndHub()
	x.add_vertices(4)
	x.add_edges([(0,1),(0,2),(0,3)])
	x.vs['piles']=[3,3,3,3]
	x.vs['names']=[0,1,2,3]
	x.find_Nim_Value()


if __name__ == '__main__':
	main()

