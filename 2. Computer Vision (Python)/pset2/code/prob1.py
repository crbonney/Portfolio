## Default modules imported. Import more if you need to.

import numpy as np
from skimage.io import imread, imsave


## Fill out these functions yourself

# Copy from Pset1/Prob6 
def im2wv(img,nLev):
    W = 1/2*np.array([[1,1,1,1],[-1,1,-1,1],[-1,-1,1,1],[1,-1,-1,1]])
    L = np.copy(img)
    dim = img.shape
    output = []    
    for i in range(nLev):
        a = L[::2,::2].reshape(-1)
        b = L[1::2,::2].reshape(-1)
        c = L[::2,1::2].reshape(-1)
        d = L[1::2,1::2].reshape(-1)
        [L,H1,H2,H3] = np.matmul(W,[a,b,c,d])
        dim = [dim[0]//2, dim[1]//2]
        L = L.reshape([dim[0],dim[1]])
        H1 = H1.reshape([dim[0],dim[1]])
        H2 = H2.reshape([dim[0],dim[1]])
        H3 = H3.reshape([dim[0],dim[1]])
        output.append([H1,H2,H3])
    output.append(L)
    return output


# Copy from Pset1/Prob6 
def wv2im(pyr):

    Wt = 1/2*np.array([[1,1,1,1],[-1,1,-1,1],[-1,-1,1,1],[1,-1,-1,1]]).T
    pyrpopper = pyr.copy()
    L = pyrpopper.pop();
    for i in range(np.shape(pyrpopper)[0]):
        [H1,H2,H3]  = pyrpopper.pop()
        dim = L.shape
        L = L.reshape(-1)
        H1 = H1.reshape(-1)
        H2 = H2.reshape(-1)
        H3 = H3.reshape(-1)
        
        [a,b,c,d] = np.matmul(Wt,[L,H1,H2,H3])
        
        a = a.reshape([dim[0],dim[1]])
        b = b.reshape([dim[0],dim[1]])
        c = c.reshape([dim[0],dim[1]])
        d = d.reshape([dim[0],dim[1]])
        L = np.zeros([dim[0]*2,dim[1]*2])
        L[::2,::2] = a
        L[1::2,::2] = b
        L[::2,1::2] = c
        L[1::2,1::2] = d

    return L




# Fill this out
# You'll get a numpy array/image of coefficients y
# Return corresponding coefficients x (same shape/size)
# that minimizes (x - y)^2 + lmbda * abs(x)
def denoise_coeff(y,lmbda):
    
    dim = y.shape
    y = y.reshape(-1)
    
    # test all pixels to see what case they are (described in solution.pdf)
    case1 = np.where((y > lmbda/2))[0]
    case2 = np.where((y < -lmbda/2))[0]
    case3 = np.where((y <= lmbda/2) & (y >= -lmbda/2))[0]
    
    # update pixels to minimum based on case
    y[case1] = y[case1]-lmbda/2
    y[case2] = y[case2]+lmbda/2
    y[case3] = 0
    
    ## naive impementation - loop over all pixels
    # for i in range(y.shape[0]):
    #     for j in range(y.shape[1]):
    #         if y[i][j] > lmbda/2:
    #             y[i][j] = y[i][j] - lmbda/2
    #         elif y[i][j] < -lmbda/2:
    #             y[i][j] = y[i][j] + lmbda/2
    #         else:
    #             y[i][j] = 0

    y = y.reshape(dim)
    return y

########################## Support code below

from os.path import normpath as fn # Fixes window/linux path conventions
import warnings
warnings.filterwarnings('ignore')


# Utility functions to clip intensities b/w 0 and 1
# Otherwise imsave complains
def clip(im):
    return np.maximum(0.,np.minimum(1.,im))



############# Main Program

lmain = 0.88

img = np.float32(imread(fn('inputs/p1.png')))/255.

pyr = im2wv(img,4)

for i in range(len(pyr)-1):
    for j in range(2):
        pyr[i][j] = denoise_coeff(pyr[i][j],lmain/(2**i))
    pyr[i][2] = denoise_coeff(pyr[i][2],np.sqrt(2)*lmain/(2**i))
    
im = wv2im(pyr)        
imsave(fn('outputs/prob1.png'),clip(im))
