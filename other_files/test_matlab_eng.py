'''
Python script to ´conduct´ modelling of photon transportation
and interaction in connective tissues
'''

# run external scripts
import matlab.engine as mateng
import pandas as pd
from tqdm import tqdm
import os
#import argparse

# data manipulation and visualization
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#def createTissue():
#    eng = mateng.start_matlab()

#    for i in tqdm(range(len(wave))):
#        tissueName = 'test_tissue_'+str(wave['nm'][i])
#        print(tissueName)
#        st = eng.tissuestruct(float(wave['nm'][i]), tissueName, nargout=1)
#        if st == 1:
#            print('Tissue structure successfully created!')
#        else:
#            print('Possible error, check code in MATLAB!')
#    eng.quit()



''' Function to visualize tissue structure
- import one of the created tissue structure binary files 
- reshape and visualize
'''    
#def visualize_tissue(data):
#    nbins = int(np.cbrt(data.shape[0]))
#    tissue_vox = data.reshape(nbins, nbins, nbins)
#    #print('Shape after reshaping: ', tissue_vox.shape)

#    tissue2d = tissue_vox[:,:,1]
#    print(tissue2d.shape)

#    fig = plt.figure()
#    ax = fig.add_subplot(111)
#    ax.imshow(tissue2d, cmap='jet')
#    plt.show()    
    
    
'''
- import wavelength list
- start matlab engine 
- loop through tissuestruct and create tissue structure for Monte Carlo simulation
  at different wavelengths
'''
wave = pd.read_csv('wave.csv')
eng = mateng.start_matlab()

for i in tqdm(range(len(wave))):
    tissueName = 'test_tissue_'+str(wave['nm'][i])
    print(tissueName)
    st = eng.tissuestruct(float(wave['nm'][i]), tissueName, nargout=1)
    if st == 1:
        print('Tissue structure successfully created!')
    else:
        print('Possible error, check code in MATLAB!')
#eng.quit()


'''
- import one of the created tissue structure binary files 
- reshape and visualize
'''
data = np.fromfile(tissueName+'_T.bin', dtype=np.ubyte)
print(type(data), ', data shape: ', data.shape)

nbins = 200
tissue_vox = data.reshape(nbins, nbins, nbins)
print('Shape after reshaping: ', tissue_vox.shape)

tissue2d = tissue_vox[:,:,1]
print(tissue2d.shape)

# matplotlib
fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(tissue2d, cmap='jet')
plt.show()

# import of the created tissue bine files and visualize
#data = np.fromfile(tissueName+'_T.bin', dtype=np.ubyte)
#print(type(data), ', data shape: ', data.shape)
#visualize_tissue(data)


'''
- system call to mcxyz to run Monte Carlo simulation
- loop through tissue structure at different wavelengths
- most time-consuming aspect of the script
'''

for i in tqdm(range(len(wave))):
    tissueName = 'test_tissue_'+str(wave['nm'][i])
    cmd = './mcxyz ' + tissueName
    d = os.system(cmd)
    print('Error Code:', d, '...No errors!')
    if d != 0:
        print('Error Code:', d, '...exiting computation')
        break        
        
'''
- Visualize and save output of Monte Carlo simulation
- again, we need the matlab engine
'''
#eng = mateng.start_matlab()

for i in tqdm(range(len(wave))):
    tissueName = 'test_tissue_'+str(wave['nm'][i])
    print(tissueName)
    st = eng.look(float(wave['nm'][i]), tissueName, nargout=1)
    if st == 1:
        print('Tissue structure successfully visualized!')
    else:
        print('Possible error, check look.m code in MATLAB!')
eng.quit()