## Default modules imported. Import more if you need to.
### Problem designed by Abby Stylianou

import numpy as np
from scipy.signal import convolve2d as conv2

def get_cluster_centers(im,num_clusters):
    # Implement a method that returns an initial grid of cluster centers. You should first
    # create a grid of evenly spaced centers (hint: np.meshgrid), and then use the method
    # discussed in class to make sure no centers are initialized on a sharp boundary.
    # You can use the get_gradients method from the support code below.
    cluster_centers = np.zeros((num_clusters,2),dtype='int')
    
    K = np.sqrt(num_clusters)
    h,w,c = im.shape
    
    # distance between cluster centers
    S = np.sqrt(h*w/num_clusters)

    # neighbor_size = 1 gives 3x3 neighborhood (+/- 1 from point)
    neighbor_size = 1
    neighbors = np.arange(-neighbor_size,neighbor_size+1)

    # get gradient of image to test for edges at cluster centers
    grad = get_gradients(im)

    for n in range(num_clusters):
        
        # evenly distributed center points
        x = ((n % K)+1/2)*S//1
        y = ((n// K)+1/2)*S//1
        # turn into int for indexing
        x = x.astype('int')
        y = y.astype('int')

        # define a neighborhood around point (3x3 for this problem)
        xc = (x+neighbors).astype('int')
        yc = (y+neighbors).astype('int')
        xc,yc = np.meshgrid(xc,yc)    
        
        # find argmin of gradient in neighborhood and set it to be the cluster center
        miny,minx = np.unravel_index(np.argmin(grad[yc,xc], axis=None), xc.shape)
        cluster_centers[n,:] = [y+1-miny,x+1-minx]
        
    return cluster_centers

def slic(im,num_clusters,cluster_centers):
    # Implement the slic function such that all pixels assigned to a label
    # should be close to each other in squared distance of augmented vectors.
    # You can weight the color and spatial components of the augmented vectors
    # differently. To do this, experiment with different values of spatial_weight.
    h,w,c = im.shape
    K = num_clusters    
    clusters = np.zeros([h,w])

    x = np.arange(w); y = np.arange(h)    
    X,Y = np.meshgrid(x,y)
    

    S = w//np.sqrt(K)
    # larger spatial wieght required for more clusters, linear scaling worked best
    spatial_weight = 0.5*np.sqrt(K)

    ## FOR CHECKING EVERY mu_k FOR EVERY PIXEL
    # initially start clusters as squares around their center
    # sqrtK = (np.sqrt(K)).astype('int')
    # clusters = X*sqrtK//w + sqrtK*(Y*sqrtK//h)

    # im_aug[n] = [R,G,B,xn,yn]
    im_aug = np.zeros([5,h*w])
    im_aug[0:3,:] = im.reshape([-1,3]).T
    im_aug[3,:] = X.reshape(-1)*spatial_weight
    im_aug[4,:] = Y.reshape(-1)*spatial_weight

    # print(im_aug[:,250:250+10])    

    clusters = clusters.reshape(-1)
        
    
    ## LOOK AT 2Sx2S GRID FOR EACH u_k        

    # Define neighborhood size
    neighbor_size = S
    neighbors = np.arange(-neighbor_size,neighbor_size+1)

    ## min_dist[n] initializes to infty
    min_dist = np.ones(clusters.shape)*10**7
    
    ## 0th iteration, seed each cluster based on cluster center
    muK = np.zeros([5,K])
    Lk = np.zeros([K,w*h])
    for k in range(K):
        xc = cluster_centers[k,1]
        yc = cluster_centers[k,0]
        muK[:,k] = im_aug[:, xc+yc*w]
        Lk[k,:] = np.sum((im_aug-muK[:,k:k+1])**2,axis=0)
    clusters = np.argmin(Lk,axis = 0)

    num_its = 1000
    for t in range(num_its):
        for k in range(k):
            # define mean vector for cluster k 
            Ik = im_aug[:,clusters == k] # all points currently in cluster k
            muK[:,k] = np.mean(Ik,axis = 1) # 5x1 mean vector

            ## Define Neighborhood of size 2Sx2S
            xc = muK[3,k]/spatial_weight
            yc = muK[4,k]/spatial_weight            
            # xc = cluster_centers[k,1]
            # yc = cluster_centers[k,0]
            Xc = (xc + neighbors).astype('int')
            Yc = (yc + neighbors).astype('int')
            # remove pixels outside of image and make a meshgrid of points
            Xc = np.delete(Xc, np.where((Xc >= w) | (Xc < 0)))
            Yc = np.delete(Yc, np.where((Yc >= w) | (Yc < 0)))
            Xc,Yc = np.meshgrid(Xc,Yc)
            Xc = Xc.flatten()
            Yc = Yc.flatten()

            # Calculate the aug distance from the mean for each pixel in neighborhood
            min_distK = np.sum((im_aug[:,Xc + Yc*w] - muK[:,k:k+1])**2,axis=0)

            # find pixels that have a lower aug distance and update them
            a = np.where(min_distK < min_dist[Xc + Yc*w])[0]

            # a is a vector of points to update based on Xc, Yc
            min_dist[Xc[a] + Yc[a]*w] = min_distK[a]
            clusters[Xc[a] + Yc[a]*w] = k

    ## LOOK AT ALL PIXELS, LOOPS THROUGH K, CHECKING EVERY N IN PARALLEL
    # num_its = 100
    # for t in range(num_its):
        
    #     muK = np.zeros([5,K])
    #     Lk = np.zeros([K,w*h])
    #     for k in range(K):
    #         Ik = im_aug[:,clusters == k]
    #         mu = np.mean(Ik,axis = 1)
    #         muK[:,k] = mu
    #         Lk[k,:] = np.sum((im_aug-muK[:,k:k+1])**2,axis=0)
    #     clusters = np.argmin(Lk,axis = 0)


    clusters = clusters.reshape(h,w)
    return clusters

########################## Support code below

from skimage.io import imread, imsave
from os.path import normpath as fn # Fixes window/linux path conventions
import matplotlib.cm as cm
import warnings
warnings.filterwarnings('ignore')

# Use get_gradients (code from pset1) to get the gradient of your image when initializing your cluster centers.
def get_gradients(im):
    if len(im.shape) > 2:
        im = np.mean(im,axis=2)
    df = np.float32([[1,0,-1]])
    sf = np.float32([[1,2,1]])
    gx = conv2(im,sf.T,'same','symm')
    gx = conv2(gx,df,'same','symm')
    gy = conv2(im,sf,'same','symm')
    gy = conv2(gy,df.T,'same','symm')
    return np.sqrt(gx*gx+gy*gy)

# normalize_im normalizes our output to be between 0 and 1
def normalize_im(im):
    im += np.abs(np.min(im))
    im /= np.max(im)
    return im

# create an output image of our cluster centers
def create_centers_im(im,centers):
    for center in centers:
        im[center[0]-2:center[0]+2,center[1]-2:center[1]+2] = [255.,0.,255.]
    return im

im = np.float32(imread(fn('inputs/lion.jpg')))

num_clusters = [25,49,64,81,100]
# num_clusters = [25]
for num_clusters in num_clusters:
    cluster_centers = get_cluster_centers(im,num_clusters)
    imsave(fn('outputs/prob1a_' + str(num_clusters)+'_centers.jpg'),normalize_im(create_centers_im(im.copy(),cluster_centers)))
    out_im = slic(im,num_clusters,cluster_centers)

    Lr = np.random.permutation(num_clusters)
    out_im = Lr[np.int32(out_im)]
    dimg = cm.jet(np.minimum(1,np.float32(out_im.flatten())/float(num_clusters)))[:,0:3]
    dimg = dimg.reshape([out_im.shape[0],out_im.shape[1],3])
    imsave(fn('outputs/prob1b_'+str(num_clusters)+'.jpg'),normalize_im(dimg))
