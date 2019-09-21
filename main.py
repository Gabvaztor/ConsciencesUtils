"""
Core project
"""
from skimage.exposure import histogram
from imageio import imread
import numpy as np
import imageio

img = imread(uri="index_photo.jpg", as_gray=True) #Open image on greyscale.
hist, hist_centers = histogram(img) #Calculating the histogram of the grey values.

markers = np.zeros_like(img) #Determine markers of the object and the background.
markers[img <= 35] = 1
markers[img > 35] = 2

#The watershed transform floods an image of elevation starting from markers, in order to determine the catchment basins
#of these markers. Watershed lines separate these catchment basins, and correspond to the desired segmentation.
from skimage.filters import sobel #The choice of the elevation map is critical for good segmentation. Here, the
elevation_map = sobel(img)        #amplitude of the gradient provides a good elevation map.
from skimage.morphology import watershed
segmentation = watershed(elevation_map, markers) #We use the Sobel operator for computing the amplitude of the gradient.

#Convert the array to binary to use it as an alpha channel.
segmentation_r = segmentation.reshape(segmentation.shape[0]*segmentation.shape[1])
for i in range(segmentation_r.shape[0]):
    if segmentation_r[i] > 1:
        segmentation_r[i] = 255
    else:
        segmentation_r[i] = 0

alpha = segmentation_r.reshape(832, 1100)
img_rgb = imread("index_photo.jpg")
img_rgb_np = np.asarray(img_rgb)

#Adding the alpha channel to the image, where 0 is a transparent pixel.
no_background = np.dstack((img_rgb_np, alpha)).astype("uint8")
imageio.imwrite('index_photo4_removed_pixels.png', no_background)