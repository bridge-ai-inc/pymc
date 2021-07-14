from pymc import CreateTissue
import numpy as np
import matplotlib.pyplot as plt

tissue = CreateTissue(0.1, 0.15, 0.75, 200)

print('tissue id is: ' + tissue.id)
print(tissue)
print('Default binsize')
print('Tissue binsize is: ' + str(tissue.binsize))
tissue.view()
print('Update binsize')
tissue.set_thickness(1.50)
print('New tissue binsize is: ' + str(tissue.binsize))
tissue.view()
# tissue.run_monte_carlo(10.0)

# data = np.fromfile('tissue_TKLM0S_T.bin', dtype=np.ubyte)
# # print(data.shape)
# print(' ')

#thickness = 1.5
#width = 2.
# nbins = int(np.cbrt(data.shape[0]))
# binsize = 0.005


# tissue_vox = data.reshape(nbins, nbins, nbins)
# tissue2d = tissue_vox[:, :, int(nbins/2)] # print(tissue2d.shape)


# fig, ax = plt.subplots(figsize=(6, 6))
# ax.imshow(tissue2d, cmap='jet', interpolation='none', 
#             extent=[0,binsize*nbins,binsize*nbins,0])
# ax.set_aspect('auto')
# plt.show()
