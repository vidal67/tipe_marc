# coding: utf-8
from simulator import *
from analyzer import *
from file_manager import *
import matplotlib.pyplot as plt

proba = []
for nb_neighbors in range(2, 14):
    f = File_manager(file_name = 'voisins/number_'+str(nb_neighbors)+'.txt')

    analyze = Analyzer(f, delta = 10, nb_filtre = 30, show=False)
    proba.append(analyze.moyenne_vidal())
plt.plot(proba, 'blue')

proba_filtred = analyze.moyenne_glissante(proba)
plt.show()
