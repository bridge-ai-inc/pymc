import os
import pandas as pd
from multiprocessing import Process, current_process

# Change to dir containing matlab code, c code and data 
path_data = './src_data'
os.chdir(path_data)

MAX_NUM_CORES_TO_USE = 6


def mc_simulation(name):
    d = os.system('./mcxyz ' + name)
    print('simulating tissue ' + name)
    print('Error Code:', d, '...No errors!')
    
    print(f"Process ID: {os.getpid()}")

    # We can also use the "current_process" function
    print(f"Process Name: {current_process().name}")

        
def make_tissue_list(wave):
    tissue_list = []
    for i in range(len(wave)):
        tissueName = 'tissue_'+str(wave['nm'][i])
        tissue_list.append(tissueName)
    return tissue_list
    

if __name__ == '__main__':
    
    wv = pd.read_csv('wave2.csv')  
    names = make_tissue_list(wv)
    #print(names)
    processes = []
    NUM_ROUNDS = len(names)//MAX_NUM_CORES_TO_USE

    # Loop through list of names, call "mc_simulation", store and start each call
    for i, name in enumerate(names):
        process = Process(target=mc_simulation, args=(name,))
        processes.append(process)

        # Processes are spawned by creating a Process object, then calling its start() method.
        process.start()

    # Wait for Python process to end before starting the next process.
    for process in processes:
        process.join()

