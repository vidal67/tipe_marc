# coding: utf-8
from simulator import *
from analyzer import *
from file_manager import *

nb_simulations = 15
power_ten = 2
nb_neighbors = 15

for nb_neighbors in range(2, 70):
    print('########### '+str(nb_neighbors)+' ###########')
    f = File_manager(file_name = 'voisins/number_'+str(nb_neighbors)+'.txt')
    f.new_file()

    simul = Simulator(file_object = f, nb_simulations = nb_simulations, power_ten =  power_ten, nb_neighbors = nb_neighbors)
    simul.start()
