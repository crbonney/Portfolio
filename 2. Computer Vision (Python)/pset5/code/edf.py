### EDF --- An Autograd Engine for instruction
## (based on joint discussions with David McAllester)

import numpy as np

# Global list of different kinds of components
ops = []
params = []
values = []


# Global forward
def Forward():
    for c in ops: c.forward()

# Global backward    
def Backward(loss):
    for c in ops:
        c.grad = np.zeros_like(c.top)
    for c in params:
        c.grad = np.zeros_like(c.top)

    loss.grad = np.ones_like(loss.top)
    for c in ops[::-1]: c.backward() 

# SGD
def SGD(lr):
    for p in params:
        p.top = p.top - lr*p.grad


# ## Fill this out        
def init_momentum():
    for p in params:
        p.hist = 0 # dont need to specify size because it will broadcast to p.grad
    

## Fill this out
def momentum(lr,mom=0.9):
    for p in params:
        p.hist = p.grad + mom*p.hist
        p.top = p.top - lr*p.hist


###################### Different kinds of nodes

# Values (Inputs)
class Value:
    def __init__(self):
        values.append(self)

    def set(self,value):
        self.top = np.float32(value).copy()

# Parameters (Weights we want to learn)
class Param:
    def __init__(self):
        params.append(self)

    def set(self,value):
        self.top = np.float32(value).copy()


### Operations

# Add layer (x + y) where y is same shape as x or is 1-D
class add:
    def __init__(self,x,y):
        ops.append(self)
        self.x = x
        self.y = y

    def forward(self):
        self.top = self.x.top + self.y.top
        # print('add', self.top.shape)

    def backward(self):
        if self.x in ops or self.x in params:
            self.x.grad = self.x.grad + self.grad

        if self.y in ops or self.y in params:
            if len(self.y.top.shape) < len(self.grad.shape):
                ygrad = np.sum(self.grad,axis=tuple(range(len(self.grad.shape)-1)))
            else:
                ygrad= self.grad
            self.y.grad = self.y.grad + ygrad

# Matrix multiply (fully-connected layer)
class matmul:
    def __init__(self,x,y):
        ops.append(self)
        self.x = x
        self.y = y

    def forward(self):
        # print('matmul', self.x.top.shape,self.y.top.shape)
        self.top = np.matmul(self.x.top,self.y.top)

    def backward(self):
        if self.x in ops or self.x in params:
            self.x.grad = self.x.grad + np.matmul(self.y.top,self.grad.T).T
        if self.y in ops or self.y in params:
            self.y.grad = self.y.grad + np.matmul(self.x.top.T,self.grad)


# Rectified Linear Unit Activation            
class RELU:
    def __init__(self,x):
        ops.append(self)
        self.x = x

    def forward(self):
        self.top = np.maximum(self.x.top,0)

    def backward(self):
        if self.x in ops or self.x in params:
            self.x.grad = self.x.grad + self.grad * (self.top > 0)


# Reduce to mean
class mean:
    def __init__(self,x):
        ops.append(self)
        self.x = x

    def forward(self):
        self.top = np.mean(self.x.top)

    def backward(self):
        if self.x in ops or self.x in params:
            self.x.grad = self.x.grad + self.grad*np.ones_like(self.x.top) / np.float32(np.prod(self.x.top.shape))



# Soft-max + Loss (per-row / training example)
class smaxloss:
    def __init__(self,pred,gt):
        ops.append(self)
        self.x = pred
        self.y = gt

    def forward(self):
        y = self.x.top
        y = y - np.amax(y,axis=1,keepdims=True)
        yE = np.exp(y)
        yS = np.sum(yE,axis=1,keepdims=True)
        y = y - np.log(yS); yE = yE / yS

        truey = np.int64(self.y.top)
        self.top = -y[range(len(truey)),truey]
        self.save = yE

    def backward(self):
        if self.x in ops or self.x in params:
            truey = np.int64(self.y.top)
            self.save[range(len(truey)),truey] = self.save[range(len(truey)),truey] - 1.
            self.x.grad = self.x.grad + np.expand_dims(self.grad,-1)*self.save
        # No backprop to labels!    

# Compute accuracy (for display, not differentiable)        
class accuracy:
    def __init__(self,pred,gt):
        ops.append(self)
        self.x = pred
        self.y = gt

    def forward(self):
        truey = np.int64(self.y.top)
        self.top = np.float32(np.argmax(self.x.top,axis=1)==truey)

    def backward(self):
        pass


# Downsample by 2    
class down2:
    def __init__(self,x):
        ops.append(self)
        self.x = x
        
    def forward(self):
        self.top = self.x.top[:,::2,::2,:]
        # print('down2', self.top.shape)

    def backward(self):
        if self.x in ops or self.x in params:
            grd = np.zeros_like(self.x.top)
            grd[:,::2,::2,:] = self.grad
            self.x.grad = self.x.grad + grd


# Flatten (conv to fc)
class flatten:
    def __init__(self,x):
        ops.append(self)
        self.x = x
        
    def forward(self):
        # print('flatten', self.x.top.shape)
        self.top = np.reshape(self.x.top,[self.x.top.shape[0],-1])

    def backward(self):
        if self.x in ops or self.x in params:
            self.x.grad = self.x.grad + np.reshape(self.grad,self.x.top.shape)
            
# Convolution Layer
## Fill this out
class conv2:

    def __init__(self,x,k):
        ops.append(self)
        self.x = x # x = shape(batch, x, y, channels)
        self.k = k


    def forward(self):
        # code here

        Hk, Wk, C1, C2 = self.k.top.shape
        N, H, W, C = self.x.top.shape
        self.top = np.zeros([N, H-Hk+1, W-Wk+1, C2])
        N, Hy, Wy, Cy = self.top.shape

        for y in range(H-Hk+1):
            for x in range(W-Wk+1):
                for yk in range(Hk):
                    for xk in range(Wk):
                        self.top[:,y,x,:] = self.top[:,y,x,:] + np.matmul(self.x.top[:,y+yk,x+xk,:],self.k.top[yk,xk,:,:])

    def backward(self):

        N, H, W, C = self.x.top.shape
        Hk, Wk, C1, C2 = self.k.top.shape
        N, Hy, Wy, Cy = self.grad.shape


        if self.x in ops or self.x in params:
            # code here
            self.x.grad = np.zeros(self.x.top.shape)
            
            for i in range(Hy):
                for j in range(Wy):
                    for cy in range(Cy):                        
                        self.x.grad[:, i:i+Hk, j:j+Wk, :] = self.x.grad[:, i:i+Hk, j:j+Wk, :] + (np.resize(self.grad[:,i,j,cy],(N,Hk,Wk,C)) * self.k.top[:,:,:,cy])
                    
        if self.k in ops or self.k in params:
            # code here
            self.k.grad = np.zeros(self.k.top.shape)

            for yy in range(Hy):
                for xy in range(Wy):
                    for cy in range(Cy):
                        self.k.grad[:,:,:,cy] = self.k.grad[:,:,:,cy] + np.sum(self.x.top[:,yy:yy+Hk,xy:xy+Wk,:],axis=0)*np.sum(self.grad[:,yy,xy,cy])
                        
