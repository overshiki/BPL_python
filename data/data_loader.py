'''
THIS MODULE LOAD ALL THE NECCESSARY DATA FOR TRAINING

for mat data, it is a dict data which contains the following keys:
	timing
	names
	images
	drawings
	offsets
each of the keys contains a list
in each list, is numpy arrays
'''

import scipy.io

keys = ['timing', 'names', 'images', 'drawings', 'offsets']

def load_mat(file):
	mat = scipy.io.loadmat(file)
	return mat

mat_dict = load_mat("./data_background.mat")

for key in keys:
	print(len(mat_dict[key]))


names = []
for i in range(len(mat_dict['names'])):
	names.append(str(mat_dict['names'][i].tolist()[0][0]))

print(names)


draw_dir = mat_dict['drawings'][0][0]
draw_character = draw_dir[0][0]
draw_img = draw_character[0][0]
print(draw_img.shape)
draw_stroke = draw_img[0][0]
print(draw_stroke.shape)