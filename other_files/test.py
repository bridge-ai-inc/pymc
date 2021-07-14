

# TEST VISUALIZATION AND VIDEO 'ON'

print(__doc__)

# run external scripts
import matlab.engine as mateng
import os

# data manipulation, visualization & miscellaneous
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
from tqdm import tqdm


path_main = '..'
path_data = './src_data'

os.chdir(path_data)

def create_tissue(wave, visualize = 'on'):
    eng = mateng.start_matlab()
    for i in tqdm(range(len(wave))):
        tissueName = 'test_tiss_'+str(wave['nm'][i])
        #print(tissueName)
        st = eng.tissuestruct(float(wave['nm'][i]), tissueName, nargout=1)
        if st == 1:
            print('Tissue structure successfully created!')
        else:
            print("Error, check 'tissuestruct' script in MATLAB!")
    eng.quit()
    
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
    
    
def visualize_fluence(wave, video = 'off'):
    eng = mateng.start_matlab()
    for i in tqdm(range(len(wave))):
        tissueName = 'tissue_'+str(wave['nm'][i])
        #print(tissueName)
        st = eng.lookfluence(float(wave['nm'][i]), tissueName, nargout=1)
        if st == 1:
            print('Tissue structure successfully visualized!')
        else:
            print('Possible error, check look.m code in MATLAB!')
    eng.quit()
        
    if video == 'on':        
        img=[]
        for i in range(len(wave)):
            tissueName = 'tissue_'+str(wave['nm'][i])+'_Fzx.jpg' # OR '_Fzy.jpg'
            print(tissueName)
            img.append(cv2.imread(tissueName))
            
        height,width,layers=img[1].shape
        video=cv2.VideoWriter('fluence.mp4',-1,1,(width,height))

        for j in range(len(wave)):
            video.write(img[j])

        cv2.destroyAllWindows()
        video.release()
        
    print('All tissue files created (and maybe visualized)') 



if __name__ == '__main__':
    wv = pd.read_csv('wave2.csv') # import wavelength list
    create_tissue(wv, visualize = 'on') # call create_tissue (turn on visualization)
    visualize_fluence(wv, video = 'on')
   