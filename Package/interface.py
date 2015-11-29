# Package: Projet MOGPL: la balade du robot

# Sportich Benjamin, de Bezenac Emmanuel


from matplotlib.table import Table
import matplotlib.lines as lines
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arrow,FancyArrowPatch
from ipywidgets import Button,IntSlider,Latex,HBox
from IPython.display import display
from inst_gen import *


###################################################################################
########################### AFFICHAGE D'UNE INSTANCE ##############################
################################################################################### 

def show_interface(result,A,startPos,endPos,figsize=(8,8)):
    colors=['white','grey']
    fig=plt.figure(figsize=figsize)
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








###################################################################################
################################### IHM  ##########################################
################################################################################### 



class Interface():
    def __init__(self,figsize=(6,6)):
        self.figsize=figsize
        self.size_slider=IntSlider(description='Grid Size',min=4,max=50)
        display(self.size_slider)

        self.nb_ob_slider=IntSlider(description='Obstacles',min=0,max=7)
        display(self.nb_ob_slider)

        self.gen_inst_button=Button(description='Generate Instance',margin=10)
        self.gen_pos_button=Button(description='Generate Start/End Positions',margin=10)
        self.gen_path_button=Button(description='Generate Path',margin=10)
        self.inst_but_container=HBox(children=[self.gen_inst_button,self.gen_pos_button,self.gen_path_button])
        self.inst_but_container.width = '100%'
        display(self.inst_but_container)


        self.show_path_button=Latex(value='Path: Value:  Actions:',margin=10)
        display(self.show_path_button)

        self.size_slider.on_trait_change(self._on_size_slider_change,'value')
        self.gen_inst_button.on_click(self._on_gen_inst_button_click)
        self.gen_pos_button.on_click(self._on_pos_button_click)
        self.gen_path_button.on_click(self._on_gen_path_button_click)
        
        self.gen_path_button.disabled=True
        self.gen_pos_button.disabled=True
            
        plt.close()
        #plt.axis('off')
        self.fig=plt.figure(figsize=self.figsize)
        self.ax=self.fig.add_subplot(111)
        

    def _on_size_slider_change(self,name,value):
        self.nb_ob_slider.max=int(value)**2/2-4 #Constrain on number of obstacles
    
    def _on_gen_inst_button_click(self,b):
        self.gen_path_button.disabled=True
        self.gen_pos_button.disabled=False
            
        self.show_path_button.value='Path: Value:  Actions:'

        for line in self.ax.lines:
            line.set_visible(False)
            del(line)
        #Instance Generation
        self.M=self.size_slider.value
        self.nb_ob=self.nb_ob_slider.value
        
        self.A=gen_rand_instance(self.M,self.M,self.nb_ob)
        
        self.G=gen_graph(self.A)
               
        
        if hasattr(self, 'ax'):
        #    print self.ax
            self.ax.cla()
        if hasattr(self, 'start_circle'):
            del(self.start_circle)
            del(self.end_circle)
            del(self.arrow)


        
        colors=['white','grey']
        self.ax.set_ylim([0,self.A.shape[0]])
        self.ax.set_xlim([0,self.A.shape[1]])
        self.ax.set_axis_off()
        self.tb = Table(self.ax, bbox=[0,0,1,1])
        nrows, ncols = self.A.shape
        width, height = 1.0 / ncols, 1.0 / nrows
        # Add cells
        for (i,j),val in np.ndenumerate(self.A):
            color=colors[val]
            self.tb.add_cell(i, j, width, height,loc='center', facecolor=color)
        # Row Labels...
        for i in range(self.A.shape[0]):
            self.tb.add_cell(i, -1, width, height, text=i, loc='right', 
                        edgecolor='none', facecolor='none')
        # Column Labels
        for j in range(self.A.shape[1]):
            self.tb.add_cell(-1, j, width, height/2, text=j, loc='center', 
                               edgecolor='none', facecolor='none')
        self.ax.add_table(self.tb)
        self.ax.invert_yaxis()
        #self.leg=self.ax.legend(bbox_to_anchor=(1.3, 1.05),fancybox=True)
        #self.leg.get_frame().set_alpha(0.5)
        #self.ax.legend()
        plt.show()

        
    def _on_pos_button_click(self,b):
        for line in self.ax.lines:
            line.set_visible(False)
            del(line)
        self.gen_path_button.disabled=False

        self.start,self.end=gen_rand_positions(self.G)
        #Ajout Depart
        start_inst=self.start[:2][::-1]
        #Ajout Direction de Depart
        start_dir=self.start[2]
        start_posA=start_inst
        end_inst=self.end[:2][::-1]
        if(start_dir==1):        
            start_posB=(start_posA[0],start_posA[1]-1)
        if(start_dir==2):
            start_posB=(start_posA[0]+1,start_posA[1])
        if(start_dir==3):
            start_posB=(start_posA[0],start_posA[1]+1)
        if(start_dir==4):
            start_posB=(start_posA[0]-1,start_posA[1]) 
            
        if hasattr(self, 'start_circle'): #deja trace
            self.start_circle.set_visible(True)
            self.end_circle.set_visible(True)
            self.arrow.set_visible(True)
            self.start_circle.center=start_inst
            self.arrow.set_positions(start_posA,start_posB)
            self.end_circle.center=end_inst
            self.show_path_button.value='Path: Value:  Actions:'
            
        else: #jamais trace encore
            #Position de Depart
            self.start_circle=Circle(start_inst,radius=0.5,alpha=0.8, color='g',zorder=2,label='Depart',clip_on=False)
            self.ax.add_patch(self.start_circle)
            #Direction de Depart
            self.arrow=FancyArrowPatch(start_posA,start_posB,arrowstyle='->',color='m',mutation_scale=15.0,lw=2,zorder=3,clip_on=False)
            self.ax.add_patch(self.arrow)
            #Ajout Arrivee

            self.end_circle=Circle(end_inst,radius=0.5,alpha=0.8, color='r',zorder=2,label='Arrivee',clip_on=False)
            self.ax.add_patch(self.end_circle)
            self.leg=self.ax.legend(bbox_to_anchor=(1.1, 1.05),fancybox=True)
            self.leg.get_frame().set_alpha(0.5)
        
        plt.show()
        

        
    def _on_gen_path_button_click(self,b):
        self.gen_path_button.disabled=True

        self.result=gen_shortest_path(self.start,self.end,self.G)
        self.show_path_button.value='Path: Value:  '+str(self.result[0])+' Actions: '+' '.join(e for e in self.result[1])    
    
        #Ajout Chemin
        for i,j in self.result[2]:
            self.ax.add_line(lines.Line2D((i[1],j[1]),(i[0],j[0]),linewidth=3,zorder=1,clip_on=False))
        plt.draw()
        
        
        
        
        
        
        
        
        
        
###################################################################################
############################# AFFICHAGE DU GRAPHE #################################
################################################################################### 
        
        
        
def fixed_pos(G): #Assigne des positions aux noeuds du graphe
    fixed_pos={}
    for n in G.nodes():
        if(n[2]==1):
            fixed_pos[n]=(int(n[1])*4+1,int(n[0])*4)
        if(n[2]==2):
            fixed_pos[n]=(int(n[1])*4+2,int(n[0])*4+1)
        if(n[2]==3):
            fixed_pos[n]=(int(n[1])*4+1,int(n[0])*4+2)
        if(n[2]==4):
            fixed_pos[n]=(int(n[1])*4,int(n[0])*4+1)        
    return fixed_pos


def draw_graph(G,pos,ax,sg=None): #Genere l'affichage du graphe
    G_new=G.copy()
    for n in G_new:
        c=Circle(pos[n],radius=0.15,alpha=0.5)
        ax.add_patch(c)
        G_new.node[n]['patch']=c
        x,y=pos[n]
    seen={}
    for (u,v,d) in G_new.edges(data=True):
        n1=G_new.node[u]['patch']
        n2=G_new.node[v]['patch']
        rad=0.2
        if (u,v) in seen:
            rad=seen.get((u,v))
            rad=(rad+np.sign(rad)*0.1)*-1
        alpha=0.5
        color='k'
        e = FancyArrowPatch(n1.center,n2.center,patchA=n1,patchB=n2,
                            arrowstyle='-|>',
                            connectionstyle='arc3,rad=%s'%rad,
                            mutation_scale=10.0,
                            lw=2,
                            alpha=alpha,
                            color=color)
        seen[(u,v)]=rad
        ax.add_patch(e)
    return e

def show_graph(G,figsize=(7,7)): # affiche le graphe
    fig=plt.figure(figsize=figsize)
    ax=fig.add_subplot(111)
    ax.invert_yaxis()
    draw_graph(G,fixed_pos(G),ax)
    ax.autoscale()
    plt.axis('equal')
    plt.axis('off')
    plt.savefig('graph2.png')
    plt.show()
    #nx.draw_networkx(G,fixed_pos,ax=axe,arrows=True,node_size=400,font_size=10)
    #nx.draw(G,fixed_pos(G),ax=axe)
