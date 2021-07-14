# One can create a pool of processes which will carry out tasks submitted to
# it with the Pool class.

# A process pool object which controls a pool of worker processes to which
# jobs can be submitted. It supports asynchronous results with timeouts and
# callbacks and has a parallel map implementation.

import time
from multiprocessing import Pool
import os
import pandas as pd


def mc_simulation(name):
    d = os.system('./mcxyz ' + name)
    print('Error Code:', d, '...No errors!')

        
def make_tissue_list(wave):
    tissue_list = []
    for i in range(len(wave)):
        tissueName = 'tissue_'+str(wave['nm'][i])
        tissue_list.append(tissueName)
    return tissue_list
            

def multiproc_sim(tissue_list):
    start_time = time.time()
    p = Pool(6)
    result = p.map(mc_simulation, tissue_list)
    p.close()
    p.join()
    
    end_time = time.time() - start_time
    print(f"Processing {len(tissue_list)} tissues took {end_time} time using multiprocessing.")    
    

if __name__ == '__main__':
    wv = pd.read_csv('wave2.csv')  
    tissue_list = make_tissue_list(wv)
    print(tissue_list)
    multiproc_sim(tissue_list)
