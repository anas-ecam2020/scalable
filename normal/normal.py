from PIL import Image as im 
from numpy      import linspace, reshape
import numpy as np
import time



xmin, xmax = -2.0 ,0.5   # x range
ymin, ymax = -1.25,1.25  # y range
nx  , ny   =  1000,1000  # resolution
maxiter    =  50         # max iterations




# pour déterminer si un complexe  appartient à l'ensemble de mandelbrot est donc simple: 
# calculer la suite jusqu"à ce que:
# soit le module de  soit supérieur à 2,
# soit on atteigne un  maximum définit à l'avance
def mandelbrot(z): # computation for one pixel
  c = z
  for n in range(maxiter):
    #Dans le premier cas,  n'appartient pas à l'ensemble
    if abs(z)>2: return n  # divergence test
    #Dans le second, on considère que  appartient à l'ensemble
    z = z*z + c
  return maxiter

start = time.perf_counter()

X = linspace(xmin,xmax,nx) # lists of x and y
Y = linspace(ymin,ymax,ny) # pixel co-ordinates


# main loops
N = []
for y in Y:
  for x in X:
    z  = complex(x,y)
    N += [mandelbrot(z)]


N = reshape(N, (nx,ny)) # change to rectangular
data = im.fromarray((N*255).astype(np.uint16))
data.save('mandelbrot.png') 

finish = time.perf_counter()
perf = finish - start
print(f'Finished running after seconds:', perf)
