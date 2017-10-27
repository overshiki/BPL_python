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

I rearranged this into a new data container: character
'''

import scipy.io

keys = ['timing', 'names', 'images', 'drawings', 'offsets']

def load_mat(file):
	mat = scipy.io.loadmat(file)
	return mat

mat_dict = load_mat("./data_background.mat")

# for key in keys:
# 	print(len(mat_dict[key]))


names = []
for i in range(len(mat_dict['names'])):
	names.append(str(mat_dict['names'][i].tolist()[0][0]))

# print(names)


# draw_dir = mat_dict['drawings'][0][0]
# draw_character = draw_dir[0][0]
# draw_img = draw_character[0][0]
# print(draw_img.shape)
# draw_stroke = draw_img[0][0]
# print(draw_stroke.shape)


character = {}
for index, (name, drawings_dir, images_dir, timing_dir) in enumerate(zip(names, mat_dict['drawings'], mat_dict['images'], mat_dict['timing'])):

	drawings_dir, images_dir, timing_dir = drawings_dir[0], images_dir[0], timing_dir[0]

	_dir = []
	for drawings_subdir, images_subdir, timing_subdir in zip(drawings_dir, images_dir, timing_dir):
		drawings_subdir, images_subdir, timing_subdir = drawings_subdir[0], images_subdir[0], timing_subdir[0]
		_subdir = []
		for drawings_img, images_img, timing_img in zip(drawings_subdir, images_subdir, timing_subdir):
			idrawings_img, images_img, timing_img = drawings_img[0], images_img[0], timing_img[0]

			_img = {}
			_img['data'] = images_img
			_img['time'] = []
			_img['strokes'] = []
			for drawings_stroke, timing_stroke in zip(drawings_img, timing_img):
				_img['strokes'].append(drawings_stroke[0])
				_img['time'].append(timing_stroke[0])
			_subdir.append(_img)
		_dir.append(_subdir)

	character[name] = _dir

				
# print(character['Greek'])