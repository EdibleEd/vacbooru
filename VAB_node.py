import Image as im_
import numpy as np_
import scipy.signal as ss_
import scipy.misc as sm_
import matplotlib.pyplot as mp_
from scipy import ndimage
import math as m



# numpy array from image file
# lena = misc.imread('lena.png') 
# large files
# lena_memmap = np.memmap('lena.raw', dtype=np.int64, shape=(512, 512))

# .mean() .max() 

# scipy quick and easy sobel
# sx = ndimage.sobel(im, axis=0, mode='constant')
# sy = ndimage.sobel(im, axis=1, mode='constant')
# sob = np.hypot(sx, sy)

# l = sm_.lena()
# sm_.imsave('lena.png', l)

l = sm_.imread('123.thumbnail', flatten=True)

n = 10
im = l
#im[(l[0]).astype(np_.int), (l[1]).astype(np_.int)] = 1
im = ndimage.gaussian_filter(im, sigma=(0.5,0.5))
mask = im > im.mean()

sm_.imsave('mask.png', mask)

label_im, nb_labels = ndimage.label(mask)

print(nb_labels)

# range(nb_labels + 1)
sizes = ndimage.sum(mask, label_im, range(1, nb_labels + 1))
mean_vals = ndimage.sum(im, label_im, range(1, nb_labels + 1))
print(sizes * mean_vals)
print(mean_vals)
labels = np_.unique(label_im)
label_im = np_.searchsorted(labels, label_im)

sm_.imsave('mask_2.png', label_im)











# im = im_.open('123.jpg').convert('L')
# width, height = (700, 826)
# imarray = np_.array(im)

# laplacian = [[0, -1, 0], [-1, 4, -1], [0, -1, 0]]

# edges = ss_.convolve2d(imarray, laplacian)




# outputImage = sm_.toimage(output)
# outputImage.save('A.jpg')