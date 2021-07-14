'''
About  : Python class to create tissue objects with know layer thickness
         and visualize Monte Carlo simulation outputs
Author : Isaac Afara
Date   : 14.07.2021
Licence: MIT [This code calls mcxyz program written by Steve Jacques]
version: 0.1 [26.02.2020]
         updated to use cartilage optical properties
========================================================
TODO for version O.3
- setup xxxx
========================================================
TODO for version O.4
- xxxx
- better wrapper to call mcxyz.c
========================================================
TODO for version 1.O
- encapsulate in GUI
- option to run and visualize all or single wavelengths
========================================================
========================README==========================
This code requires the following files (located in ./src_data):
- makeCartilageList.m
- mcxyz
'''

import numpy as np
import random
import string
from datetime import date
import matplotlib.pyplot as plt
import os
from multiprocessing import Process, current_process


class CreateTissue:

    tissueType = 'Cartilage'
    tissueLayers = 3
    tissueThicness = 0.0
    # tissueWidth = 0.0
    binsize = 0.005

    def __init__(self, SZ, MZ, DZ, nbins):
        self.SZ = SZ        # SZ = % of superficial zone
        self.MZ = MZ        # MZ = % of middle zone
        self.DZ = DZ        # DZ = % of deep zone
        self.nbins = nbins  # nbins = number of bins

        self.id = 'tissue'+'_'+''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(6))

        tissue1d = []
        nSZ = int(self.SZ * self.nbins)
        nMZ = int(self.MZ * self.nbins)
        nDZ = int(self.DZ * self.nbins)

        for i in range(self.nbins):
            if i <= nSZ:
                tissue1d.append(1)
            elif i > nSZ and i <= nSZ+nMZ:
                tissue1d.append(2)
            else:
                tissue1d.append(3)

        tissue1d = np.asarray(tissue1d)
        tissue2d = tissue1d
        for i in range(nbins-1):
            tissue2d = np.vstack((tissue2d, tissue1d))

        tissue3d = np.transpose(tissue2d)
        for i in range(nbins-1):
            tissue3d = np.dstack((tissue3d, np.transpose(tissue2d)))

        self.T = tissue3d
        self.T.astype('int8').tofile(self.id + '_T.bin')
        print('{} has been successfully saved as {}_T.bin'.format(self.id, self.id))


    def set_thickness(self, thickness):
        self.thickness = thickness
        self.binsize = self.thickness / self.nbins


    def view(self):
        tissue2d = self.T[:, :, int(self.nbins/2)]
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(tissue2d, cmap='jet', interpolation='none', 
                  extent=[0, self.binsize*self.nbins, self.binsize*self.nbins, 0])
        ax.set_aspect('auto')
        plt.show()

    
    def run_monte_carlo(self, time):
        self.time = time
        # create .mci file here
        d = os.system('./mcxyz ' + self.id)
        print('simulating tissue ' + self.id)
        print('Error Code:', d, '...No errors!')

        print(f"Process ID: {os.getpid()}") # can also use the "current_process" function
        print(f"Process Name: {current_process().self.id}")


    def visualize_fluence(self):
        self.F = np.fromfile('{}_F.bin'.format(self.id), dtype=np.float32)
        outTissue3d = self.F.reshape(self.nbins, self.nbins, self.nbins)
        outTissue2d = outTissue3d[:, :, int(self.nbins/2)]

        fig = plt.figure()
        ax = fig.add_subplot(111)
        im1 = ax.imshow(outTissue2d,vmin=0,vmax=10,cmap='gnuplot2') # cmap='jet'
        cbar = plt.colorbar(im1)
        cbar.set_label('Light intensity')
        plt.show() 



    '''Special (Magic/Dunder) Methods'''

    def __repr__(self):
        return "CreateTissue('{}','{}','{}','{}')".format(self.SZ, self.MZ, self.DZ, self.nbins)

    def __str__(self):
        return "{} has {} layers with {} bins.".format(self.id, self.tissueLayers, self.nbins)




