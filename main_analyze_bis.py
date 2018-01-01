# coding: utf-8
from simulator import *
from analyzer import *
from file_manager import *
import matplotlib.pyplot as plt

proba = []
for nb_neighbors in range(2, 50):
    f = File_manager(file_name = 'voisins/number_'+str(nb_neighbors)+'.txt')

    analyze = Analyzer(f, delta = 2, nb_filtre = 1, show=True, nb_neighbors = nb_neighbors)

    proba.append(analyze.moyenne_vidal())

plt.ylim([0,1])
plt.plot(proba, 'blue')

proba_filtred = analyze.moyenne_glissante(proba)
#plt.plot(proba_filtred, 'red', label = 'Courbe lissée')
plt.legend()
plt.title('Percolation en fonction du nombre de voisins')
plt.xlabel('Nombre de voisins')
plt.ylabel('Probabilité de percolation')
plt.savefig('graphes/perco_voisins.png')
#plt.show()
