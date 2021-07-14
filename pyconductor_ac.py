
'''
About  : Python script to conduct MC modelling of light interaction in cartilage
Author : Isaac Afara
Date   : 19.06.2019
Licence: MIT [Check mcxyz]
version: 0.2 [26.02.2020]
         updated to use cartilage optical properties
========================================================
TODO for version O.3
- setup Puhti to run and visualize all wavelengths
========================================================
TODO for version O.4
- port all matlab code to python
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

# Number of CPU available on machine >>> os.cpu_count()

from tqdm import tqdm
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from multiprocessing import Process, current_process
import os
import matlab.engine as mateng
print(__doc__)

# external scripts and parallel processing
#import argparse

# data manipulation, visualization & miscellaneous

# Change to dir containing input and other files: matlab & c codes
path_data = './src_data'
os.chdir(path_data)
MAX_NUM_CORES_TO_USE = int(os.cpu_count()/2)


''' Function to create tissue structure: wave = pandas dataframe of wavelengths
- start matlab engine
- loop with tissuestruct and create tissue structure at different wavelengths for MC sim
- if set by user, visualize tissue
'''


def create_tissue(wave, visualize='on'):
    eng = mateng.start_matlab()
    for i in tqdm(range(len(wave))):
        tissueName = 'cartilage_'+str(wave['nm'][i])
        tissue = tissueName
        tissue = eng.makeCartilageList(float(wave['nm'][i]), nargout=0)
        # st = eng.cartilage3Dstruct(float(wave['nm'][i]), tissueName, nargout=1)
        st = eng.cartilage3Dstruct_dev(float(wave['nm'][i]), tissueName, nargout=1)
        if st == 1:
            print('Tissue structure successfully created!')
        else:
            print("Error, check 'cartilage3Dstruct' script in MATLAB!")
    eng.quit()
    # return tissueName

    if visualize == 'on':
        data = np.fromfile(tissueName+'_T.bin', dtype=np.ubyte)
        nbins = int(np.cbrt(data.shape[0]))
        tissue_vox = data.reshape(nbins, nbins, nbins)
        tissue2d = tissue_vox[:, :, 1]

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.imshow(tissue2d, cmap='jet')
        plt.show()
    print('All tissue files created (and maybe visualized)')


def make_tissue_list(wave):
    tissue_list = []
    for i in range(len(wave)):
        tissueName = 'cartilage_'+str(wave['nm'][i])
        tissue_list.append(tissueName)
        print(tissue_list)
    return tissue_list


''' Function to run Monte Carlo simulation
- loop through tissue structure at different wavelengths
- implement multiprocessing parallelization to increase speed of computation
'''

# OLD mc_simulation
# def mc_simulation(wave):
#    for i in tqdm(range(len(wave))):
#        tissueName = 'tissue_'+str(wave['nm'][i])
#        cmd = './mcxyz ' + tissueName
#        d = os.system(cmd)
#        print('Error Code:', d, '...No errors!')
#        if d != 0:
#            print('Error Code:', d, '...exiting computation')
#            break

# NEW mc_simulation


def mc_simulation(name):
    d = os.system('./mcxyz ' + name)
    print('simulating tissue ' + name)
    print('Error Code:', d, '...No errors!')

    print(f"Process ID: {os.getpid()}")
    # can also use the "current_process" function
    print(f"Process Name: {current_process().name}")


''' Function to visualize output of Monte Carlo simulation
- optional argument to create video
'''


def visualize_fluence(wave, video='off'):
    eng = mateng.start_matlab()
    for i in tqdm(range(len(wave))):
        tissueName = 'cartilage_'+str(wave['nm'][i])
        # print(tissueName)
        st = eng.lookfluence(float(wave['nm'][i]), tissueName, nargout=1)
        if st == 1:
            print('Tissue structure successfully visualized!')
        else:
            print('Error, check input args or see lookfluence.m!')
    eng.quit()

    if video == 'on':
        img = []
        for i in range(len(wave)):
            tissueName = 'cartilage_'+str(wave['nm'][i])+'_Fzx.jpg'  # OR '_Fzy.jpg'
            print(tissueName)
            img.append(cv2.imread(tissueName))

        height, width, layers = img[1].shape
        video = cv2.VideoWriter('ac_fluence.mp4', -1, 1, (width, height))

        for j in range(len(wave)):
            video.write(img[j])

        cv2.destroyAllWindows()
        video.release()

    print('All tissue files created and visualized)')


'''================================== MAIN CODE  ================================='''


if __name__ == '__main__':

    wv = pd.read_csv('wave3.csv')  # import wavelength list

    create_tissue(wv, visualize='on')  # create tissue structure (turn on visualization)

    names = make_tissue_list(wv)  # create list of tissue names >> #mc_simulation(wv)

    processes = []  # NUM_ROUNDS = len(names)//MAX_NUM_CORES_TO_USE

    # Loop through list of names and call "mc_simulation" in each process
    for i, name in enumerate(names):
        process = Process(target=mc_simulation, args=(name,))  # create process object
        processes.append(process)
        process.start()  # spawn process by calling start() method.

    # Wait for Python process to end before starting the next process.
    for process in processes:
        process.join()

    visualize_fluence(wv, video='off')  # visualize fluence maps
