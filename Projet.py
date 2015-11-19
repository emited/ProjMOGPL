""

########## Projet MOGPL : La balade du robot
########## 

########## DE BEZENAC Emmanuel - Groupe TD ???
########## SPORTICH Benjamin - Groupe TD ???

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
import numpy as np







################################################################################################################
#                                   GENERATION ALEATOIRE D'INSTANCES
################################################################################################################


################################################################################################################
#                                   LECTURE DE FICHIER
################################################################################################################

def readfile(filename):
    with open(filename) as f:
        M,N = [int(x) for x in f.readline().split()] # read first line
        array = []
        i=0
        for line in f: # read rest of lines
            if(i<M):
                array.append(np.array([int(x) for x in line.split()]))
                i+=1
            else:
                iStart,jStart,iEnd,jEnd=[int(line.split()[i]) for i in range(4)]
                startDir=line.split()[4]
                break
    return M,N,np.array(array),iStart,jStart,iEnd,jEnd,startDir

################################################################################################################
#                                   CREATION & GESTION DU GRAPHE
################################################################################################################

def genGraph(M,N,A):
    G=nx.DiGraph()
    for i in range(M+1):
        for j in range(N+1):
            if(A[i][j]==0 and A[i][j-1]==0 and A[i-1][j]==0 and A[i-1][j-1]==0):
                
                #Creation des noeuds - un par direction = 4 par position                
                G.add_node(str(i)+str(j)+'1',direct='N')
                G.add_node(str(i)+str(j)+'2',direct='E')
                G.add_node(str(i)+str(j)+'3',direct='S')
                G.add_node(str(i)+str(j)+'4',direct='O')

                #Creation des arcs
                #Changement de direction                
                G.add_edge(str(i)+str(j)+'1',str(i)+str(j)+'2',edge_color='b',direct='R',weight=1)
                G.add_edge(str(i)+str(j)+'1',str(i)+str(j)+'4',edge_color='b',direct='L',weight=1)
                G.add_edge(str(i)+str(j)+'2',str(i)+str(j)+'3',edge_color='b',direct='R',weight=1)
                G.add_edge(str(i)+str(j)+'3',str(i)+str(j)+'4',edge_color='b',direct='R',weight=1)

                G.add_edge(str(i)+str(j)+'2',str(i)+str(j)+'1',direct='L',weight=1)
                G.add_edge(str(i)+str(j)+'4',str(i)+str(j)+'1',direct='R',weight=1)
                G.add_edge(str(i)+str(j)+'3',str(i)+str(j)+'2',direct='L',weight=1)
                G.add_edge(str(i)+str(j)+'4',str(i)+str(j)+'3',direct='L',weight=1)
                
                
                
                #Deplacement
                #Nord/Haut
                if (A!=1): #Teste la présence d'obstacle
                    if(i>=3):
                        G.add_edge(str(i)+str(j)+'1',str(i-3)+str(j)+'1',direct='a3',weight=1)
                    if(i>=2):
                        G.add_edge(str(i)+str(j)+'1',str(i-2)+str(j)+'1',direct='a2',weight=1)
                    if(i>=1):
                        G.add_edge(str(i)+str(j)+'1',str(i-1)+str(j)+'1',direct='a1',weight=1)  
                #Sud/Bas
                if (A):
                    if(i<=M-3):
                        G.add_edge(str(i)+str(j)+'3',str(i+3)+str(j)+'3',direct='a3',weight=1)
                    if(i<=M-2):
                        G.add_edge(str(i)+str(j)+'3',str(i+2)+str(j)+'3',direct='a2',weight=1)
                    if(i<=M-1):
                        G.add_edge(str(i)+str(j)+'3',str(i+1)+str(j)+'3',direct='a1',weight=1)
                #Ouest/Gauche
                if (A[i][j-1]!=1):
                    if(j>=3):
                        G.add_edge(str(i)+str(j)+'4',str(i)+str(j-3)+'4',direct='a3',weight=1)
                    if(j>=2):
                        G.add_edge(str(i)+str(j)+'4',str(i)+str(j-2)+'4',direct='a2',weight=1)
                    if(j>=1):
                        G.add_edge(str(i)+str(j)+'4',str(i)+str(j-1)+'4',direct='a1',weight=1)
                #Est/Droite
                if(A[i][j+1]!=1):
                    if(j<=N-3):
                        G.add_edge(str(i)+str(j)+'2',str(i)+str(j+3)+'2',direct='a3',weight=1)
                    if(j<=N-2):
                        G.add_edge(str(i)+str(j)+'2',str(i)+str(j+2)+'2',direct='a2',weight=1)
                    if(j<=N-1):
                        G.add_edge(str(i)+str(j)+'2',str(i)+str(j+1)+'2',direct='a1',weight=1)
                    
                
    return G


def add_edge(self, u, v, key=None, attr_dict=None, **attr):
        """Add an edge between u and v.

        The nodes u and v will be automatically added if they are
        not already in the graph.

        Edge attributes can be specified with keywords or by providing
        a dictionary with key/value pairs.  See examples below.

        Parameters
        ----------
        u,v : nodes
            Nodes can be, for example, strings or numbers.
            Nodes must be hashable (and not None) Python objects.
        key : hashable identifier, optional (default=lowest unused integer)
            Used to distinguish multiedges between a pair of nodes.
        attr_dict : dictionary, optional (default= no attributes)
            Dictionary of edge attributes.  Key/value pairs will
            update existing data associated with the edge.
        attr : keyword arguments, optional
            Edge data (or labels or objects) can be assigned using
            keyword arguments.

        See Also
        --------
        add_edges_from : add a collection of edges

        Notes
        -----
        To replace/update edge data, use the optional key argument
        to identify a unique edge.  Otherwise a new edge will be created.

        NetworkX algorithms designed for weighted graphs cannot use
        multigraphs directly because it is not clear how to handle
        multiedge weights.  Convert to Graph using edge attribute
        'weight' to enable weighted graph algorithms.

        Examples
        --------
        The following all add the edge e=(1,2) to graph G:

        >>> G = nx.MultiDiGraph()
        >>> e = (1,2)
        >>> G.add_edge(1, 2)           # explicit two-node form
        >>> G.add_edge(*e)             # single edge as tuple of two nodes
        >>> G.add_edges_from( [(1,2)] ) # add edges from iterable container

        Associate data to edges using keywords:

        >>> G.add_edge(1, 2, weight=3)
        >>> G.add_edge(1, 2, key=0, weight=4)   # update data for key=0
        >>> G.add_edge(1, 3, weight=7, capacity=15, length=342.7)
        """
        # set up attribute dict
        if attr_dict is None:
            attr_dict = attr
        else:
            try:
                attr_dict.update(attr)
            except AttributeError:
                raise NetworkXError(
                    "The attr_dict argument must be a dictionary.")
        # add nodes
        if u not in self.succ:
            self.succ[u] = self.adjlist_dict_factory()
            self.pred[u] = self.adjlist_dict_factory()
            self.node[u] = {}
        if v not in self.succ:
            self.succ[v] = self.adjlist_dict_factory()
            self.pred[v] = self.adjlist_dict_factory()
            self.node[v] = {}
        if v in self.succ[u]:
            keydict = self.adj[u][v]
            if key is None:
                # find a unique integer key
                # other methods might be better here?
                key = len(keydict)
                while key in keydict:
                    key += 1
            datadict = keydict.get(key, self.edge_key_dict_factory())
            datadict.update(attr_dict)
            keydict[key] = datadict
        else:
            # selfloops work this way without special treatment
            if key is None:
                key = 0
            datadict = self.edge_attr_dict_factory()
            datadict.update(attr_dict)
            keydict = self.edge_key_dict_factory()
            keydict[key] = datadict
            self.succ[u][v] = keydict
            self.pred[v][u] = keydict

################################################################################################################
#                                   DJIKSTRA
################################################################################################################

################################################################################################################
#                                   INTERFACE
################################################################################################################


