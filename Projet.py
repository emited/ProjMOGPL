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


################################################################################################################
#                                   DJIKSTRA
################################################################################################################

################################################################################################################
#                                   INTERFACE
################################################################################################################


