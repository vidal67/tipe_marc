# coding: utf-8

import networkx as nx
import numpy
from random import *
from file_manager import *

class Simulator:
    def __init__(self, nb_simulations, power_ten = 1, file_object = None, nb_nodes = 500, nb_neighbors = 15):
        self.nb_simulations = nb_simulations
        self.power_ten = power_ten
        self.nb_nodes = nb_nodes
        self.nb_neighbors = nb_neighbors
        if file_object == None:
            print('[SIM] No file passed by parameter')
            self.file = File_manager(prefixe = 'simulation')
            self.file.new_file()
        else:
            print('[SIM] Using file passed by parameter')
            self.file = file_object

    def start(self):
        for i in range(self.nb_simulations):
            print('[SIM] ###Simulation nº'+str(i+1)+'/'+str(self.nb_simulations)+'###')
            self.nbre_noeud = [500]

            self.K = nx.watts_strogatz_graph(self.nbre_noeud[0], self.nb_neighbors, 0)


            ### On va utiliser celui là
            self.K=nx.random_regular_graph(self.nb_neighbors,self.nbre_noeud[0])

            self.pos = nx.spring_layout(self.K, k=0.15, scale=2)

            self.p = 1

            self.bool_end = True
            self.bool_init_end = False
            self.proba_end = 1

            while self.p < 10**self.power_ten:
                if self.bool_end:
                    if self.p == 1:
                        self.file.new_line()

                    self.proba = self.p/(10**self.power_ten)
                    self.liste_contamines = []
                    self.liste_gueries = []
                    self.liste_morts = []
                    #self.color_liste = ['r'] + ['b' for i in range(1, len(self.K.nodes()))]

                    self.loop()

                    if self.bool_init_end:
                        if self.proba-self.proba_end >= 0.15:
                            self.bool_end = False
                else:
                    self.show()
                self.p += 1

    def loop(self):
        nb_gueris = len(self.liste_gueries)
        nb_morts = len(self.liste_morts)

        if self.liste_contamines == [] and ( nb_gueris == 0 and nb_morts == 0):
            self.liste_contamines.append(1)
            self.show()
        while self.liste_contamines != []:
            self.update()
            #self.change_couleur()
            self.show()
            self.loop()


    def show(self):
        if self.bool_end:
            nb_gueris = len(self.liste_gueries)
            nb_morts = len(self.liste_morts)


            if self.liste_contamines == [] and (nb_gueris != 0 or nb_morts != 0):
                nombre_to_write = self.nbre_noeud[0]-(nb_gueris+nb_morts)
                file_input = ';'+str((self.proba,nombre_to_write))

                self.file.write(file_input)

                if nombre_to_write == 0 and self.bool_init_end == False:
                    self.init_end()
        else:
            file_input = ';'+str((self.proba,0))

            self.file.write(file_input)

    def update(self):
        nb_contamines = len(self.liste_contamines)

        for k in range(nb_contamines):
            individu_contamine = self.liste_contamines[k]

            voisins = list(self.K.neighbors(individu_contamine))
            nb_voisins = len(voisins)

            for l in range(nb_voisins):
                voisin = voisins[l]

                if voisin not in self.liste_morts and voisin not in self.liste_gueries and voisin not in self.liste_contamines:
                    prob = random()
                    if prob>1-self.proba:
                        self.liste_contamines.append(voisin)

            prob2 = random()
            if prob2>0.88 and individu_contamine not in self.liste_morts:
                self.liste_morts.append(individu_contamine)

            elif prob2<=0.88 and individu_contamine not in self.liste_gueries:
                self.liste_gueries.append(individu_contamine)


        liste_finis = self.liste_gueries+self.liste_morts
        nb_finis = len(liste_finis)

        for individu in liste_finis:
            if individu in self.liste_contamines:
                self.liste_contamines.remove(individu)

    def scan(self):
        nodes = self.K.nodes()
        nb_nodes = len(nodes)

        for node in range(nb_nodes):
            if self.color_liste[node] == 'r':
                self.liste_contamines.append(node)
        self.show()



    def init_end(self):
        self.proba_end = self.proba
        self.bool_init_end = True

if __name__ == '__main__':
    a = Simulator(2, 400)
    a.start()
