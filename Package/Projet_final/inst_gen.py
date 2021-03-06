# Package: Projet MOGPL: la balade du robot

# Sportich Benjamin, de Bezenac Emmanuel

import networkx as nx
import numpy as np
from random import choice
import matplotlib.pyplot as plt


###################################################################################
########################### ENTREE/SORTIE INSTANCES ###############################
################################################################################### 



def read_entry_file(filename):
    with open(filename) as f:
        k=0
        inst_size=245 #arbitrary number
        inst_list=[]
        for line in f:
            if(k==0%inst_size):
                M=int(line.split()[0]) # lecture de la premiere ligne
                N=int(line.split()[1]) # lecture de la premiere ligne
                inst_size=M+2
                k+=1
                array = [] 
            elif(k<=(M%inst_size)): # lecture du bloc                
                array.append(np.array([int(x) for x in line.split()]))
                k+=1
            
            elif(k==M%inst_size+1): #lecture du debut, de la fin, ainsi que de la direction
                iStart,jStart,iEnd,jEnd=[int(line.split()[i]) for i in range(4)]
                startDir=line.split()[4]
                if(startDir=='nord'):
                    startDir=1
                if(startDir=='est'):
                    startDir=2
                if(startDir=='sud'):
                    startDir=3
                if(startDir=='ouest'):
                    startDir=4 
                k+=1
            else:
                inst_list.append((M,N,np.array(array),(iStart,jStart,startDir),(iEnd,jEnd,1)))
                k=0
    return inst_list

#Ecriture de fichier d'entree
#def write_entry_file(filename,A,startPos,endPos,startDir):
def write_entry_file(filename,mod,A,startPos,endPos,startDir):
    f=open(filename,mod)
    f.write(str(A.shape[0])+' '+str(A.shape[1])+'\n')
    for i in A:
        f.write(' '.join(str(int(e)) for e in i))
        f.write('\n')
    if(startDir==1):
        d='nord'
    if(startDir==2):
        d='est'
    if(startDir==3):
        d='sud'
    if(startDir==4):
        d='ouest'
    f.write(str(startPos[0])+' '+str(startPos[1])+' '+str(endPos[0])+' '+str(endPos[1])+' '+d+'\n')
    f.write('0 0\n')
    f.close()

#Ecriture de fichier de resultat
#filename : nom du fichier 
#mod : type d'ecriture w creation de nouveau fichier a ajout a la fin du fichier deja cree
#result : 
def write_result_file(filename,mod,result):
    f=open(filename,mod)
    f.write(str(result[0])+' '+' '.join(e for e in result[1])+'\n')
    f.close()





###################################################################################
######################## GENERATION ALEATOIRE D'INSTANCES #########################
################################################################################### 

#M : nombre de lignes
#N : nombre de colonnes
#nb_obstacles : nombre d'obstacles
#Genere un tableau d'obstacles A a partir des parametres en entree
def gen_rand_instance(M,N,nb_obstacles):
    A=np.zeros((M,N),dtype=int)
    obstacles=[]
    if(nb_obstacles<=M*N-4):
        #Generation d'obstacles
        for i in range(nb_obstacles):
            obstacle=(int(np.random.rand()*M),int(np.random.rand()*N))
            while(obstacle in obstacles): #Obstacle deja cree
                obstacle=(int(np.random.rand()*M),int(np.random.rand()*N))
            A[obstacle]=1
            obstacles.append(obstacle)        
    else:
        print 'Erreur, trop d\'obstacles.'
        
    return A

#Renvoie les positions de depart et d'arrivee a PARTIR D'UN GRAPHE DEJA CREE (!!)
def gen_rand_positions(G):
    startPos=choice(G.nodes())
    endPos=choice(G.nodes())
    return startPos,endPos

###################################################################################
############################# CREATION DU GRAPHE ##################################
###################################################################################

# ###  Teste si le point $(i,j) \in O$

def is_obstacle(i,j,A): #Teste si le point (i,j) appartient a O (O=X\P)
    M=A.shape[0]
    N=A.shape[1]
    #Cas Limites
    if(i==0): #Premiere ligne
        if(j==0): #Premiere case
            return A[0][0]
        if(j==N): #Derniere case
            return A[0][N-1]
        if(j>0 and j<N): #Cases restantes
            return A[0][j] or A[0][j-1]       
    if(i==M): #Derniere ligne
        if(j==0): #Premiere case
            return A[M-1][0]
        if(j==N): #Derniere case
            return A[M-1][N-1]
        if(j>0 and j<N): #Cases restantes
            return A[M-1][j-1] or A[M-1][j] 
    if(j==0): #Premiere colonne 
        if(i>0 and i<M): #Cases restantes
            return A[i][0] or A[i-1][0]       
    if(j==N): #Derniere colonne 
        if(i>0 and i<M): #Cases restantes
            return A[i-1][N-1] or A[i][N-1] 
    #Cas General
    if( i>=1 and j>=1 and i<M and j<N and A[i-1][j-1]==0 and A[i][j-1]==0 and A[i-1][j]==0 ):
        return A[i][j]
    return 1


# ### Genere le graphe en fonction du tableau d'obstacles


def gen_graph(A):
    M=A.shape[0]
    N=A.shape[1]
    G=nx.DiGraph()
    for i in range(M+1):
        for j in range(N+1):
            if(is_obstacle(i,j,A)==False): # le point (i,j) n'appartient pas a O, il appartient donc a P.            
                #Creation des noeuds - un par direction = 4 par position                
                G.add_node((i,j,1),direct='nord')
                G.add_node((i,j,2),direct='est')
                G.add_node((i,j,3),direct='sud')
                G.add_node((i,j,4),direct='ouest')

                #Creation des arcs
                #Changement des directions               
                G.add_edge((i,j,1),(i,j,2),action='D')
                G.add_edge((i,j,1),(i,j,4),action='G')
                G.add_edge((i,j,2),(i,j,3),action='D')
                G.add_edge((i,j,3),(i,j,4),action='D')

                G.add_edge((i,j,2),(i,j,1),action='G')
                G.add_edge((i,j,4),(i,j,1),action='D')
                G.add_edge((i,j,3),(i,j,2),action='G')
                G.add_edge((i,j,4),(i,j,3),action='G')

                #Deplacement
                #Nord/Haut
                for k in [1,2,3]:
                    if(is_obstacle(i-k,j,A)==False): #(i,j) et (i-k,j) appartiennent a P, on peut donc creer l'arc
                        G.add_edge((i,j,1),(i-k,j,1),action=('a'+str(k)))
                    else:
                        break #Si il y a un obstacle en i-k on ne creer pas d'arc en i-k-1
                #Est/Droite
                for k in [1,2,3]:
                    if(is_obstacle(i,j+k,A)==False):
                        G.add_edge((i,j,2),(i,j+k,2),action=('a'+str(k)))
                    else:
                        break #Si il y a un obstacle en j+k on ne creer pas d'arc en j+k+1
                
                #Sud/Bas
                for k in [1,2,3]:
                    if(is_obstacle(i+k,j,A)==False):
                        G.add_edge((i,j,3),(i+k,j,3),action=('a'+str(k)))
                    else:
                        break #Si il y a un obstacle en i+k on ne creer pas d'arc en i-k+1
                
                #Ouest/Gauche
                for k in [1,2,3]:
                    if(is_obstacle(i,j-k,A)==False):
                        G.add_edge((i,j,4),(i,j-k,4),action=('a'+str(k)))
                    else:
                        break #Si il y a un obstacle en j-k on ne creer pas d'arc en j-k-1
                        
    return G

###################################################################################
############################## PARCOURS DU GRAPHE #################################
################################################################################### 


def BFS(start,end,G):
    dist={}
    for i in G.nodes():
        dist[i]=[np.inf,None] #dist: [distance a start, predecesseur]
    dist[start][0]=0 
    q=[start] #on mets le premier element dans la queue q
    while(q):# tant que la queue n'est pas vide
        
        u=q.pop(0) #on retire le prochain element de la queue q pour l'assigner a u
        
        for v in G.neighbors(u): #on explore tout les voisins de u
            
            if(np.isinf(dist[v][0])): #si le voisin v de u n'a pas encore ete explore
                dist[v][0]=dist[u][0]+1
                dist[v][1]=u # le predecesseur de v est u
                q.append(v) #on rajoute v a la queue
                if(v[:2]==end[:2]): #on s'arrete lorsqu'on voit la fin
                    return dist
    return dist


def gen_shortest_path(start,end,G):
    #Backtracking: on retrouve le chemin minimal a partir d'un des 4 sommets de la fin
    dist=BFS(start,end,G) #resultat du BFS
    path=[] #stocke l'action associe aux arcs parcourus
    path_edges=[] #stocke le nom des arcs parcourus
    i=end[0]
    j=end[1]
    dist_end=[dist[(i,j,1)][0],dist[(i,j,2)][0],dist[(i,j,3)][0],dist[(i,j,4)][0]]
    k=np.argmin(dist_end)+1 #renvoie la direction de la derniere etape
    if(dist_end[k-1]==np.inf): #si on n'a pas parcouru la position end
        return -1,[],[]
    prec=(i,j,k)
    while(prec!=start):
        temp=prec
        prec=dist[prec][1]
        path_edges.append([prec,temp])
        path.append(G[prec][temp]['action'])
    return len(path),path[::-1],path_edges[::-1] 
    #on renvoie le cout du chemin, ainsi les listes dans l'ordre inverse

