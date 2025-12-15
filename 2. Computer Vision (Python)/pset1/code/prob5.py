## Default modules imported. Import more if you need to.

import numpy as np
from skimage.io import imread, imsave
from scipy.signal import convolve2d as conv2


# Fill this out
def kernpad(K,size):
    Ko = np.zeros(size,dtype=np.float32)
    Ko[:K.shape[0],:K.shape[1]] = K
    Ko = np.roll(Ko, int(-(K.shape[0]-1)/2),axis=0)    
    Ko = np.roll(Ko, int(-(K.shape[1]-1)/2),axis=1)    
    return Ko

########################## Support code below

from os.path import normpath as fn # Fixes window/linux path conventions
import warnings
warnings.filterwarnings('ignore')

img = np.float32(imread(fn('inputs/p5_inp.jpg')))/255.

# Create Gaussian Kernel
x = np.float32(range(-21,22))
x,y = np.meshgrid(x,x)
G = np.exp(-(x*x+y*y)/2/9.)
G = G / np.sum(G[:])


# Traditional convolve
v1 = conv2(img,G,'same','wrap')

# Convolution in Fourier domain
G = kernpad(G,img.shape)
v2f = np.fft.fft2(G)*np.fft.fft2(img)
v2 = np.real(np.fft.ifft2(v2f))

# Stack them together and save
out = np.concatenate([img,v1,v2],axis=1)
out = np.minimum(1.,np.maximum(0.,out))

imsave(fn('outputs/prob5.jpg'),out)

## tests the difference in normal convolution and fft multiplication
# test = v1-v2 
# print(np.max(np.abs(test))) # on the order of e-06 for the maximum difference
# # imsave(fn('outputs/test.jpg'),test)