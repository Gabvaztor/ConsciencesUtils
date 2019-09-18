"""
Core project
"""
from PIL import Image
import numpy as np
import imageio
from skimage.feature import canny
from scipy import ndimage as ndi

img = Image.open("index_photo.png")
np_img = np.asarray(img)
r = np_img[:,:,0] #split array into rgb channels
g = np_img[:,:,1]
b = np_img[:,:,2]

edges_r = canny(r/255.) #edge detection, only support 2D arrays
edges_g = canny(g/255.) #that's the reason why we split channels
edges_b = canny(b/255.)
rgb = np.dstack((edges_r,edges_g,edges_b)) #join channels agaim
fill_np_img = ndi.binary_fill_holes(rgb).astype("int") # fill the edges we found before
#maybe it's necesary to use the function in smaller portions of the array to work

imageio.imwrite('index_photo_removed_pixels.png', fill_np_img) #guardando el array en una imagen
