## Default modules imported. Import more if you need to.

import numpy as np


#########################################
### Hamming distance computation
### You can call the function hamdist with two
### uint32 bit arrays of the same size. It will
### return another array of the same size with
### the elmenet-wise hamming distance.
hd8bit = np.zeros((256,))
for i in range(256):
    v = i
    for k in range(8):
        hd8bit[i] = hd8bit[i] + v%2
        v=v//2


def hamdist(x,y):
    dist = np.zeros(x.shape)
    g = x^y
    for i in range(4):
        dist = dist + hd8bit[g%256]
        g = g // 256
    return dist
#########################################


# CENSUS TRANSFORM FROM PSET 3 KEY
def census(img):
    
    W = img.shape[1]; H = img.shape[0]
    c = np.zeros([H,W],dtype=np.uint32)
    inc = np.uint32(1)
    
    for dx in range(-2,3):
        for dy in range(-2,3):
            
            if dx == 0 and dy == 0:
                continue
            
            cx0 = np.maximum(0,-dx); dx0 = np.maximum(0,dx)
            cx1 = W-dx0; dx1 = W-cx0
            
            cy0 = np.maximum(0,-dy); dy0 = np.maximum(0,dy)
            cy1 = H-dy0; dy1 = H-cy0
            
            c[cy0:cy1,cx0:cx1] = c[cy0:cy1,cx0:cx1] + \
                inc*(img[cy0:cy1,cx0:cx1] > img[dy0:dy1,dx0:dx1])
                
            inc = inc*2
            
    return c

# Copy this from solution to problem 2.
def buildcv(left,right,dmax):

    # shape[0] = H, shape[1] = W
    shape = left.shape
    W = shape[1]
    H = shape[0]

    c_left = census(left)
    c_right = census(right)

    V = np.zeros([H,W,dmax+1])

    for k in range(dmax+1):

        # if the index is outside the image, assign max cost        
        V[:,0:k,k] = 24        
        # else set the cost to be hamming distance
        V[:,k:-1,k] = hamdist(c_right[:,:(-k-1)],c_left[:,k:-1])
        
    return V

# augmented cost volume maker from problem 3a
def Cbar(cv,P1,P2):
    H = cv.shape[0]
    W = cv.shape[1]
    D = cv.shape[2]
    
    dd = np.zeros([H,W],dtype=np.uint32)
    
    DD = np.arange(D).reshape([1,-1])*np.ones([H,1])
    
    # z = np.zeros(cv.shape)
    C_ = np.zeros(cv.shape)    

    min_opts = np.zeros(cv.shape)

    # x=0 case
    C_[:,0,:] = cv[:,0,:]
    ## forward track for every horizontal line
    for xf in range(W):
        # x=0 case already computed above
        if xf==0:
            continue

        # Ctilde for each epipolar line
        Ct = C_[:,xf-1,:]-np.min(C_[:,xf-1,:],axis=1).reshape([H,1])

        # compute the 4 options for min of Ctilde for each d in each horizontal line
        options = np.zeros([H,D,4])

        # print(Ct[:,1].shape)
        options[:,0,:] = np.stack((P2*np.ones([H]), (P2+1)*np.ones([H]), Ct[:,1]+P1*np.ones([H]), Ct[:,0]),axis = 1)
        options[:,1:D-1,:] = np.stack((P2*np.ones([H,D-2]), Ct[:,0:D-2]+P1*np.ones([H,D-2]), Ct[:,2:D]+P1*np.ones([H,D-2]), Ct[:,1:D-1]),axis=2)
        options[:,D-1,:] = np.stack((P2*np.ones([H]),Ct[:,D-2]+P1*np.ones([H]), (P2+1)*np.ones([H]), Ct[:,D-1]),axis = 1)

        # find the argmin for each d in each horizontal line
        min_opts[:,xf,:] = np.argmin(options[:,:,:], axis = 2)

        # based on which option was argmin, store z and C_ 
        
        # this problem doesn't require z
        # z[:,xf,:] = np.where(min_opts[:,xf,:] == 0, np.argmin(Ct[:,:],axis=1).reshape([-1,1])*np.ones([1,D]), z[:,xf,:])
        # z[:,xf,:] = np.where(min_opts[:,xf,:] == 1, DD-1, z[:,xf,:])
        # z[:,xf,:] = np.where(min_opts[:,xf,:] == 2, DD+1, z[:,xf,:])
        # z[:,xf,:] = np.where(min_opts[:,xf,:] == 3, DD, z[:,xf,:])

        C_[:,xf,:] = cv[:,xf,:] 
        C_[:,xf,:] = np.where(min_opts[:,xf,:] == 0, options[:,:,0] + C_[:,xf,:], C_[:,xf,:])
        C_[:,xf,:] = np.where(min_opts[:,xf,:] == 1, options[:,:,1] + C_[:,xf,:], C_[:,xf,:])
        C_[:,xf,:] = np.where(min_opts[:,xf,:] == 2, options[:,:,2] + C_[:,xf,:], C_[:,xf,:])
        C_[:,xf,:] = np.where(min_opts[:,xf,:] == 3, options[:,:,3] + C_[:,xf,:], C_[:,xf,:]) 
        
    return C_
# Do SGM. First compute the augmented / smoothed cost volumes along 4
# directions (LR, RL, UD, DU), and then compute the disparity map as
# the argmin of the sum of these cost volumes. 
def SGM(cv,P1,P2):
    H = cv.shape[0]
    W = cv.shape[1]
    D = cv.shape[2]

    dd = np.zeros([H,W],dtype=np.uint32)

    # use the same forward path algorithm as in problem 3a (Cbar function)
    # change the shape of cv to compute different paths, and then change back after computing C_
    
    # same as in 3a without backtracking
    C_lr = Cbar(cv,P1,P2)
    
    # horizontal flip of cv, then horizontal flip of C_
    C_rl = Cbar(cv[:,::-1,:],P1,P2)[:,::-1,:]

    # transpose of cv along X,Y dimensions, then transpose of resulting C_    
    C_ud = np.transpose(Cbar(np.transpose(cv,(1,0,2)),P1,P2),(1,0,2))
    
    # transpose and horizontal flip <=> vertical and flipped
    C_du = np.transpose(Cbar(np.transpose(cv[::-1,:,:],(1,0,2)),P1,P2),(1,0,2))[::-1,:,:]

    # add augmented Cost volumes together and compute argmin along D
    C_ = C_lr + C_rl + C_ud + C_du

    return np.argmin(C_,axis=2)

    
    
########################## Support code below

from skimage.io import imread, imsave
from os.path import normpath as fn # Fixes window/linux path conventions
import matplotlib.cm as cm
import warnings
warnings.filterwarnings('ignore')


left = np.float32(imread(fn('inputs/left.jpg')))/255.
right = np.float32(imread(fn('inputs/right.jpg')))/255.

left_g = np.mean(left,axis=2)
right_g = np.mean(right,axis=2)
                   
cv = buildcv(left_g,right_g,50)
d = SGM(cv,0.5,16)

# Map to color and save
dimg = cm.jet(np.minimum(1,np.float32(d.flatten())/50.))[:,0:3]
dimg = dimg.reshape([d.shape[0],d.shape[1],3])
imsave(fn('outputs/prob3b.jpg'),dimg)
