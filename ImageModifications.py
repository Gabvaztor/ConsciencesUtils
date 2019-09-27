import os
from pathlib import Path
import numpy
from PIL import Image

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
    return cropped_img

def remove_black_pixels_of_image_path_v2(path):
    """

    Args:
        path:

    """
    print("Creating folder...")
    # Step 1
    new_folder_name = create_nested_directory_from_path_v1(path=path)
    print("Folder created!")
    # Step 2
    print("Executing...")
    for count_number, file in enumerate(os.listdir(path)):
        filename = os.fsdecode(file)
        if filename.endswith((".jpeg", ".jpg", ".png")):
            img, image_array = get_image_array(fullpath=path + os.sep + filename)
            img_cropped = crop_image_from_image_array_by_black_pixels(image=img, image_array=image_array)
            # Step 3: Save
            img_cropped.save(new_folder_name + filename)
        else:
            continue
    print("Finish!")