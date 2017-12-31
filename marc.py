# coding: utf-8
import os
import networkx as nx
import numpy
from random import *
from progress import *

window_progress = ProgressBar()

n = 5
for i in range(n):
    print('###########'+str(i)+'/'+str(n)+'###########')
    nbre_noeud =[500]
    
    #K=nx.random_regular_graph(15,nbre_noeud[0])
    K=nx.watts_strogatz_graph(nbre_noeud[0], 15, 0)
    # K=nx.random_regular_graph(2,nbre_noeud[0])
    pos=nx.spring_layout(K,k=0.15,scale=2)
    #Loop pour les probas de 100 à 50 (1-m):
    for m in range(1,400):
        print(m)
        #Saute une ligne dans le fichier de save des percos:
        if m == 1:
            ofi = open('data.txt', 'a+')
            ofi.write('\n')
            ofi.close()
            
    #### Variables Globales
    
            
        
        liste_contamines=[]
        liste_gueries=[]
        liste_morts=[]
        color_liste =['r']+['b' for i in range(1,len(K.nodes()))];
        
        
        # f = Figure(figsize=(10,9), dpi=100)
        # a = f.add_subplot(111)
        #maze=nx.random_regular_graph(5,50);
        
        # nx.draw(K,pos,ax=a,fixed = pos.keys(),node_size =200, width=0.5)
        # nx.draw_shell(K)
        
        
        def Show():
            # a.clear()
            # nx.draw(K,pos,ax=a,fixed = pos.keys(),node_size =200, width=0.5,node_color=color_liste)
            #nx.set_node_attributes(K,'color',{k:color_liste[k] for k in range(len(color_liste))})
            # canvas.show()
        
            if liste_contamines==[] and (len(liste_gueries)!=0 or len(liste_morts)!=0):
                
                # ofi = open('C:\\Users\\grauz\\Documents\\Python code\\Outputs\\Perco.txt', 'r')
                # chaine=ofi.read()
                # liste=chaine.split(';')
                # #print(liste)
                # liste.append((m,nbre_noeud[0]-(len(liste_morts)+len(liste_gueries))))
                # chaine2=';'.join(str(v) for v in liste)
                # ofi = open('C:\\Users\\grauz\\Documents\\Python code\\Outputs\\Perco.txt', 'w')
                # ofi.write(chaine2)
                #print(chaine2)
                
                # Save les percos dans le fichier
                ofi = open('data.txt', 'a+')
                ofi.write(';'+str((m,nbre_noeud[0]-(len(liste_morts)+len(liste_gueries)))))
                ofi.close()
                        
        def Update():
            for k in range(len(liste_contamines)):
                for l in range(len(list(K.neighbors(liste_contamines[k])))):
                    i =list(K.neighbors(liste_contamines[k]))[l]
                    if i not in liste_morts and i not in liste_gueries and i not in liste_contamines:
                        prob = randint(1,1000)
                        if prob>1000-m:
                            liste_contamines.append(list(K.neighbors(liste_contamines[k]))[l]);
                prob2 = randint(1,1000);
                if prob2>880 and liste_contamines[k] not in liste_morts:
                    liste_morts.append(liste_contamines[k])
                elif prob2<=880 and liste_contamines[k] not in liste_gueries:
                    liste_gueries.append(liste_contamines[k])
                
            
            #print('liste_contamines : ',liste_contamines,' liste_gueries :',liste_gueries,' liste_morts : ', liste_morts,' colors : ',color_liste)
            
            #Vire de la liste des contaminés les morts et les guéris
            for i in range(len(liste_gueries+liste_morts)):
                if (liste_gueries+liste_morts)[i] in  liste_contamines:
                    liste_contamines.remove((liste_gueries+liste_morts)[i]);
        
        
        def Scan(): #Scan au début les contaminés et génère une liste des contaminés
            for i in range(len(K.nodes())):
                if color_liste[i] =='r':
                    liste_contamines.append(i)
            Show();
        
        def ChangerCouleur(): #Update la liste des couleurs après contamination/guérison/mort
            del color_liste[:]
            for i in range(len(K.nodes())):
                if i in liste_contamines:
                    color_liste.append('r')
                elif i in liste_gueries:
                    color_liste.append('g')
                elif i in liste_morts:
                    color_liste.append('grey')
                else:
                    color_liste.append('b')
            Show();
        
        def Start():
            Update();
            ChangerCouleur();
            
        def Loop():
            if liste_contamines==[] and (len(liste_gueries)==0 and len(liste_morts)==0):
                Scan()
            while liste_contamines!=[]:
                Update();
                ChangerCouleur();
                Loop()
    
        Loop();
    
    


#### Fonctions plot et moyenne:

def liste_tuples_perco():
    final_liste = []
    # ofi = open('C:\\Users\\grauz\\Documents\\Python code\\Outputs\\Perco.txt', 'r')
    ofi = open('data.txt', 'r')
    content = ofi.readlines()
    content = [x.strip() for x in content] 
    for x in content:
        if x!='':
            liste=x.split(';')[1:]
            elements = [eval(k) for k in liste]
            final_liste.append(elements)
    return final_liste
    
def moyenne_glissante(y, k):
    print('\n\n\n')
    print(k)
    print('\n\n\n')
    mean = y[k]
    for i in range(5):
        mean += y[max(k-i,0)]
        mean += y[min(k+i,len(y)-1)]
    return mean/11
    
def moyenne_vidal():
    print('Je suis meilleure que celle de Markoudoudou')
    
    import matplotlib.pyplot as plt
    
    liste_tuple = liste_tuples_perco()
    x = []
    y=[]
    
    for k in range(399):
        moyenne = numpy.mean([liste_tuple[i][k][1] for i in range(len(liste_tuple))])
        x.append(k)
        y.append(moyenne)
        print(x)
    
    z = [0]*len(y)
    for k in range(len(y)):
        z[k] = moyenne_glissante(y, k)    
    
    plt.plot(x,y,'blue')
    plt.xlabel('Probabilités en %')
    plt.ylabel('Nombre de survivants')
    plt.title('Nombre de survivants à la fin de l\'épidemie')
    plt.legend();
    plt.show()
    
    
    
def moyenne():
    import matplotlib.pyplot as plt
    
    liste_tuple = liste_tuples_perco()
    x = []
    y=[]
    
    for k in range(399):
        moyenne = numpy.mean([liste_tuple[i][k][1] for i in range(len(liste_tuple))])
        x.append(k)
        y.append(moyenne)
        print(x)
    plt.plot(x,y,'blue')
    plt.xlabel('Probabilités en %')
    plt.ylabel('Nombre de survivants')
    plt.title('Nombre de survivants à la fin de l\'épidemie')
    plt.legend();
    plt.show()
    return y
    
    
    
###### Fonction pour faire des logs propre (Seulement esthetique, pas utile)

def logs_propre():
    ofi2 = open('C:\\Users\\grauz\\Documents\\TIPE 2017\\Simu par Vidal\\caca2.txt', 'w+')
    
    final_liste = []
    # ofi = open('C:\\Users\\grauz\\Documents\\TIPE 2017\\Simu par Vidal\\150-500-15.txt', 'r')
    ofi = open('C:\\Users\\grauz\\Documents\\Python code\\Outputs\\Perco.txt', 'r')
    content = ofi.readlines()
    content = [x.strip() for x in content] 
    for x in content:
        if x!='':
            liste=x.split(';')[1:]
            elements = [eval(k) for k in liste]
            final_liste.append(elements)
    for i in range(len(final_liste)):
        ofi2.write(str(final_liste[i]))
        ofi2.write('\n')
    ofi2.close()
    ofi.close()
        
        
        