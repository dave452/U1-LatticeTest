# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 16:14:17 2021

@author: David
"""

import numpy as np
import U1LatticeFunctions as U1
import U1LatticeTestFunctions as U1Test
#Defines a Lattice sizes  
#N = [Lattice Size Time, L.S x, L.S y, L.S z]

lattice_size = [4,4,4,4]
beta = 1
suggested_change = np.pi / 8 # standard deviation of the change
N_t = 5000 # thermalisation steps
N_c = 4 # number of steps between observations (assumed correlated)
N_o = 250 # number of oberservations 
seed = 54565
U1.main(lattice_size, beta, suggested_change, N_t, N_c, N_o, './output/output_file5.txt',seed)
#test_plaquette(lattice_size, beta)
#U1Test.test_action(lattice_size, beta)