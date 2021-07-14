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
- cartilage3Dstruct.m
- mcxyz
'''

import numpy as np

class CreateTissue:

    def __init__(self, SZ, MZ, DZ, nbins):
        self.SZ = SZ        # SZ = % of superficial zone
        self.MZ = MZ        # MZ = % of middle zone
        self.DZ = DZ        # DZ = % of deep zone
        self.nbins = nbins  # nbins = number of bins

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

        return tissue3d
