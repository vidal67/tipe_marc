# coding: utf-8
from simulator import *
from analyzer import *
from file_manager import *

nb_simulations = 10
nb_points = 400
nb_neighbors = 15

for nb_neighbors in range(2, 50):
    print(nb_neighbors)
    f = File_manager(file_name = 'voisins/number_'+str(nb_neighbors)+'.txt')
    f.new_file()

    simul = Simulator(file_object = f, nb_simulations = nb_simulations, nb_points =  nb_points, nb_neighbors = nb_neighbors)
    simul.start()
