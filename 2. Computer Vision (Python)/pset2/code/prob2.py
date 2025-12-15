## Default modules imported. Import more if you need to.

import numpy as np
from skimage.io import imread, imsave


## Fill out these functions yourself

## Take color image, and return 'white balanced' color image
## based on gray world, as described in Problem 2(a). For each
## channel, find the average intensity across all pixels.
##
## Now multiply each channel by multipliers that are inversely
## proportional to these averages, but add upto 3.
def balance2a(img):
    
    # prevents from changing input image
    img=img.copy()
    
    # calculate the mean of each color channel individually
    r = img[:,:,0].reshape(-1)
    g = img[:,:,1].reshape(-1)
    b = img[:,:,2].reshape(-1)
    
    mu_r = np.mean(r)
    mu_g = np.mean(g)
    mu_b = np.mean(b)
    
    # calculate normalizing constant, c to make the sum of alpha_i = 3
    # alpha_i = c/mu_i
    c = 3/(1/mu_r+1/mu_g+1/mu_b)

    # confirm the sum of alpha_i = 3
    # print(c*(1/mu_r+1/mu_g+1/mu_b))

    # update img color channels by multiplying them individually by their alpha value
    img[:,:,0] = img[:,:,0]*c/mu_r
    img[:,:,1] = img[:,:,1]*c/mu_g
    img[:,:,2] = img[:,:,2]*c/mu_b

    return img


## Take color image, and return 'white balanced' color image
## based on description in Problem 2(b). In each channel, find
## top 10% of the brightest intensities, take their average.
##
## Now multiply each channel by multipliers that are inversely
## proportional to these averages, but add upto 3.
def balance2b(img):

    # prevents from changing input image
    img=img.copy()

    # grab individualy color channels (copies so they don't sort the original)
    r = img[:,:,0].reshape(-1).copy()
    g = img[:,:,1].reshape(-1).copy()
    b = img[:,:,2].reshape(-1).copy()

    # sorts channels in descending order
    r[::-1].sort()
    g[::-1].sort()
    b[::-1].sort()

    
    # get the index for the 90th precentile intensity
    # dont worry about rounding from integer division, 10% is arbitrary
    ten_percent_index = r.size//10
    
    # only consider the 10% highest intensity pixels in r,g,b channels
    r = r[:ten_percent_index]
    g = g[:ten_percent_index]
    b = b[:ten_percent_index]

    mu_r = np.mean(r)
    mu_g = np.mean(g)
    mu_b = np.mean(b)
    
    # calculate normalizing constant, c to make the sum of alpha_i = 3
    # alpha_i = c/mu_i
    c = 3/(1/mu_r+1/mu_g+1/mu_b)

    # confirm the sum of alpha_i = 3
    # print(c*(1/mu_r+1/mu_g+1/mu_b))

    # update img color channels by multiplying them individually by their alpha value
    img[:,:,0] = img[:,:,0]*c/mu_r
    img[:,:,1] = img[:,:,1]*c/mu_g
    img[:,:,2] = img[:,:,2]*c/mu_b

    return img



########################## Support code below

from os.path import normpath as fn # Fixes window/linux path conventions
import warnings
warnings.filterwarnings('ignore')


# Utility functions to clip intensities b/w 0 and 1
# Otherwise imsave complains
def clip(im):
    return np.maximum(0.,np.minimum(1.,im))



############# Main Program
im1 = np.float32(imread(fn('inputs/CC/ex1.jpg')))/255.
im2 = np.float32(imread(fn('inputs/CC/ex2.jpg')))/255.
im3 = np.float32(imread(fn('inputs/CC/ex3.jpg')))/255.

im1a = balance2a(im1)
im2a = balance2a(im2)
im3a = balance2a(im3)

imsave(fn('outputs/prob2a_1.png'),clip(im1a))
imsave(fn('outputs/prob2a_2.png'),clip(im2a))
imsave(fn('outputs/prob2a_3.png'),clip(im3a))

im1b = balance2b(im1)
im2b = balance2b(im2)
im3b = balance2b(im3)

imsave(fn('outputs/prob2b_1.png'),clip(im1b))
imsave(fn('outputs/prob2b_2.png'),clip(im2b))
imsave(fn('outputs/prob2b_3.png'),clip(im3b))


