#Compute dx/dt partial derivatives
#for each column (variable) of X
#
#Input
# X: [T x dim]
# t: [T x 1] time points
#
#Output
# dxdt: [T-1 x 1] derivatives

def get_deriv(X,t):
	T, dim = X.shape
	dxdt = numpy.zeros((T,dim))
	for i in range(1,T):
		_prev = X[i-1,:]
		_next = X[i,:]
		dt = t[i]-t[i-1]
		dxdt[i,:] = (_next-_prev)*1./dt

	return dxdt


def find(sel, keyword='first'):
	if(keyword=='first'):
		for i in range(sel.shape[0]):
			if sel[i,0]==True:
				index = i 
				return index 
	elif(keyword=='last'):
		for i in range(sel.shape[0],0,-1):
			if sel[i,0]==True:
				index = i 
				return index
	elif(keyword=='all'):
		re_list = []
		for i in range(sel.shape[0]):
			if sel[i,0]==True:
				 re_list.append(i)
		return re_list


 # Partition a stroke in to sub-strokes based on pauses of the pen.

 # Input
 #  unif_stk: [n x 2] stroke, assuming uniform time sampling
 #  dthresh: [scalar] if this much distance (norm) is not covered
 #         at each time point, then it's a pause
 #  max_sequence: [scalar] maximum length of a stop sequence, before it is
 #         called it's own stroke

 # Output
 #  substrokes: [ns x 1] cell array of sub-strokes
 #  unif_stk: stroke with pause sequences shortened to a single point
 #  breaks: where the pauses occured


def partition_strokes(unif_stk, dthresh, max_sequence):
	n = unif_stk.shape[0]
	dxdt = get_deriv(unif_stk, numpy.array([x for x in range(n)]))

	if n==1:
		substrokes = unif_stk
		breaks = True
		return substrokes, unif_stk, breaks

	norm_dxdt = numpy.zeros((n,1))
	for i in range(n):
		norm_dxdt[i] = numpy.linalg.norm(dxdt[i,:])


	#compute the candidate stop points
	stop_pt = norm_dxdt < dthresh
	for i in range(1,n):
		if(stop_pt[i]):
			stop_pt[i-1] = True

	stop_pt[0], stop_pt[-1] = True, True

	# Partition the stop points into stop sequences.
	# Here, non-stops are denoted as zeros, the first stop
	# is a sequence of 1s, second is a sequence of twos, etc.
	# Until the pen is moving fast enough again
	stop_sequence = numpy.zeros((n,1))
	stop_count = 1
	for i in range(n):
		if stop_pt[i]: #current point is a stop, it's the same stop
			stop_sequence[i] = stop_count
		elif (stop_pt[i-1] && stop_pt[i+1]): #points surround it are a stop... its the same stop
			stop_sequence[i] = stop_count
		elif stop_pt[i-1]:
			stop_count = stop_count+1

	# special case where the entire stroke is a stop sequence
	if stop_count==1:
		stop_sequence = numpy.zeros((n,1))
		stop_sequence[0] = 1
		stop_sequence[-1] = 2
		stop_count = 2

	# Make sure the stop sequences aren't too long. If they are,
	# we place a sub-stroke break at the beginning and end.
	i = 1
	while i<=stop_count:
		sel = stop_sequence==i
		nsel = sel.shape[0]
		if nsel>max_sequence:
			#get the index of first and last True value in sel, and set the corresponding position to be False
			index_first = find(sel, keyword='first')
			index_last = find(sel, keyword='last')

			sel[index_first, 0] = False
			sel[index_last, 0] = False 


			stop_sequence[sel] = 0
			stop_sequence[stop_sequence>i] = stop_sequence[stop_sequence>i]+1
			stop_sequence[index_last,0] = i+1
			stop_count = stop_count+1

		i = i+1


	#breaks are the average of the stop sequences
	mybreaks = numpy.zeros((n,1))
	for i in range(stop_count):
		sel = stop_sequence==i #select the stop sequence

		if i==1 #begining of the stroke
			mybreaks[i] = find(sel, keyword='first')
		elif i==stop_count:  #end of stroke
			mybreaks[i] = find(sel, keyword='last')
		else: #all other positions
			mybreaks[i] = math.floor(numpy.mean(find(sel, keyword='all')))

		#set the mean element to the mean of the sequence
		unif_stk[mybreaks[i],:] = numpy.mean(unif_stk[sel], axis=0)

		#mark to keep
		stop_sequence[mybreaks[i]] = -1


	#remove all other stop sequence elements, except for the marked mean
	numpy.delete(unif_stk[stop_sequence>0])
	numpy.delete(stop_sequence>0)
	breaks = stop_sequence<0

	#convert to cell array
	fbreaks = find(breaks, keyword='all')
	nb = len(fbreaks)
	ns = max(1, nb-1)
	substrokes = numpy.zeros((ns, 1))
	if nb==1:  #if this stroke was just a single stop sequence
		substrokes[1] = unif_stk
	else:
		for s in range(ns):
			substrokes[s] = unif_stk[fbreaks[s]:fbreaks[s+1],:]

	new_start = substrokes[1][1,:]
	new_end = substrokes[-1][-1,:]

	return substrokes, unif_stk, breaks
