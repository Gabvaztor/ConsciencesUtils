"""
This file is used to run ImageModification.remove_black_pixels_of_image_path_v2 using a parameter as argparse

Use this file in this way in command line:

python "fullpath_of_this_file" -i "path_of_image_path"
"""

import sys, os, argparse

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append('../../')

from ImageModifications import remove_black_pixels_of_image_path_v2

if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--path_images", required=False,
                    help="Path of images")

    args = vars(ap.parse_args())
    path_ = args["path_images"]

    height, width = 720, 1280
    resize_dimensions = (width, height)

    remove_black_pixels_of_image_path_v2(path=path_, resize_dimensions=resize_dimensions, keep_aspect_ratio=False)