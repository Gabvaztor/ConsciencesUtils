import os
from pathlib import Path
from skimage.exposure import histogram
from imageio import imread
import numpy as np
import imageio
from skimage.filters import sobel
from skimage.morphology import watershed

DEBUG = False

def create_nested_directory_from_fullpathv1(fullpath):
    """
    Create a nested directory from fullpath with the same name as base directory + _removed_pixels. If the file exists,
    it does nothing.
    Args:
        fullpath: Full path to the directory where the new directory has to be created.

    """
    path = Path(fullpath)
    Path(fullpath + os.sep + path.name + '_removed_pixels').mkdir(exist_ok=True)

def remove_black_pixels_from_path_v1(path, **kwargs):
    """
    Create a new folder in the same path with the same name as the current folder and the string "_removed_pixels"
    added in the right.

    Loop each image in the folder and remove all possible black pixels outside the "real" image.

    Save each image in the new folder created.

    NOTE: Do not delete or modify original images.
    Args:
        path:

    Returns:

    """

    debug = kwargs["DEBUG"] if ("DEBUG" in kwargs) else 0

    create_nested_directory_from_fullpathv1(path)


    img = imread(uri=path, as_gray=True) #Open image on greyscale.
    #hist, hist_centers = histogram(img) #Calculating the histogram of the grey values to determine markers.

    markers = np.zeros_like(img) #Determine markers of the object and the background.
    markers[img <= 35] = 1
    markers[img > 35] = 2

    #The watershed transform floods an image of elevation starting from markers, in order to determine the catchment
    #basins of these markers. Watershed lines separate these catchment basins, and correspond to the desired
    #segmentation.
    #The choice of the elevation map is critical for good segmentation. Here, the
    elevation_map = sobel(img)        #amplitude of the gradient provides a good elevation map.
    segmentation = watershed(elevation_map, markers) #We use the Sobel operator for computing the amplitude of the
                                                     #gradient.
    ay, ax = segmentation.shape
    #Convert the array to binary to use it as an alpha channel.
    segmentation_r = segmentation.reshape(segmentation.shape[0]*segmentation.shape[1])
    for i in range(segmentation_r.shape[0]):
        if segmentation_r[i] > 1:
            segmentation_r[i] = 255
        else:
            segmentation_r[i] = 0

    alpha = segmentation_r.reshape(ay, ax)
    img_rgb = imread(path)
    img_rgb_np = np.asarray(img_rgb)

    #Adding the alpha channel to the image, where 0 is a transparent pixel.
    no_background = np.dstack((img_rgb_np, alpha)).astype("uint8")
    imageio.imwrite('index_photo4_removed_pixels.png', no_background)

remove_black_pixels_from_path_v1("C:", DEBUG=DEBUG, x=2)