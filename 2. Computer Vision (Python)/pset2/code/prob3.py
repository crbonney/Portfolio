### Default modules imported. Import more if you need to.
### DO NOT USE linalg.lstsq from numpy or scipy

import numpy as np
from skimage.io import imread, imsave

## Fill out these functions yourself


# Inputs:
#    imgs: A list of N color images, each of which is HxWx3
#    L:    An Nx3 matrix where each row corresponds to light vector
#          for corresponding image.
#    mask: A 0-1 mask of size HxW, showing where observed data is 'valid'.
#
# Returns nrm:
#    nrm: HxWx3 Unit normal vector at each location.
#
# Be careful about division by zero at mask==0 for normalizing unit vectors.
def pstereo_n(imgs, L, mask):

    gray_imgs = np.mean(imgs, axis=3) # mean across color channels
    size = np.shape(gray_imgs) #img_number, x, y


    # pre-calculate the pseudoinverse of L
    # inv(L.T*L) is guarenteed to exist for at least 3 linearly independent light sources
    Lsq = np.matmul(L.T,L)
    pinvL = np.matmul(np.linalg.inv(Lsq),L.T)

    # reshape image shaped to vectors for matrix math
    gray_imgs = gray_imgs.reshape([size[0],-1])
    mask = mask.reshape(-1)

    #initialize nrm to be 0, masked terms will remain 0
    nrm = np.zeros([mask.size,3])

    #all points on the mask
    valid = np.where(mask > 0)[0]

    #calculates the surface norm for all pixels not masked at once
    nrm[valid,:] = np.matmul(pinvL,gray_imgs[:,valid]).T
    
    #normalize magnitude for the computed nrms 
    mag = np.linalg.norm(nrm,axis=1).reshape([-1,1])
    nrm[valid,:] = nrm[valid,:]/mag[valid]

    # reshape into image
    nrm = nrm.reshape([size[1],size[2],3])
    return nrm


# Inputs:
#    imgs: A list of N color images, each of which is HxWx3
#    nrm:  HxWx3 Unit normal vector at each location (from pstereo_n)
#    L:    An Nx3 matrix where each row corresponds to light vector
#          for corresponding image.
#    mask: A 0-1 mask of size HxW, showing where observed data is 'valid'.
#
# Returns alb:
#    alb: HxWx3 RGB Color Albedo values
#
# Be careful about division by zero at mask==0.
def pstereo_alb(imgs, nrm, L, mask):

    size = np.shape(imgs) #img_number, x, y, color
    imgs = np.array(imgs)
    alb = np.zeros([size[1],size[2],3])

    imgs = imgs.reshape([size[0],-1,3])
    mask = mask.reshape(-1)
    nrm = nrm.reshape([-1,3])
    alb = alb.reshape([-1,3])
    
    valid = np.where(mask > 0)[0]
    
    for i in valid:
        if mask[i]:
            I = imgs[:,i,:]
            nhat = nrm[i:i+1,:].T
            Ln = np.matmul(L,nhat)
            alb[i,:] = np.reshape(np.matmul(I.T,Ln)/np.linalg.norm(Ln),[-1])
                
                
    # for x in range(size[1]):
    #     for y in range(size[2]):
    #         for rgb in range(3):
    #             if mask[x,y]:
    #                 I = imgs[:,x:x+1,y,rgb]
    #                 nhat = nrm[x:x+1,y,:].T
                    
    #                 Ln = np.matmul(L,nhat)

    #                 alb[x,y,rgb] = np.matmul(I.T,Ln)/np.linalg.norm(Ln)
    
    alb = alb.reshape([size[1],size[2],3])
    return alb

    
########################## Support code below

from os.path import normpath as fn # Fixes window/linux path conventions
import warnings
warnings.filterwarnings('ignore')

### Light directions matrix
L = np.float32( \
                [[  4.82962877e-01,   2.58819044e-01,   8.36516321e-01],
                 [  2.50000030e-01,   2.58819044e-01,   9.33012664e-01],
                 [ -4.22219593e-08,   2.58819044e-01,   9.65925813e-01],
                 [ -2.50000000e-01,   2.58819044e-01,   9.33012664e-01],
                 [ -4.82962966e-01,   2.58819044e-01,   8.36516261e-01],
                 [ -5.00000060e-01,   0.00000000e+00,   8.66025388e-01],
                 [ -2.58819044e-01,   0.00000000e+00,   9.65925813e-01],
                 [ -4.37113883e-08,   0.00000000e+00,   1.00000000e+00],
                 [  2.58819073e-01,   0.00000000e+00,   9.65925813e-01],
                 [  4.99999970e-01,   0.00000000e+00,   8.66025448e-01],
                 [  4.82962877e-01,  -2.58819044e-01,   8.36516321e-01],
                 [  2.50000030e-01,  -2.58819044e-01,   9.33012664e-01],
                 [ -4.22219593e-08,  -2.58819044e-01,   9.65925813e-01],
                 [ -2.50000000e-01,  -2.58819044e-01,   9.33012664e-01],
                 [ -4.82962966e-01,  -2.58819044e-01,   8.36516261e-01]])


# Utility functions to clip intensities b/w 0 and 1
# Otherwise imsave complains
def clip(im):
    return np.maximum(0.,np.minimum(1.,im))


############# Main Program


# Load image data
imgs = []
for i in range(L.shape[0]):
    imgs = imgs + [np.float32(imread(fn('inputs/phstereo/img%02d.png' % i)))/255.]
gray_imgs = np.mean(imgs, axis=3)
mask = np.float32(imread(fn('inputs/phstereo/mask.png')) > 0)

nrm = pstereo_n(imgs,L,mask)

nimg = nrm/2.0+0.5
nimg = clip(nimg * mask[:,:,np.newaxis])
imsave(fn('outputs/prob3_nrm.png'),nimg)
print("norm calculated")

alb = pstereo_alb(imgs,nrm,L,mask)

alb = alb / np.max(alb[:])
alb = clip(alb * mask[:,:,np.newaxis])

imsave(fn('outputs/prob3_alb.png'),alb)
