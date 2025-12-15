## Default modules imported. Import more if you need to.

import numpy as np
from skimage.io import imread, imsave, imshow
from scipy.signal import convolve2d as conv2

# Different thresholds to try
T0 = 0.5
T1 = 1.0
T2 = 1.5


########### Fill in the functions below

# Return magnitude, theta of gradients of X
def grads(X):

    #kernel of sobel derivative in X direction
    #kernel in Y direction is just the transpose of this
    sobelX = np.array([[1, 0, -1],[2, 0, -2],[1, 0, -1]])

    #get the sobel derivatives in x,y directions using convolutions
    Ix = conv2(img, sobelX, mode='same', boundary='symm')
    Iy = conv2(img, sobelX.T, mode='same', boundary='symm')

    #magnitude and angle of derivatives 
    H = np.sqrt(Ix**2+Iy**2)
    theta = np.arctan2(Iy,Ix)    

    return H,theta

def nms(E,H,theta):
    
    #round angles to 0, 45, 90, 135, 180=0, ...
    # 0 = vertical, 1 = 45deg cw, 2 = horizontal, 3 = 45deg ccw
    direction = np.round(theta*4/np.pi) % 4
    
    #set all boundary pixels to 0, (assume boundary cannot be an edge)
    E[0,:] = 0
    E[:,0] = 0
    E[-1,:] = 0
    E[:,-1] = 0
    
    # for all pixels except boundaries of image
    for i in range(1,np.size(E,0)-1):
        for j in range(1,np.size(E,1)-1):
            #if previously calculated as edge...
            if E[i,j] == 1:
                
                #compare the magnitude of derivative to points along angle
                d = direction[i,j]
                # vertical line 
                if d == 0:
                    E[i,j] = H[i,j-1] < H[i,j] > H[i,j+1]
                # 45deg cw line
                elif d == 1:
                    E[i,j] = H[i+1,j-1] < H[i,j] > H[i-1,j+1]
                # horizontal line
                elif d == 2:
                    E[i,j] = H[i-1,j] < H[i,j] > H[i+1,j]
                # 45deg ccw line
                elif d == 3: 
                    E[i,j] = H[i-1,j-1] < H[i,j] > H[i+1,j+1]
                
    
    return E

########################## Support code below

from os.path import normpath as fn # Fixes window/linux path conventions
import warnings
warnings.filterwarnings('ignore')

img = np.float32(imread(fn('inputs/p3_inp.jpg')))/255.

H,theta = grads(img)


imsave(fn('outputs/prob3_a.jpg'),H/np.max(H[:]))

imshow(theta)
imshow(H/np.max(H[:]))


## Part b

E0 = np.float32(H > T0)
E1 = np.float32(H > T1)
E2 = np.float32(H > T2)

imsave(fn('outputs/prob3_b_0.jpg'),E0)
imsave(fn('outputs/prob3_b_1.jpg'),E1)
imsave(fn('outputs/prob3_b_2.jpg'),E2)

E0n = nms(E0,H,theta)
E1n = nms(E1,H,theta)
E2n = nms(E2,H,theta)

imsave(fn('outputs/prob3_b_nms0.jpg'),E0n)
imsave(fn('outputs/prob3_b_nms1.jpg'),E1n)
imsave(fn('outputs/prob3_b_nms2.jpg'),E2n)
