
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


