 # Convert a stroke [x,y,t] such that it is uniformly sampled
 # in time. This is done by linear interpolation in time

 # Input
 #  stk:  [n x 2] for x and y
 #  time: [n x 1] for time coordinate
 #  tint: [scalar] time interval (in milliseconds)

 # Output
 #  unif_stk: [k x 2] new stroke x and y 
 #  unif_t: [k x 1] uniform time interval

 #this is basically 'translated' from original matlab version of code
import numpy


def uniform_time_lerp(stk,time,tint):
    mint = min(time)
    maxt = max(time)
	unif_t = [x for x in range(mint, maxt, tint)]

    #make sure we don't leave out the last point
    if unif_t[-1] < maxt 
       unif_t.append(maxt)

    nt = len(unif_t)
	unif_stk = numpy.zeros((nt, 2))

    for i in range(nt):
        ti = unif_t[i];
        
        diff = time-ti;

        if((diff==0).sum()>0):
        	sel = numpy.select([diff==0], [stk])
        	unif_stk[i,:] = sel.mean(axis=1)
        	continue

		# find the point before and after in time
		check = diff>0
		indx_gt = 0
		for j in range(check.shape[0]):
			if(check[j]==True):
				indx_gt = j
				break

		check = diff<0
		indx_lt = 0
		for j in range(check.shape[0], 0, -1):
			if(check[j]==True):
				indx_lt = j
				break

        x_gt = stk[indx_gt,:];
        x_lt = stk[indx_lt,:];
        t_gt = time[indx_gt];
		t_lt = time[indx_lt]; 

        # Compute the linear interpolation
        frac = (ti - t_lt)*1./(t_gt - t_lt)
        if(frac<=1):
			unif_stk[i,:] = (1-frac)*1.*x_lt + frac*1.*x_gt
		else:
			print("error")