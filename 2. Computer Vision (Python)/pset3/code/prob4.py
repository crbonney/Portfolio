## Default modules imported. Import more if you need to.

import numpy as np


## Fill out these functions yourself

# Fits a homography between pairs of pts
#   pts: Nx4 array of (x,y,x',y') pairs of N >= 4 points
# Return homography that maps from (x,y) to (x',y')
#
# Can use np.linalg.svd
def getH(pts):

    # unpack points
    x = pts[:,0]
    y = pts[:,1]
    x_p = pts[:,2]
    y_p = pts[:,3]

    # add 'z' of ones for homogeneous points
    z = np.ones(x.shape)
    z_p = np.ones(x_p.shape)
    
    
    A = np.zeros([0, 9])

    # build A matrix by stacking A_i matrices from each point
    for i in range(x.size):       

        #cross product matrix from p'
        cross_i = cross_i = [[0, -z_p[i], y_p[i]],[z_p[i], 0, -x_p[i]],[-y_p[i], x_p[i], 0]]        

        #sparce matrix with points from p
        zero = np.zeros([1,3])
        p_i = [[x[i],y[i],z[i]]]
        # [p, 0, 0]
        a1 = np.concatenate([p_i,zero,zero])
        # [0, p, 0]
        a2 = np.roll(a1,1,axis=0)
        # [0, 0, p]
        a3 = np.roll(a1,2,axis=0)

        #stack them together
        mult_i = np.concatenate([a1,a2,a3],axis=1)

        #multiply together
        A_i = np.matmul(cross_i,mult_i)[0:2,:] # only need two rows of A matrix


        #stack A_i onto A        
        A = np.concatenate([A,A_i])

    u,s,v = np.linalg.svd(A,full_matrices=True)
    
    # last singular vector
    h = v[-1]
    
    H = h.reshape([3,3])
    return H
    

# Splices the source image into a quadrilateral in the dest image,
# where dpts in a 4x2 image with each row giving the [x,y] co-ordinates
# of the corner points of the quadrilater (in order, top left, top right,
# bottom left, and bottom right).
#
# Note that both src and dest are color images.
#
# Return a spliced color image.
def splice(src,dest,dpts):

    src_shape = src.shape
    src_pts = [[0,0],[0,src_shape[1]-1],[src_shape[0]-1,0],[src_shape[0]-1,src_shape[1]-1]]
    
    pts = np.concatenate([dpts,src_pts],axis=1)
    
    H = getH(pts)
    # print(H)

    # get max and min x,y points from quad
    min_dpts_x,min_dpts_y = np.min(dpts,axis=0)
    max_dpts_x,max_dpts_y = np.max(dpts,axis=0)

    # build a meshgrid of every homogeneous point that could be in the quad
    x = np.arange(min_dpts_x,max_dpts_x)
    y = np.arange(min_dpts_y,max_dpts_y)
    xv,yv = np.meshgrid(x,y)
    zv = np.ones(xv.shape)
    
    xvf=xv.reshape([1,-1]).astype('int32')
    yvf=yv.reshape([1,-1]).astype('int32')
    zvf=zv.reshape([1,-1]).astype('int32')
    
    # flattened representation of the homogeneous meshgrid
    ptsf = np.concatenate([xvf,yvf,zvf])
    
    # apply transform to every point
    pts_src = np.matmul(H,ptsf)
    # make sure homogeneous term is 1, then ignore it
    pts_src = pts_src[0:2,:]/pts_src[2,:]

    pts_src = np.round(pts_src).astype('int32')

    # find all points from meshgrid that are still in the source image
    valid = np.where((pts_src[0,:] >= 0) & (pts_src[0,:] < src_shape[0]) & (pts_src[1,:] >= 0) & (pts_src[1,:] < src_shape[1]))[0]

    # pick only those points
    pts_src = pts_src[:,valid]
    
    # replace all valid points in destination with points corresponding points from source image
    # does not take into account multiple points being mapped to same location
    dest[yvf[0,valid],xvf[0,valid],:] = src[pts_src[0,:],pts_src[1,:],:]

    return dest
    
    
########################## Support code below

from skimage.io import imread, imsave
from os.path import normpath as fn # Fixes window/linux path conventions
import warnings
warnings.filterwarnings('ignore')


simg = np.float32(imread(fn('inputs/p4src.png')))/255.
dimg = np.float32(imread(fn('inputs/p4dest.png')))/255.
dpts = np.float32([ [276,54],[406,79],[280,182],[408,196]]).astype('int32') # Hard coded
# dpts = np.float32([ [276,54],[406,79],[280,182],[408,196]]) # Hard coded

comb = splice(simg,dimg,dpts)

imsave(fn('outputs/prob4.png'),comb)
