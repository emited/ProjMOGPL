from inst_gen import *
from interface import *
from stats import *


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
    
    
'''################################################################################################################
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
        
    return A'''
