 # Convert a stroke [x,y] such that it is uniformly sampled in space.

 # Input
 #   stk : [n x 2] stroke
 #   dint : target distance between poitns

 # Output
 #   yi : [m x 2] interpolated stroke

 #this is basically 'translated' from original matlab version of code
import numpy, math

def uniform_space_lerp(stk,dint)

    # return if stroke is too short
    n = stk.shape[0]
    if n==1:
       stk_yi = stk
       return stk_yi
    
    # compute distance between each point
    dist = numpy.zeros((n,1))

    tormv = numpy.empty(shape=(n,1))
    tormv[0] = True
    for i in range(1,n):       
        x1 = stk[i,:]
        x2 = stk[i-1,:]
        dist[i] = numpy.linalg.norm(x1-x2)
        tormv[i] = dist[i] > 1e-4
    
    # remove points that are too close
    dist = dist[tormv]
    stk = stk[tormv]
    
    # return if stroke is too short
    n = stk.shape[0]
    if n==1:
       stk_yi = stk
       return stk_yi
    
    # cumulative distance
    cumdist = numpy.cumsum(dist)
    start_dist = cumdist[1]
    end_dist = cumdist[-1]
    x = cumdist[:]
   

    nint = numpy.around(end_dist*1./dint)
    nint = math.max(nint,2);   
    xi = [x for x in range(start_dist,end_dist,nint)]
    stk_yi = numpy.interp(x,stk,xi)

