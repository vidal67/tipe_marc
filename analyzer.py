# coding: utf-8
import numpy as np
from file_manager import *
import matplotlib.pyplot as plt
import os

class Analyzer:
    def __init__(self, file_object = None, delta = 10, nb_filtre = 0, file_name = '', show = True):
        self.show = show
        self.nb_filtre = nb_filtre
        self.delta = delta
        self.coefficient_scalaire = 1/(self.delta*np.sqrt(2*np.pi))
        self.coefficient_exp = 1/(-2*(self.delta**2))
        print('[AN] Coefficient scalaire : '+str(self.coefficient_scalaire))
        print('[AN] Coefficient exponentiel : '+str(self.coefficient_exp))



        if file_object == None:

            print('[AN] No file passed, trying to find the last simulation')

            if file_name != '':
                print('[AN] Using file name passed '+str(file_name))
                self.file = File_manager(name = file_name)
                if os.path.isfile(self.file.file_name):
                    print('[AN] File succesfully opened')
                else:
                    print('[AN] File not found')
                    raise SystemExit
            else:
                self.file = File_manager(prefixe = 'simulation')

                print('[AN] Last simulation found : '+self.file.file_name)


        else:
            print('[AN] Openin passed file')
            self.file = file_object

    def liste_tuples_perco(self):
        final_liste = []

        content = self.file.readlines()
        content = [x.strip() for x in content]
        for x in content:
            if x != '':
                liste = x.split(';')[1:]
                elements = [eval(k) for k in liste]
                final_liste.append(elements)
        return final_liste

    def moyenne(self):
        for k in range(399):
            moyenne = np.mean([liste_tuple[i][k][1] for i in range(len(liste_tuple))])
            x.append(k)
            y.append(moyenne)

        plt.plot(x,y,'blue')
        plt.xlabel('Probabilités en %')
        plt.ylabel('Nombre de survivants')
        plt.title('Nombre de survivants à la fin de l\'épidemie')
        plt.legend();
        plt.show()

    def plot_gauss(self):
        x = [i-self.delta*10 for i in range(20*self.delta)]
        y = []
        for i in x:
            y.append(self.gauss(i))

        plt.plot(x, y)
        plt.show()

    def gauss(self, ecart):
        return_value = self.coefficient_scalaire*np.exp((ecart**2)*self.coefficient_exp)
        return return_value

    def moyenne_glissante(self, y):
        n = len(y)
        temp_list = []
        for k in range(n):
            temp_list.append(self.mean(y, k))
        return temp_list

    def mean(self, y, k):
        d = self.delta
        mean = y[k]
        mean_divide = 1
        n = len(y)
        for i in range(1,d+1):
            mean += y[max(0, k-i)] + y[min(n-1, k+i)]
            mean_divide+=2
        return mean/mean_divide

    def find_maximum(self, tab):
        maximum = tab[0]
        index = 0
        n = len(tab)
        for i in range(n-1):
            if maximum < tab[i]:
                index = i
                maximum = tab[i]
        return maximum, index

    def find_middle(self, tab):
        max = tab[0]
        min = tab[-1]
        middle = (max+min)/2

        n = len(tab)

        for i in range(n):
            if tab[i] < middle:
                return i
        return -1


    def moyenne_vidal(self):
        liste_tuple = self.liste_tuples_perco()
        x = []
        y=[]

        for k in range(399):
            moyenne = np.mean([liste_tuple[i][k][1] for i in range(len(liste_tuple))])
            x.append(k)
            y.append(moyenne)

        filtrages = [y]

        for i in range(self.nb_filtre):
            print('[AN] Filtrage nº'+str(i+1))
            filtrages.append(self.moyenne_glissante(filtrages[i]))
        middle = self.find_middle(filtrages[-1])
        print(middle)

        if self.show:
            for i in range(self.nb_filtre, self.nb_filtre+1):

                plt.plot(x, y, 'blue')
                plt.plot(x, filtrages[i], 'yellow')
                plt.plot( [middle, middle], [min(y), max(y)], 'red')

                plt.xlabel('Probabilités en %')
                plt.ylabel('Nombre de survivants')
                plt.title('Nombre de survivants à la fin de l\'épidemie')
                plt.legend();
                plt.show()
        return middle/10
