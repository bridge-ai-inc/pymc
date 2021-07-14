"""
Code to create tissue volume
"""

import numpy as np
import matplotlib.pyplot as plt
#import pandas as pd
#import cv2



time_min     = 60        # time duratn of simulation <-run time-
binsize      = 0.0005    # size of each bin, eg. [cm] or [mm]

# function for creating tissue volume
def makeTissueVox(tissuename,nm,SZ=0.1,MZ=0.15,DZ=0.75,nbins=200):
    '''
    Definition of the input parameters are:
    SZ = superficial zone
    MZ = middle zone
    DZ = deep zone
    nm = desired wavelength of simulation
    nbins = no. of bins in each dimension of cube
    tissuename = name for files: _T.bin, _H.mci
    '''
    tissue1d = []
    nSZ = int(SZ*nbins)
    nMZ = int(MZ*nbins)
    nDZ = int(DZ*nbins)
    
    for i in range(nbins):
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

    # Save data as binary file
    tissue3d.astype('int8').tofile('./src_data/'+tissuename+'_T.bin')
    
    return tissue3d


if __name__ == '__main__':

    tissue3d = makeTissueVox('testTissue', 530)
    print(tissue3d.shape)
    tissue2d = tissue3d[:,:,100]
    print(tissue2d.shape)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(tissue2d, cmap='jet')#
    plt.show()


