
import os
from pathlib import Path
import numpy
from PIL import Image
from skimage.exposure import histogram
from imageio import imread
import numpy as np
import imageio
from skimage.filters import sobel
from skimage.morphology import watershed

DEBUG = False

def create_nested_directory_from_path_v1(path):
    """
    Create a nested directory from fullpath with the same name as base directory + _removed_pixels. If the file exists,
    it does nothing.
    Args:
        fullpath: Full path to the directory where the new directory has to be created.

    """
    path_ = Path(path)
    new_folder_name = path + os.sep + path_.name + '_removed_pixels' + os.sep
    Path(new_folder_name).mkdir(exist_ok=True)
    return new_folder_name

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()

def get_pixel_not_black_from_array(row_or_column_array):
    index_to_return = None
    for index, pixel in enumerate(row_or_column_array):
        #print("current pixel: ", pixel)
        if pixel[0] != 0 and pixel[1] != 0 and pixel[2] != 0:  # If not black
            index_to_return = index
            break
    return index_to_return

def get_image_array(fullpath):
    """

    Args:
        fullpath:

    Returns: Image.img , array image

    """
    img = Image.open(fullpath) # Imgur's naming scheme
    image_array = numpy.array(img)        # Convert to array
    return  img, image_array

def crop_image_from_image_array_by_black_pixels(image_array, image):
    """

    Args:
        image_array:

    Returns: Image cropped array

    """
    h, w, _ = image_array.shape

    half_of_rows_resolution = int(h / 2)
    half_of_column_resolution = int(w / 2)

    # Recogemos la columna que hay que cortar por la izquierda
    left_column_to_crop = get_pixel_not_black_from_array(row_or_column_array=
                                                         image_array[half_of_rows_resolution])
    # Recogemos la columna que hay que cortar por la derecha
    right_column_to_crop = get_pixel_not_black_from_array(row_or_column_array=
                                                          reversed(image_array[half_of_rows_resolution]))
    # Recogemos la columna que hay que cortar por la izquierda
    top_row_to_crop = get_pixel_not_black_from_array(row_or_column_array=
                                                     image_array[:,half_of_column_resolution])
    # Recogemos la columna que hay que cortar por la izquierda
    bottom_row_to_crop = get_pixel_not_black_from_array(row_or_column_array=
                                                        reversed(image_array[:,half_of_column_resolution]))


    area = (left_column_to_crop, top_row_to_crop, w - right_column_to_crop, h - bottom_row_to_crop)
    cropped_img = image.crop(area)
    #cropped_img.show()
    return cropped_img

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

def remove_black_pixels_from_path_v2(path):
    """

    Args:
        path:

    """
    # Step 1
    new_folder_name = create_nested_directory_from_path_v1(path=path)
    # Step 2
    for count_number, file in enumerate(os.listdir(path)):
        filename = os.fsdecode(file)
        if count_number == 3:
            break
        if filename.endswith((".jpeg", ".jpg", ".png")):
            # print(os.path.join(fullpath, filename))
            img, image_array = get_image_array(fullpath=path + os.sep + filename)
            img_cropped = crop_image_from_image_array_by_black_pixels(image=img, image_array=image_array)
            # Step 3: Save
            img_cropped.save(new_folder_name + filename)
        else:
            continue

remove_black_pixels_from_path_v1("C:", DEBUG=DEBUG, x=2)