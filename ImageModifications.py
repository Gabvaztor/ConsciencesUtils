import os
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps

def create_nested_directory_from_path_v1(path):
    """
    Create a nested directory from path with the same name as base directory + _removed_pixels. If the file exists,
    it does nothing.
    Args:
        path: Path to the directory where the new directory has to be created.

    Returns: new_folder_name, the path to the new folder.
    """
    img_path = Path(path)
    new_folder_name = path + os.sep + img_path.name + '_removed_pixels' + os.sep
    Path(new_folder_name).mkdir(exist_ok=True)
    return new_folder_name

def get_image_array(fullpath, resize_dimensions=None, keep_aspect_ratio=False):
    """
    Get image from fullpath.
    (Optional) Resize the image to the given resize dimensions.
    Convert it to numpy array.

    Args:
        fullpath: fullpath of image
        resize_dimensions: resize_dimensions is a tuple with the format: (height, width). Ths will be the new dimension
        of the images.
        If none, then the image will be the same.
        keep_aspect_ratio: True if we want to keep aspect ratio of new images.


    Returns: Image.img , array image

    """

    img = Image.open(fullpath) # Imgur's naming scheme

    if resize_dimensions:
        w = list(resize_dimensions)[0]
        h = list(resize_dimensions)[1]
        size = (w, h)
        if keep_aspect_ratio:
            width, high = img.size
            aspect_ratio = int((width / high) * h)
            if w == aspect_ratio:
                # If the aspect ratio of the original image is the same as the resize dimensions
                image_array = np.array(img.resize(size), Image.BICUBIC) # Resize image
            else:
                # To keep it the same, if the aspect ratio of the original image is different of the resize dimensions
                image_array = np.array(img.resize((aspect_ratio, h), Image.BICUBIC))  # Resize image
        else:
            img = ImageOps.fit(img, size, Image.ANTIALIAS)
            image_array = np.array(img) # Convert to array
    else:
        image_array = np.array(img) # Convert to array

    return  img, image_array

def get_pixel_not_black_from_array(row_or_column_array):
    """
    Iterate over a row or column array until a non black pixel is found.

    Args:
        row_or_column_array: row or column we want to iterate over until we found a not black pixel

    Returns: index_to_return, the column or row where the non black pixel is found

    """
    index_to_return = None
    for index, pixel in enumerate(row_or_column_array):
        if pixel[0] != 0 and pixel[1] != 0 and pixel[2] != 0:  # If not black
            index_to_return = index
            break
    return index_to_return

def crop_image_from_image_array_by_black_pixels(image_array, image):
    """
    With the data collected with get_pixel_not_black_from_array() function, the image black border is cropped.
    The non black pixels found iterating over from the middle row and column of the image to the center, we get the
    area to be cropped.

    Args:
        image_array: Numpy array image

        image: Original image

    Returns: Image cropped array

    """
    h, w, _ = image_array.shape

    # the middle row and column
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

    # The rectangle of the image to be cropped, based on non black pixels found with get_pixel_not_black_from_array()
    area = (left_column_to_crop, top_row_to_crop, w - right_column_to_crop, h - bottom_row_to_crop)
    image =  Image.fromarray(np.uint8(image_array))
    cropped_img = image.crop(area)
    return cropped_img

def remove_black_pixels_of_image_path_v2(path, resize_dimensions=None, keep_aspect_ratio=False):
    """
    From the path to the image folder, create a new nested folder with the same name as the image
    folder + '_removed_pixels'.
    Iterate over the image folder to process only the image files and do nothing if a non image file is found.
    Convert the images to numpy arrays and found the black border area to be cropped.
    Save the cropped images to the new folder created, without modifying the original images.

    Args:
        path: images path
        resize_dimensions: is a tuple with the format: (height, width). Ths will be the new dimension of the images.
        If none, then the image will be the same.
        keep_aspect_ratio: True if we want to keep aspect ratio of new images.
    """
    print("Creating folder...")
    # Step 1: Creating the new nested folder
    new_folder_name = create_nested_directory_from_path_v1(path=path)
    print("Folder created!")
    print("Executing...")
    # Step 2: Iterating over all the files in the image folder and processing it
    for count_number, file in enumerate(os.listdir(path)):
        new_fullpath = new_folder_name + file # Fullpath of each file in directory
        # Processing only those with the given suffixes
        if file.endswith((".jpeg", ".jpg", ".png")):
            image_cropped = None
            # Converting the image to numpy array and resizing if arguments given, keeping the original aspect ratio
            img, image_array = get_image_array(fullpath=path + os.sep + file, resize_dimensions=resize_dimensions)
            # Cropping the image, catching exeptions if the image cropping fail
            try:
                image_cropped = crop_image_from_image_array_by_black_pixels(image=img, image_array=image_array)
            except Exception as e:
                print(str(e))
            # Step 3: Save the cropped images
            if image_cropped:
                image_cropped.save(new_fullpath, "JPEG")
            else:
                img.save(new_folder_name + file, "JPEG")
        else:
            continue
    print("Finish!")