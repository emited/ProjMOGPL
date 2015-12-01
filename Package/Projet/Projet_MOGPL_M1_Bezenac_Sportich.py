
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 17:32:50 2015
@author: 3209524
"""

########## Projet MOGPL : La balade du robot
########## 

########## DE BEZENAC Emmanuel - Groupe TD ???
########## SPORTICH Benjamin - Groupe TD ???

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
import numpy as np
import time

################################################################################################################
#                                   GENERATION ALEATOIRE D'INSTANCES
################################################################################################################

from random import choice

#M : nombre de lignes
#N : nombre de colonnes
#nb_obstacles : nombre d'obstacles
#Genere un tableau d'obstacles A à partir des paramètres en entrée
def gen_rand_instance(M,N,nb_obstacles):
    A=np.zeros((M,N),dtype=int)
    obstacles=[]
    if(nb_obstacles<=M*N-4):
        #Generation d'obstacles
        for i in range(nb_obstacles):
            obstacle=(int(np.random.rand()*M),int(np.random.rand()*N))
            while(obstacle in obstacles): #Obstacle déjà créé
                obstacle=(int(np.random.rand()*M),int(np.random.rand()*N))
            A[obstacle]=1
            obstacles.append(obstacle)        
    else:
        print 'Erreur, trop d\'obstacles.'
        
    return A

#Renvoie les positions de départ et d'arrivée à PARTIR D'UN GRAPHE DEJA CREE (!!)
def gen_rand_positions(G):
    startPos=choice(G.nodes())
    endPos=choice(G.nodes())
    return startPos,endPos

################################################################################################################
#                                   LECTURE ET ECRITURE DE FICHIER
################################################################################################################

#Lecture de fichier d'entree

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
def write_entry_file(filename,A,startPos,endPos,startDir,mod):
    #f=open(filename,'w')
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
#mod : type d'écriture w creation de nouveau fichier a ajout à la fin du fichier déja créé
#result : 
def write_result_file(filename,mod,result):
    f=open(filename,mod)
    f.write(str(result[0])+' '+' '.join(e for e in result[1])+'\n')
    f.close()

################################################################################################################
#                                   CREATION & GESTION DU GRAPHE
################################################################################################################

#Renvoie 0 si les coordonnées correspondent à un croisement accessible
#Sinon renvoie 1
# i j coordonnées 
# A tableau d'obstacles
def is_obstacle(i,j,A):
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
    if(i==M): #Dernière ligne
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

#Genere le graphe en fonction du tableau d'obstacle A
def gen_graph(A):
    M=A.shape[0]
    N=A.shape[1]
    G=nx.DiGraph()
    for i in range(M+1):
        for j in range(N+1):
            if(is_obstacle(i,j,A)==False):              
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
                    if(is_obstacle(i-k,j,A)==False):
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




################################################################################################################
#                                   PLUS COURT CHEMIN : PARCOURS EN LARGEUR
################################################################################################################

#Marque tous les noeuds du graphe avec leur distance à la position de depart
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


################################################################################################################
#                                   AFFICHAGE DE LA GRILLE
################################################################################################################

from matplotlib.table import Table
import matplotlib.lines as lines
from matplotlib.patches import Circle, Arrow,FancyArrowPatch

def show_interface(result,A,startPos,endPos):
    colors=['white','grey']
    fig=plt.figure(figsize=(10,10))
    ax=plt.subplot(111)    
    ax.set_ylim([0,A.shape[0]])
    ax.set_xlim([0,A.shape[1]])
    ax.set_axis_off()
    tb = Table(ax, bbox=[0,0,1,1])
    nrows, ncols = A.shape
    width, height = 1.0 / ncols, 1.0 / nrows
    # Add cells
    for (i,j),val in np.ndenumerate(A):
        color=colors[val]
        tb.add_cell(i, j, width, height,loc='center', facecolor=color)
    # Row Labels...
    for i in range(A.shape[0]):
        tb.add_cell(i, -1, width, height, text=i, loc='right', 
                    edgecolor='none', facecolor='none')
    # Column Labels
    for j in range(A.shape[1]):
        tb.add_cell(-1, j, width, height/2, text=j, loc='center', 
                           edgecolor='none', facecolor='none')
    ax.add_table(tb)
    
    #Ajout Chemin
    for i,j in result[2]:
        ax.add_line(lines.Line2D((i[1],j[1]),(i[0],j[0]),linewidth=3,zorder=1))
    
    #Ajout Depart
    start=startPos[:2][::-1]
    start_circle=Circle(start,radius=0.2,alpha=0.8, color='g',zorder=2,label='Position de Depart')
    ax.add_patch(start_circle)
    
    #Ajout Direction de Depart
    start_dir=startPos[2]
    start_posA=start
    if(start_dir==1):        
        start_posB=(start_posA[0],start_posA[1]-1)
    if(start_dir==2):
        start_posB=(start_posA[0]+1,start_posA[1])
    if(start_dir==3):
        start_posB=(start_posA[0],start_posA[1]+1)
    if(start_dir==4):
        start_posB=(start_posA[0]-1,start_posA[1])    
    arrow=FancyArrowPatch(start_posA,start_posB,arrowstyle='->',color='m',mutation_scale=15.0,lw=2,zorder=3,label='Sens de Depart')
    ax.add_patch(arrow)

    #Ajout Arrivee
    end=endPos[:2][::-1]
    end_circle=Circle(end,radius=0.2,alpha=0.9, color='r',zorder=2,label='Position d\'arrivee')
    ax.add_patch(end_circle)
    
    ax.invert_yaxis()
    ax.legend(bbox_to_anchor=(1.1, 1.05))
    plt.show()



################################################################################################################
#                                   PERFOMRANCE
################################################################################################################

#Genere X instances pour une grille de taille NxN avec nb_obstacles obstacles
#Ecrit ces X instances dans nom_fichier
def Gen_inst_perf(X,N,nb_obstacles,nom_fichier) : 
    mod='w'    
    for i in range(X) :
        
        #creation de l'instance
        t0=time.time()
        A=gen_rand_instance(N,N,nb_obstacles)
        t1=time.time()
        print '\nGen Instance :'+str((t1-t0))
        G=gen_graph(A)
        
        #t2=time.time()
        Pos=gen_rand_positions(G)
        #t3=time.time()
        #print '\nGen Rand Pos:'+str(t3-t2)        
        
        #ecriture dans le fichier
        write_entry_file(nom_fichier,A,Pos[0],Pos[1],Pos[0][2],mod)   ##DOUTE
        
        mod='a'
        
    return

#Fonction Gen_Inst_perf un peu inutile vu le codage de la suivante

#Gen_inst_perf(10,10,10,'entree_test.txt')
   
#Mesure :
#   - temps de generation d'instance aleatoire des caracteristiques donnees
#   - temps de generation du graphe correspondant
#   - temps de calcul du chemin
#Retourne le tableau des temps des calculs du chemin et le tableau des temps de génération des graphes
 #Genere X instances pour une grille de taille NxN avec nb_obstacles obstacles
#Ecrit ces X instances dans nom_fichier_entree
#Ecrit le resultat dans nom_fichier_sortie
def MesureTemps(X,N,nb_obstacles,nom_fichier_entree,nom_fichier_sortie,mod):
    
    tab=[]
    tab2=[]
    #mod='w'
    #Generation des instances
    #Gen_inst_perf(X,N,nb_obstacles,nom_fichier_entree)
    
    for i in range(X) :

        #m,n,A,start,end=read_entry_file(nom_fichier_entree)
        
        #creation de l'instance
        t0=time.time()
        A=gen_rand_instance(N,N,nb_obstacles)
        t1=time.time()
        print '\nGen Instance :'+str((t1-t0))
        G=gen_graph(A)
        
        #t2=time.time()
        Pos=gen_rand_positions(G)
        #t3=time.time()
        #print '\nGen Rand Pos:'+str(t3-t2)
        
        #ecriture dans le fichier
        write_entry_file(nom_fichier_entree,A,Pos[0],Pos[1],Pos[0][2],mod)   ##DOUTE        
        start=Pos[0]
        end=Pos[1]
        
    
        
        #Generation du graphe
        t0=time.time()
        G=gen_graph(A)
        t1=time.time()
        tab2.append(t1-t0)
        
        #Calcul
        result=gen_shortest_path(start,end,G)
        t2=time.time()
        
        #Affichage du chemin
        #print result[:-1]
        #show_interface(result,A,start,end)        
        
        #Ecriture du resultat        
        write_result_file(nom_fichier_sortie,mod,result[:-1]) ####DOUTE
        #mod='a'
        
        print 'Gen Graph:'+str(t1-t0)
        print 'Gen shortest path:'+str(t2-t1)
        tab.append(t2-t1)
    
    print ''
    print 'Total time: '+str(sum(tab))+'\n'
    #return tab,result
    return tab,tab2

#a,b=MesureTemps(10,50,10,'entrelol.txt','sortielol.txt')


#Mesure temps pour nuage de points
#Renvoie un tableau avec les temps si il y a un chemin, un tableau de temps pour les non chemins 
def MesureTemps2(X,N,nb_obstacles,nom_fichier_entree,nom_fichier_sortie,mod):
    
    tab=[]
    tab2=[]
    tab_n=[]
    #mod='w'
    #Generation des instances
    #Gen_inst_perf(X,N,nb_obstacles,nom_fichier_entree)
    
    for i in range(X) :

        #m,n,A,start,end=read_entry_file(nom_fichier_entree)
        
        #creation de l'instance
        t0=time.time()
        A=gen_rand_instance(N,N,nb_obstacles)
        t1=time.time()
        print '\nGen Instance :'+str((t1-t0))
        G=gen_graph(A)
        
        #t2=time.time()
        Pos=gen_rand_positions(G)
        #t3=time.time()
        #print '\nGen Rand Pos:'+str(t3-t2)
        
        #ecriture dans le fichier
        write_entry_file(nom_fichier_entree,A,Pos[0],Pos[1],Pos[0][2],mod)   ##DOUTE        
        start=Pos[0]
        end=Pos[1]
        
    
        
        #Generation du graphe
        t0=time.time()
        G=gen_graph(A)
        t1=time.time()
        tab2.append(t1-t0)
        
        #Calcul
        result=gen_shortest_path(start,end,G)
        t2=time.time()
        
        #Affichage du chemin
        #print result[:-1]
        #show_interface(result,A,start,end)        
        
        #Ecriture du resultat        
        write_result_file(nom_fichier_sortie,mod,result[:-1]) ####DOUTE
        #mod='a'
        
        print 'Gen Graph:'+str(t1-t0)
        print 'Gen shortest path:'+str(t2-t1)
        #print result
        if result[0]!=-1 : 
            tab.append(t2-t1)
        else :
            tab_n.append(t2-t1)
    
    print '\nTotal time: '+str(sum(tab))+'\n'
    #return tab,result
    return tab,tab_n,tab2


#X abscisse
def grapheGen(X,tab,tab2) : 
    fig=plt.figure(figsize=(10,10))
    ax=plt.subplot(111)
    y=tab
    #x=np.arange(len(tab))
    ten_plot=ax.plot(X,y,label='Recherche du plus court chemin en seconde(s)',linestyle='-',marker='o',color='r')
    if tab2 :
        y2=tab2
        ten_plot=ax.plot(X,y2,label='Generation du graphe en seconde(s)',linestyle='-',marker='o',color='b')
        
    
    plt.legend()
    
 
    
    plt.show()

#grapheGen(range(10),a,[])

#Même fonction que précédemment mais pour le graphe en nuage de points
#tab et tab_n : tableau des tableau des temps ave tab_n cas où pas de chemin trouvé
def grapheGen2(X,tab,tab_n,tab2) : 
    fig=plt.figure(figsize=(10,10))
    ax=plt.subplot(111)
    y=tab

    for i in range(len(X)) :
        Y=[]
        Z=[]
        for j in range(len(tab[i])) :
            Y.append(X[i])
        for j in range(len(tab_n[i])):
            Z.append(X[i])
        

        ten_plot=ax.plot(Y,tab[i],label='',linestyle='.',marker='o',color='b')
        if (tab_n[i]!=[]) :
            ten_plot=ax.plot(Z,tab_n[i],label='',linestyle='.',marker='o',color='r')
    
    
    
    if tab2 :
        y2=tab2
        ten_plot=ax.plot(X,y2,label='Generation du graphe en seconde(s)',linestyle='-',marker='o',color='b')
        
    
    plt.legend()
    plt.show()
    
    

# X : liste des tailles de la grille
# nb_inst : nombre d'instances aléatoires générées pour chaque valeur
#Pour chaque element de X : cree un fichier dentree et un fichier de sortie avec nb_inst blocs
#dg=1 : Double graphe || dg=0 Graphe de la creation du chemin seulement
def etudeTempsGrille(X,nb_inst,nom_fic_entree,nom_fic_sortie,dg) : 
    tab=[]
    tab2=[]
    e2=nom_fic_entree+"GrilleLigne_"
    s2=nom_fic_sortie+"GrilleLigne_"
    mod='w'
    for i in X :
        a,b=MesureTemps(nb_inst,i,i,e2,s2,mod)
        
        #On fait les moyennes des temps pour les instances de caractéristiques communes :            
        a_moy=sum(a)
        a_moy=a_moy/len(a)
        tab.append(a_moy)
        
        b_moy=sum(b)
        b_moy=b_moy/len(b)
        tab2.append(b_moy)
        mod='a'
    
    #Temps de la generation du graphe :
    if dg==0 :
        tab2=[]    
    grapheGen(X,tab,tab2)

#Même fonction que précédemment mais pour le graphe en nuage de points 
def etudeTempsGrille2(X,nb_inst,nom_fic_entree,nom_fic_sortie,dg) : 
    tab=[]
    tab_n=[]
    tab2=[]
    e2=nom_fic_entree+"GrilleNuage_"
    s2=nom_fic_sortie+"GrilleNuage_"
    mod='w'
    for i in X :
        a,a_n,b=MesureTemps2(nb_inst,i,i,e2,s2,mod)
        
        tab.append(a)
        tab_n.append(a_n)
        
        b_moy=sum(b)
        b_moy=b_moy/len(b)
        tab2.append(b_moy)
        mod='a'
    
    if dg==0 :
        tab2=[]
    print tab
    print tab_n
    grapheGen2(X,tab,tab_n,tab2)


#etudeTempsGrille2([10,20,30,40,50],10,'entree_','sortie_',1)

# X : liste des nombres d'obstacles
# nb_inst : nombre d'instances aléatoires générées pour chaque valeur
#Pour chaque element de X : cree un fichier dentree et un fichier de sortie avec nb_inst blocs
#dg=1 : Double graphe || dg=0 Graphe de la creation du chemin seulement
def etudeTempsObstacle(X,taille_grille,nb_inst,nom_fic_entree,nom_fic_sortie,dg) :
    tab=[]
    tab2=[]
    e2=nom_fic_entree+"ObstLigne_"
    s2=nom_fic_sortie+"ObstLigne_"
    mod='w'
    for i in X :
        a,b=MesureTemps(nb_inst,taille_grille,i,e2,s2,mod)
        
        #On fait les moyennes des temps pour les instances de caractéristiques communes :      
        a_moy=sum(a)
        a_moy=a_moy/len(a)
        tab.append(a_moy)
        
        b_moy=sum(b)
        b_moy=b_moy/len(b)
        tab2.append(b_moy)
        mod='a'
    
    #Temps de la generation du graphe :
    if dg==0 :
        tab2=[]
    grapheGen(X,tab,tab2)

#Même fonction que précédemment mais pour le graphe en nuage de points 
def etudeTempsObstacle2(X,taille_grille,nb_inst,nom_fic_entree,nom_fic_sortie,dg) :
    tab=[]
    tab_n=[]
    tab2=[]
    e2=nom_fic_entree+"ObstNuage_"
    s2=nom_fic_sortie+"ObstNuage_"
    mod='w'
    for i in X :

        a,a_n,b=MesureTemps2(nb_inst,taille_grille,i,e2,s2,mod)
                
        tab.append(a)
        tab_n.append(a_n)
        
        b_moy=sum(b)
        b_moy=b_moy/len(b)
        tab2.append(b_moy)
        mod='a'
    
    if dg==0 :
        tab2=[]
    grapheGen2(X,tab,tab_n,tab2)

#etudeTempsObstacle([10,20,30,40,50],20,10,'entree_','sortie_',1)

################################################################################################################
#                                   INTERFACE PRIMAIRE
################################################################################################################

#Genere un tableau d'obstacles A à partir des paramètres en entrée
def gen_interact_instance():
    M=int(raw_input('Taille? (X*X) '))
    A=np.zeros((M,M),dtype=int)
    nb_obstacles=int(raw_input('\nNombre d\'obstacles? '))
    obstacles=[]
    if(nb_obstacles<=M*M-4):
        #Generation d'obstacles
        for i in range(nb_obstacles):
            x_obstacle=int(raw_input('Ligne de l\obstacle \n? '))
            y_obstacle=int(raw_input('Colonne de l\obstacle \n? '))
            while((x_obstacle,y_obstacle) in obstacles): #Obstacle déjà créé
                print "Obstacle déja créé sur cette case."
                print "Creer un autre"
                x_obstacle=int(raw_input('Ligne de l\obstacle \n? '))
                y_obstacle=int(raw_input('Colonne de l\obstacle \n? '))
                    
            A[x_obstacle][y_obstacle]=1
            print "Obstacle "+str(i+1)+" sur "+str(nb_obstacles)+"placés"
            obstacles.append((x_obstacle,y_obstacle))        
    else:
        print 'Erreur, trop d\'obstacles.'
        
    return A
    

################################################################################################################
#                                   MAIN
################################################################################################################

#Test de la fonction read_entry_file
#Fichier dans le dossier
#mod='w'
#for i in range(10) :
#   m,n,A,start,end=read_entry_file('entree_test.txt')[i]  
#   G=gen_graph(A)
#   result=gen_shortest_path(start,end,G)
#   print result[:-1]
#   f=show_interface(result,A,start,end)
#   write_result_file('resultat_test.txt',mod,result[:2])
#   mod='a'

#Instance aléatoire
#A2=gen_rand_instance(50,50,350)
#G2=gen_graph(A2)
#start2,end2=gen_rand_positions(G2)
#result2=gen_shortest_path(start2,end2,G2)
#print result2[:-1]
#show_interface(result2,A2,start2,end2)
#write_result_file('rand_resultat.txt','w',result2[:-1])


#Ecrit dans les fichiers d'entree et de sortie de manière interactive
#Mesure le temps
#Affiche le resultat
def main(filename_entree,filename_sortie,mod):
    A=gen_interact_instance()
    
    t0=time.time()
    
    G=gen_graph(A)
    t1=time.time()    
        
    start,end=gen_rand_positions(G)
    t2=time.time()    
    
    result=gen_shortest_path(start,end,G)
    t3=time.time()
    
    print result[:-1]
    show_interface(result,A,start,end)
    write_entry_file(filename_entree,A,start,end,start[2],mod)
    write_result_file(filename_sortie,mod,result[:-1])
    
    print '\nGen Graph:'+str(t1-t0)
    print '\nGen Positions;'+str(t2-t1)
    print '\nGen shortest path:'+str(t3-t2)
    print 'Total Time:'+str(t3-t0)
    
    return

#On peut creer des instances aleatoires avec Gen_inst_perf(X,N,nb_obstacles,nom_fichier) 
def mainLect(filename):
    tab=read_entry_file(filename)    
    mod='w'
    for i in range() :
        m,n,A,start,end=tab[i]
        t0=time.time()        
        
        G=gen_graph(A)
        t1=time.time()    
    
        result=gen_shortest_path(start,end,G)
        t2=time.time()
       
        print result[:-1]
        f=show_interface(result,A,start,end)
        write_result_file('resultat_test.txt',mod,result[:2])
        
        print '\nGen Graph:'+str(t1-t0)
        print '\nGen shortest path:'+str(t2-t1)
        print 'Total Time:'+str(t2-t0)
        mod='a'
    print 'Overall'+str(t2)

#mainLect("nomfichier")

#ON NOTE QU'EN VERT LES INSTANCES AYANT UN CHEMIN ET EN ROUGE CELLES N'EN AYANT PAS.

etudeTempsGrille([10,20,30,40,50],10,'entree_','sortie_',1)
etudeTempsGrille2([10,20,30,40,50],10,'entree_','sortie_',1)


etudeTempsObstacle([10,20,30,40,50],20,10,'entree_','sortie_',1)
etudeTempsObstacle2([10,20,30,40,50],20,10,'entree_','sortie_',1)


