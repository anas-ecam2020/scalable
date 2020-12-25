from numpy import linspace, reshape
from multiprocessing import Pool
import time
import numpy as np
from PIL import Image as im 


xmin, xmax = -2.0 ,0.5    # x range
ymin, ymax = -1.25,1.25   # y range
nx  , ny   =  1000,1000   # resolution
maxiter    =  50          # max iterations

def mandelbrot(z): # computation for one pixel
  c = z
  for n in range(maxiter):
    if abs(z)>2: return n   # divergence test
    z = z*z + c
  return maxiter

X = linspace(xmin,xmax,nx) # lists of x and y
Y = linspace(ymin,ymax,ny) # pixel co-ordinates



# main loops
if __name__ == '__main__':
    p = Pool()
    Z = [complex(x,y) for y in Y for x in X]
    N = p.map(mandelbrot,Z)
    

    p.close()
    p.join()
    N = reshape(N, (nx,ny)) # change to rectangular array
    data = im.fromarray((N*255).astype(np.uint16))
    data.save('mandelbrot.png') 
    finish = time.perf_counter()
    print(f'Finished running after seconds:', finish)