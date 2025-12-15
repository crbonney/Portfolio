## Default modules imported. Import more if you need to.

import numpy as np
from skimage.io import imread, imsave
import matplotlib.pyplot as plt

# Fill this out
# X is input 8-bit grayscale image
# Return equalized image with intensities from 0-255
def histeq(X):
    #get dims of X to reshape at end
    dims = [np.size(X,0), np.size(X,1)]
    #flatten X
    X = X.reshape(-1)
    #get which intensities are in X and how many of each
    histX = np.unique(X, return_counts = True)
    #intensities in X
    Xvals = histX[0]
    #how many counts of the intensity in Xvals are in the image
    Xcounts = histX[1]
    #build a cumulative distribution by summing counts below an intensity level
    cum_dist = np.array([])

    # for all intensities
    for i in range(256):
        #find the index of the intensity in Xvals
        max_index = np.where(Xvals >= i)[0]
        #if it doesnt exist in Xvals, all pixels are below this intensity
        max_index = max_index[0] if np.size(max_index) > 0 else np.size(X)
        
        #sum all the elements in Xcounts below max_index 
        #ie, number of pixels with intensity < i
        cum_dist = np.append(cum_dist, sum(Xcounts[0:max_index]))

    #normalize distribution by dividing by number of pixels to get h
    h = cum_dist/np.size(X)
    #apply pointwise opperation
    X = h[X]*255 
    #reshape flattened X into image
    X = X.reshape(dims)
    return X
    

########################## Support code below

from os.path import normpath as fn # Fixes window/linux path conventions
import warnings
warnings.filterwarnings('ignore')

img = imread(fn('inputs/p2_inp.jpg'))
# in_pixels = np.copy(img).reshape(-1)

out = histeq(img)
# out_pixels = np.copy(out).reshape(-1)

out = np.maximum(0,np.minimum(255,out))
out = np.uint8(out)

imsave(fn('outputs/prob2.jpg'),out)

plt.imshow(out, cmap='gray')