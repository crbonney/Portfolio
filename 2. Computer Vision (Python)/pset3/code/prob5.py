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





## Fill out these functions yourself

# Compute a 5x5 census transform of the grayscale image img.
# Return a uint32 array of the same shape
def census(img):

    W = img.shape[1]
    H = img.shape[0]

    c = np.zeros([H,W],dtype=np.uint32)
    
    # pad image with 0s to deal with edge pixels
    img_pad = np.zeros([H+4,W+4])
    img_pad[2:H+2,2:W+2] = img

    # the power to raise the ith neighboring pixel for transform
    powers = np.arange(24)

    for i in range(H):
        for j in range(W):
                center = img[i,j]
                local_img = img_pad[i:i+5,j:j+5]

                local_img = local_img.reshape(-1)
                # delete the center pixel
                local_img = np.delete(local_img,12)

                # sum of the boolean of each ith pixel < center * 2^i
                c[i,j] = np.sum((center > local_img)*2**powers)

    return c
    
def census2(img):
    
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


# Given left and right image and max disparity D_max, return a disparity map
# based on matching with  hamming distance of census codes. Use the census function
# you wrote above.
#
# d[x,y] implies that left[x,y] matched best with right[x-d[x,y],y]. Disparity values
# should be between 0 and D_max (both inclusive).
def smatch(left,right,dmax):

    # shape[0] = H, shape[1] = W
    shape = left.shape
    W = shape[1]
    H = shape[0]

    c_left = census2(left)
    c_right = census2(right)

    V = np.zeros([H,W,dmax])
    d = np.zeros(left.shape)


    for i in range(H):
        for j in range(W):
            for k in range(dmax):
                # print("i:", i, ", j:", j, "j-k:", j-k)
                if j-k < 0 : 
                    V[i,j,k] = 24
                else:
                    V[i,j,k] = hamdist(c_right[i,j-k],c_left[i,j])

                d[i,j] = np.argmin(V[i,j,:])

    return d
    
    
########################## Support code below

from skimage.io import imread, imsave
from os.path import normpath as fn # Fixes window/linux path conventions
import matplotlib.cm as cm
import warnings
warnings.filterwarnings('ignore')


left = imread(fn('inputs/left.jpg'))
right = imread(fn('inputs/right.jpg'))
# c = census(left)
# c2= census2(left)
d = smatch(left,right,40)

# Map to color and save
dimg = cm.jet(np.minimum(1,np.float32(d.flatten())/20.))[:,0:3]
dimg = dimg.reshape([d.shape[0],d.shape[1],3])
imsave(fn('outputs/prob5.png'),dimg)
