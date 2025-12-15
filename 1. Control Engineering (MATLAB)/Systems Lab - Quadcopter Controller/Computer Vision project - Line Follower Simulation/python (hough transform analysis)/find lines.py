## Default modules imported. Import more if you need to.

import numpy as np
from skimage.io import imread, imsave
from scipy.signal import convolve2d as conv2
import time



########### Fill in the functions below

# Return magnitude, theta of gradients of X
# Code from solution key to PSET 1
def grads(X):

    #kernel of sobel derivative in X direction
    #kernel in Y direction is just the transpose of this
    df = np.float32([[1,0,-1]])
    sf = np.float32([[1,2,1]])
    
    #get the sobel derivatives in x,y directions using convolutions
    Ix = conv2(X, sf.T,'same','symm')
    Ix = conv2(Ix, df,'same','symm')

    Iy = conv2(X, sf,'same','symm')
    Iy = conv2(Iy, df.T,'same','symm')

    # sobelX = np.array([[1, 0, -1],[2, 0, -2],[1, 0, -1]])
    # Ix = conv2(img, sobelX, mode='same', boundary='symm')
    # Iy = conv2(img, sobelX.T, mode='same', boundary='symm')

    #magnitude and angle of derivatives 
    H = np.sqrt(Ix**2+Iy**2)
    theta = np.arctan2(Iy,Ix)    

    return H,theta

# Code From soultion key to PSET 1
def nms(E,H,theta):
    
    h, w = E.shape
    E2 = E > 0
    #round angles to 0, 45, 90, 135, 180=0, ...
    # 0 = vertical, 1 = 45deg cw, 2 = horizontal, 3 = 45deg ccw
    direction = np.mod(np.round(theta*4/np.pi), 4)
    
    #set all boundary pixels to 0, (assume boundary cannot be an edge)
    # E[0,:] = 0
    # E[:,0] = 0
    # E[-1,:] = 0
    # E[:,-1] = 0
    
    yx = np.where(np.logical_and(E2, direction == 0))
    E2[yx[0],yx[1]] = np.logical_and(
        H[yx[0],yx[1]] > H[yx[0],np.minimum(w-1,yx[1]+1)],
        H[yx[0],yx[1]] > H[yx[0],np.maximum(0,yx[1]-1)])

    yx = np.where(np.logical_and(E2, direction == 1))
    E2[yx[0],yx[1]] = np.logical_and(
        H[yx[0],yx[1]] > H[np.minimum(h-1,yx[0]+1),np.minimum(w-1,yx[1]+1)],
        H[yx[0],yx[1]] > H[np.maximum(0,yx[0]-1),yx[1]-1])    
    
    yx = np.where(np.logical_and(E2, direction == 2))
    E2[yx[0],yx[1]] = np.logical_and(
        H[yx[0],yx[1]] > H[np.minimum(h-1,yx[0]+1),yx[1]],
        H[yx[0],yx[1]] > H[np.maximum(0,yx[0]-1),yx[1]])

    yx = np.where(np.logical_and(E2, direction == 3))
    E2[yx[0],yx[1]] = np.logical_and(
        H[yx[0],yx[1]] > H[np.maximum(0,yx[0]-1),np.minimum(w-1,yx[1]+1)],
        H[yx[0],yx[1]] > H[np.minimum(h-1,yx[0]+1),yx[1]-1])    

    
    # # for all pixels except boundaries of image
    # for i in range(1,np.size(E,0)-1):
    #     for j in range(1,np.size(E,1)-1):
    #         #if previously calculated as edge...
    #         if E[i,j] == 1:
                
    #             #compare the magnitude of derivative to points along angle
    #             d = direction[i,j]
    #             # vertical line 
    #             if d == 0:
    #                 E[i,j] = H[i,j-1] < H[i,j] > H[i,j+1]
    #             # 45deg cw line
    #             elif d == 1:
    #                 E[i,j] = H[i+1,j-1] < H[i,j] > H[i-1,j+1]
    #             # horizontal line
    #             elif d == 2:
    #                 E[i,j] = H[i-1,j] < H[i,j] > H[i+1,j]
    #             # 45deg ccw line
    #             elif d == 3: 
    #                 E[i,j] = H[i-1,j-1] < H[i,j] > H[i+1,j+1]
                
    return np.float32(E2)

def hough(E, ntheta):
    
    
    h, w = E.shape                               # size of img
    Theta = np.linspace(-np.pi/2,np.pi/2,ntheta) # initialize values for theta
    Y,X = np.where(E > 0)                        # location of edge pixels

    # largest value for radius 
    max_r = np.ceil(np.sqrt(np.max(Y)**2+np.max(X)**2))

    # initialize shape of hough 
    # size of the full diagonal of the image
    Hough = np.zeros([(2*max_r+1).astype('int'), ntheta])

    # reshape for broadcasting
    X = X.reshape([-1,1])
    Y = Y.reshape([-1,1])
    Theta = Theta.reshape([1,-1])

    # generate R for each (pixel,theta)
    R = X*np.cos(Theta) + Y*np.sin(Theta) + max_r #offset max_r to make all values between (0, 2*max_r + 1)
    R = np.round(R)
    R = R.astype('int') # round and set to int to discretize for indexing
    
    ### VOTING STILL REQURIES FOR LOOP

    ## METHOD 1: loop over Theta
    a = (2*max_r+1).astype('int')
    for i in range(Theta.size):
        Hough[:,i] = np.histogram(R[:,i], bins=a, range=(0,a))[0]

    ## METHOD 2: loop over edge pixels
    # t = np.arange(Theta.size)   # indexes for theta
    # for i in range(X.size):        
    #     Hough[R[i,t],t] = Hough[R[i,t],t] + 1
        
    return Hough, Theta.flatten(), max_r
########################## Support code below

from os.path import normpath as fn # Fixes window/linux path conventions
import warnings
warnings.filterwarnings('ignore')

# which image to use
# n = 2
for n in range(1,13):
    # n = 'test'
    # downsizes = [1, 2, 4, 8, 16, 32, 64, 128]    
    # for i in range(len(downsizes)):
    img_raw = np.float32(imread(fn('inputs/'+str(n)+'.jpg')))/255.
    # # img = np.mean(img_raw, axis=2) #takes mean across the color channels to get grayscale
    start_time = time.time()
    
    img = img_raw[:,:,1] #get only green color channel (for green line)
    
    downsize = 64
    # downsize = downsizes[i]
    img = img[::downsize,::downsize]

    # imsave(fn('outputs/'+str(n)+'_green.jpg'),img)
    
    H, theta = grads(img)
    
    # imsave(fn('outputs/'+str(n)+'_grad.jpg'),H/np.max(H[:]))
    
    T0 = 0.5
    E = np.float32(H > T0)
    # E2 = nms(E,H,theta)
    

    # img_b = np.float32(img < 0.5)
    # imsave(fn('outputs/'+str(n)+'_large.jpg'),img_b)
    # imsave(fn('outputs/'+str(n)+'_edge_downsize'+str(downsize)+'.jpg'),E)
    # imsave(fn('outputs/'+str(n)+'_nms.jpg'),E2)
    
    Eh, Theta, max_r = hough(E,50)
    # Eh, Theta, max_r = hough(img_b,50)

    # Eh = Eh**(3/4) # scaling to make smaller values more visible 
    # imsave(fn('outputs/'+str(n)+'_hough.jpg'),Eh/np.max(Eh))
    
    num_lines = 2
    thetas = np.zeros(num_lines)
    rs = np.zeros(num_lines)
    slopes = np.zeros(num_lines)
    intercepts = np.zeros(num_lines)
    for j in range(num_lines):
        best_r,best_theta = np.unravel_index(np.argmax(Eh, axis=None), Eh.shape)
        
        size = 1
        Eh[best_r-size:best_r+size+1,best_theta-size:best_theta+size+1] = 0        
        thetas[j] = Theta[best_theta]
        rs[j] = best_r-max_r
        
        slopes[j] = -1/np.tan(thetas[j])
        intercepts[j] = rs[j]/np.sin(thetas[j])
        
    #     X = np.arange(img_raw.shape[1])
    #     Y = np.maximum(0,np.minimum(slopes[j]*X + intercepts[j]*downsize, img_raw.shape[0]-1)).astype('int')
    #     for i in range(-3,4):    
    #         img_raw[np.minimum(Y+i,img_raw.shape[0]-1),np.minimum(X+i,img_raw.shape[1]-1),:] = [1,0,0]
 
    theta = np.mean(thetas)
    r = np.mean(rs)
    slope = -1/np.tan(theta)
    intercept = r/np.sin(theta)

    print('theta =', theta, 'r =', r, '--- m =', slope, 'b =', intercept)
    print("--- %s seconds ---" % (time.time() - start_time))
    # X = np.arange(img_raw.shape[1])
    # Y = np.maximum(0,np.minimum(slope*X + intercept*downsize, img_raw.shape[0]-1)).astype('int')
    # for i in range(-3,4):    
    #     img_raw[np.minimum(Y+i,img_raw.shape[0]-1),np.minimum(X+i,img_raw.shape[1]-1),:] = [0,0,1]
    
    # imsave(fn('outputs/'+str(n)+'_line.jpg'),img_raw)
    # imsave(fn('outputs/'+str(n)+'_hough.jpg'),Eh/np.max(Eh))
    
    