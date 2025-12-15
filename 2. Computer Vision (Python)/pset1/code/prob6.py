## Default modules imported. Import more if you need to.

import numpy as np
from skimage.io import imread, imsave


## Fill out these functions yourself

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


def wv2im(pyr):

    Wt = 1/2*np.array([[1,1,1,1],[-1,1,-1,1],[-1,-1,1,1],[1,-1,-1,1]]).T
    pyrpopper = pyr.copy()
    L = pyrpopper.pop();
    for i in range(np.shape(pyrpopper)[0]):
        [H1,H2,H3]  = pyrpopper.pop()
        L = L.reshape(-1)
        H1 = H1.reshape(-1)
        H2 = H2.reshape(-1)
        H3 = H3.reshape(-1)
        
        [a,b,c,d] = np.matmul(Wt,[L,H1,H2,H3])
        
        dim = int(np.sqrt(np.size(a)))
        a = a.reshape([dim,dim])
        b = b.reshape([dim,dim])
        c = c.reshape([dim,dim])
        d = d.reshape([dim,dim])
        L = np.zeros([dim*2,dim*2])
        L[::2,::2] = a
        L[1::2,::2] = b
        L[::2,1::2] = c
        L[1::2,1::2] = d

    return L



########################## Support code below

from os.path import normpath as fn # Fixes window/linux path conventions
import warnings
warnings.filterwarnings('ignore')


# Utility functions to clip intensities b/w 0 and 1
# Otherwise imsave complains
def clip(im):
    return np.maximum(0.,np.minimum(1.,im))


# Visualize pyramid like in slides
def vis(pyr, lev=0):
    if len(pyr) == 1:
        return pyr[0]/(2**lev)

    sz=pyr[0][0].shape
    sz1 = [sz[0]*2,sz[1]*2]
    img = np.zeros(sz1,dtype=np.float32)

    img[0:sz[0],0:sz[1]] = vis(pyr[1:],lev+1)

    # Just scale / shift gradient images for visualization
    img[sz[0]:,0:sz[1]] = pyr[0][0]*(2**(1-lev))+0.5
    img[0:sz[0],sz[1]:] = pyr[0][1]*(2**(1-lev))+0.5
    img[sz[0]:,sz[1]:] = pyr[0][2]*(2**(1-lev))+0.5

    return img



############# Main Program


img = np.float32(imread(fn('inputs/p6_inp.jpg')))/255.

# Visualize pyramids
pyr = im2wv(img,1)
imsave(fn('outputs/prob6a_1.jpg'),clip(vis(pyr)))

pyr = im2wv(img,2)
imsave(fn('outputs/prob6a_2.jpg'),clip(vis(pyr)))

pyr = im2wv(img,3)
imsave(fn('outputs/prob6a_3.jpg'),clip(vis(pyr)))

# Inverse transform to reconstruct image
im = clip(wv2im(pyr))
imsave(fn('outputs/prob6b.jpg'),im)

# Zero out some levels and reconstruct
for i in range(len(pyr)-1):

    for j in range(3):
        pyr[i][j][...] = 0.

    im = clip(wv2im(pyr))
    imsave(fn('outputs/prob6b_%d.jpg' % i),im)
