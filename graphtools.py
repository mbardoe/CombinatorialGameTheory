from igraph import *
def mod_prufer_code(mygraph):
    """Returns with the Prufer code

    Returns
    -------
    With a Prufer code as a list of vertex names if
    the network is a tree, else with None.

    """
    #net = self.copy()
    g=mygraph.copy()
    prufer_code = []
    # Check if it is a tree
    vc = g.vcount()
    ec = g.ecount()
    if ec == vc -1 and g.is_connected():
        # Now that we know it is a tree. 
        while g.vcount() > 1:
            ## find a leaf with minimum label.
            # leaf = net.degree().index(1)
            leaf = find_leaf_with_minimum_label(g)
            neig = g.neighbors(leaf)[0]
            name = int(g.vs[neig]["names"])
            neig_info=(name,g.vs[neig]['piles'])
            leaf_info=(int(g.vs[leaf]["names"]), g.vs[leaf]['piles'])
            prufer_code.append((neig_info, leaf_info))
            g.delete_vertices(leaf)
        return prufer_code

def find_leaf_with_minimum_label(g):
    '''returns the index of the vertex that is a leaf of minimal 
    label.'''
    leaf_positions = [i for i,val in enumerate(g.degree()) if val==1]
    labels_of_leaves = [g.vs[i]['piles'] for i in leaf_positions]
    
    return leaf_positions[labels_of_leaves.index(min(labels_of_leaves))]
    #return min(leaf_positions)

def rename_names(mygraph):
    g=mygraph.copy()
    copy_g=mygraph.copy()
    while g.vcount()>1:
        leaf_position=find_leaf_with_minimum_label(g)
        curname=g.vs[leaf_position]['names']
        copy_g_leaf_position=copy_g.vs['names'].index(curname)
        min_name=min(g.vs['names'])
        index_min=copy_g.vs['names'].index(min_name)
        #if g.vs[leaf_position]['piles']==copy_g.vs[index_min]['piles']:

        copy_g.vs[index_min]['names']=curname
        copy_g.vs[copy_g_leaf_position]['names']=min_name
        g.vs[index_min]['names']=curname
        g.delete_vertices(leaf_position)
    return copy_g




def main():
    g=Graph()
    g.add_vertices(5)
    g.add_edges([(0,1),(0,2),(1,3),(1,4)])
    g.vs['piles']=[4,3,2,2,1]
    g.vs['names']=range(g.vcount())
    print find_leaf_with_minimum_label(g)
    new_g=rename_names(g)
    print new_g.vs['piles']
    print new_g.vs['names']

    print mod_prufer_code(g)
    print mod_prufer_code(new_g)

if __name__ == '__main__':
    main()