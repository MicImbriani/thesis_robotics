import numpy as np
def equilateral(x, y):
                
    v_x = (x[0]+y[0]+np.sqrt(3)*(x[1]-y[1]))/2 # This computes the `x coordinate` of the third vertex.
    v_y = (x[1]+y[1]+np.sqrt(3)*(x[0]-y[0]))/2 #This computes the 'y coordinate' of the third vertex. 
    z = np.array([v_x, v_y]) #This is point z, the third vertex. 
    return z

print(equilateral((50,100), (50,150)))