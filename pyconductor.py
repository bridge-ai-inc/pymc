
'''
About: Python script to conduct modelling of light interaction in connective tissues
Author: Isaac Afara
Licence: MIT >> Check mcxyz
version: 0.1

========================================================
TODO for version O.2
- update and use cartilage optical properties
- setup Puhti to run and visualize all wavelengths
========================================================
TODO for version O.3
- port all matlab code to python
- better wrapper to call mcxyz.c
========================================================
TODO for version 1.O
- encapsulate in GUI
- option to run and visualize all or single wavelengths
========================================================
'''

# Number of CPU available on machine >>> os.cpu_count()

print(__doc__)

# external scripts and parallel processing
import matlab.engine as mateng
import os
from multiprocessing import Process, current_process
#import argparse

# data manipulation, visualization & miscellaneous
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
from tqdm import tqdm

# Change to dir that contains matlab code, c code and data 
path_data = './src_data'
os.chdir(path_data)
MAX_NUM_CORES_TO_USE = int(os.cpu_count()/2)


''' Function to create tissue structure: wave = pandas dataframe of wavelengths
- start matlab engine 
- loop with tissuestruct and create tissue structure at different wavelengths for MC sim
- if set by user, visualize tissue
'''
def create_tissue(wave, visualize = 'on'):
    eng = mateng.start_matlab()
    for i in tqdm(range(len(wave))):
        tissueName = 'tissue_'+str(wave['nm'][i])
        #print(tissueName)
        st = eng.tissuestruct(float(wave['nm'][i]), tissueName, nargout=1)
        if st == 1:
            print('Tissue structure successfully created!')
        else:
            print("Error, check 'tissuestruct' script in MATLAB!")
    eng.quit()
    #return tissueName
    
    if visualize == 'on':
        data = np.fromfile(tissueName+'_T.bin', dtype=np.ubyte)
        nbins = int(np.cbrt(data.shape[0]))
        tissue_vox = data.reshape(nbins, nbins, nbins)
        tissue2d = tissue_vox[:,:,1]
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.imshow(tissue2d, cmap='jet')
        plt.show()
    print('All tissue files created (and maybe visualized)') 
        

def make_tissue_list(wave):
    tissue_list = []
    for i in range(len(wave)):
        tissueName = 'tissue_'+str(wave['nm'][i])
        tissue_list.append(tissueName)
    return tissue_list        
        
        
''' Function to run Monte Carlo simulation
- loop through tissue structure at different wavelengths
- implement multiprocessing parallelization to increase speed of computation
'''  

# OLD mc_simulation
#def mc_simulation(wave):
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
def visualize_fluence(wave, video = 'off'):
    eng = mateng.start_matlab()
    for i in tqdm(range(len(wave))):
        tissueName = 'tissue_'+str(wave['nm'][i])
        #print(tissueName)
        st = eng.lookfluence(float(wave['nm'][i]), tissueName, nargout=1)
        if st == 1:
            print('Tissue structure successfully visualized!')
        else:
            print('Error, check input args or see look.m!')
    eng.quit()
        
    if video == 'on':        
        img=[]
        for i in range(len(wave)):
            tissueName = 'tissue_'+str(wave['nm'][i])+'_Fzx.jpg' # OR '_Fzy.jpg'
            print(tissueName)
            img.append(cv2.imread(tissueName))
            
        height,width,layers=img[1].shape
        video=cv2.VideoWriter('fluence2.mp4',-1,1,(width,height))

        for j in range(len(wave)):
            video.write(img[j])

        cv2.destroyAllWindows()
        video.release()
        
    print('All tissue files created and visualized)') 
        

'''================================== run main code ================================='''


if __name__ == '__main__':
    
    wv = pd.read_csv('wave2.csv') # import wavelength list
    
    create_tissue(wv, visualize = 'on') # create tissue structure (turn on visualization)
    
    names = make_tissue_list(wv) # create list of tissue names >> #mc_simulation(wv)
    
    processes = [] #NUM_ROUNDS = len(names)//MAX_NUM_CORES_TO_USE

    # Loop through list of names and call "mc_simulation" in each process
    for i, name in enumerate(names):
        process = Process(target=mc_simulation, args=(name,)) # create process object
        processes.append(process)
        process.start() # spawn process by calling start() method.
    
    # Wait for Python process to end before starting the next process.
    for process in processes:
        process.join()
    
    visualize_fluence(wv, video = 'on') # visualize fluence maps
