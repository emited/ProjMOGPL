# Package: Projet MOGPL: la balade du robot

# Sportich Benjamin, de Bezenac Emmanuel

################################################################################################################
#                                   PERFORMANCE
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

#ON NOTE QU'EN VERT LES INSTANCES AYANT UN CHEMIN ET EN ROUGE CELLES N'EN AYANT PAS.

#etudeTempsGrille([10,20,30,40,50],10,'entree_','sortie_',1)
#etudeTempsGrille2([10,20,30,40,50],10,'entree_','sortie_',1)


#etudeTempsObstacle([10,20,30,40,50],20,10,'entree_','sortie_',1)
#etudeTempsObstacle2([10,20,30,40,50],20,10,'entree_','sortie_',1)

