import pathlib
from platform import python_version
import os
import errno
import shutil
import ntpath

def path_split(path):
    """
    Split the path into a pair of head and tail and return tail.

    Args:
        path: path or filepath

    Returns: Return tail.

    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def create_path_for_filepath(path, filepath):
    """
    From a path, create all necessaries folders and copy a file from filepath to the path destination.
    Return True if the process was executed successfully or False otherwise.

    Args:
        path: A path to be created.
        filepath: A filepath that will be copied to the "path" destination.

    Returns: True if the process is successful and False otherwise.

    """
    if float(python_version()[:2]) < 3.:
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as error:
                if error.errno != errno.EEXIST:
                    raise
    else:
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    shutil.copy2(filepath, path)

    file = pathlib.Path(path + os.sep + path_split(filepath))
    try:
        file.resolve(strict=True)
    except FileNotFoundError:
        return False
    else:
        return True



