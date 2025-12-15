## Default modules imported. Import more if you need to.

import numpy as np
from skimage.io import imread, imsave

# Fill this out
# X is input color image
# K is the support of the filter (2K+1)x(2K+1)
# sgm_s is std of spatial gaussian
# sgm_i is std of intensity gaussian
def bfilt(X,K,sgm_s,sgm_i):
    # Placeholder

    dims = [X.shape[0], X.shape[1]]
    
    X_pad = np.zeros([dims[0]+2*K,dims[1]+2*K,3])
    X_pad[K:dims[0]+K,K:dims[1]+K,:] = X
    # create gaussian kernel (does not depend on image data)
    Gaussian = np.arange(-K, K+1)**2
    Gaussian = Gaussian + Gaussian[:,np.newaxis]
    Gaussian = np.exp(-Gaussian/(2*sgm_s))

    
    Y = np.zeros_like(X)
    # create bilateral kernel for each pixel from image data
    for i in range(K,dims[0]+K):
        for j in range(K,dims[1]+K):
            B = np.zeros([2*K+1, 2*K+1])
            for ki in range(2*K+1):
                for kj in range(2*K+1):
                    xindex = i+ki-K
                    yindex = j+kj-K
                    
                    intensity_diff = X_pad[i,j,:] - X_pad[xindex,yindex,:]
                    sq_diff = intensity_diff.dot(intensity_diff)
                    B[ki,kj] = np.exp(-sq_diff/sgm_i)

            B = B*Gaussian
            B = B/np.sum(B,axis=None)
            B = B[:,:,np.newaxis]
            X_range = X_pad[i-K:i+K+1,j-K:j+K+1]
            Y[i-K,j-K,0] = np.sum(X_range[:,:,0]*B[:,:,0],axis=None)
            Y[i-K,j-K,1] = np.sum(X_range[:,:,1]*B[:,:,0],axis=None)
            Y[i-K,j-K,2] = np.sum(X_range[:,:,2]*B[:,:,0],axis=None)
                    

    #rearrange loops to have biggest loops in the middle?
    return Y


########################## Support code below

def clip(im):
    return np.maximum(0.,np.minimum(1.,im))

from os.path import normpath as fn # Fixes window/linux path conventions
import warnings
warnings.filterwarnings('ignore')

img1 = np.float32(imread(fn('inputs/p4_nz1.jpg')))/255.
img2 = np.float32(imread(fn('inputs/p4_nz2.jpg')))/255.

K=9

print("Creating outputs/prob4_1_a.jpg")
im1A = bfilt(img1,K,2,0.5)
imsave(fn('outputs/prob4_1_a.jpg'),clip(im1A))


print("Creating outputs/prob4_1_b.jpg")
im1B = bfilt(img1,K,4,0.25)
imsave(fn('outputs/prob4_1_b.jpg'),clip(im1B))

print("Creating outputs/prob4_1_c.jpg")
im1C = bfilt(img1,K,16,0.125)
imsave(fn('outputs/prob4_1_c.jpg'),clip(im1C))

# Repeated application
print("Creating outputs/prob4_1_rep.jpg")
im1D = bfilt(img1,K,2,0.125)
for i in range(8):
    im1D = bfilt(im1D,K,2,0.125)
imsave(fn('outputs/prob4_1_rep.jpg'),clip(im1D))

# Try this on image with more noise    
print("Creating outputs/prob4_2_rep.jpg")
im2D = bfilt(img2,2,8,0.125)
for i in range(16):
    im2D = bfilt(im2D,K,2,0.125)
imsave(fn('outputs/prob4_2_rep.jpg'),clip(im2D))
