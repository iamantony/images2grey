__author__ = 'Antony Cherepanov'

import argparse
import os
import multiprocessing
from PIL import Image


def main():
    folder, save_folder = parse_arguments()
    is_ok = check_arguments(folder, save_folder)
    if is_ok is True:
        start(folder, save_folder)
    else:
        print("Invalid arguments. Try again!")


def parse_arguments():
    """ Parse arguments and start transformation
    :return [tuple] of arguments
    """

    parser = argparse.ArgumentParser(
        description="Multi-thread python app for transformation of color "
                    "images to grayscale images.")

    parser.add_argument("folder",
                        help="absolute path to the folder with images to "
                             "transform")

    parser.add_argument("-s", "--save_to",
                        help="path to the folder where greyscale images "
                             "should be saved",
                        default="")

    args = parser.parse_args()
    return args.folder, args.save_to


def check_arguments(t_folder, t_save_folder):
    """ Check arguments
    :param t_folder: [string] - absolute path to the folder with images to
    transform
    :param t_save_folder: [string] - absolute path to folder for greyscale
     images
    :return [bool] True if arguments are OK.
    """

    if check_existing_folder(t_folder) is False:
        print("Error: Invalid path to folder with images - " + t_folder)
        return False

    if 0 < len(t_save_folder):
        if check_folder_path(t_save_folder) is True:
            if not os.path.exists(t_save_folder):
                os.makedirs(t_save_folder)
        else:
            print("Error: Invalid path to folder for greyscale images - " +
                  t_save_folder)
            return False

    return True


def check_existing_folder(t_path):
    """ Check if folder really exist
    :param t_path: [string] - absolute path to presumably existing folder
    :return: [bool] True if folder exist, False if it's not
    """

    if not os.path.isabs(t_path) or\
            not os.path.exists(t_path) or\
            not os.path.isdir(t_path):
        return False
    return True


def check_folder_path(t_path):
    """ Check if path to folder is valid
    :param t_path: [string] - absolute path to some folder
    :return: [bool] True if path could be path for folder.
    """

    if os.path.isabs(t_path) is True:
        return True
    return False


def start(t_folder, t_save_folder):
    """ Start transformation process
    :param t_folder: [string] - absolute path to the folder with images to
    transform
    :param t_save_folder: [string] - absolute path to folder for greyscale
     images
    """

    images = get_images_paths(t_folder)
    cores_num = multiprocessing.cpu_count()
    img_chunks = list_split(images, cores_num)

    jobs = list()
    for i in range(cores_num):
        thread = multiprocessing.Process(target=greyscale,
                                         args=(next(img_chunks), t_save_folder))
        jobs.append(thread)
        thread.start()

    for thread in jobs:
        thread.join()


def get_images_paths(t_folder):
    """ Check if folder contains images (on the first level) and return
     their paths
    :param t_folder: [string] - absolute path to the folder
    :return: [list] with the absolute paths of the images in folder
    """

    if not os.path.isdir(t_folder):
        return list()

    image_extensions = ("jpg", "jpeg", "bmp", "png", "gif", "tiff")
    images = list()
    entries = os.listdir(t_folder)
    for entry in entries:
        file_path = os.path.join(t_folder, entry)
        extension = get_extension(file_path)
        if os.path.isfile(file_path) and extension in image_extensions:
            images.append(file_path)

    return images


def get_extension(t_path):
    """ Get extension of the file
    :param t_path: [string] - path or name of the file
    :return: [string] with extension of the file or empty string if we failed
     to get it
    """

    path_parts = str.split(t_path, '.')
    extension = path_parts[-1:][0]
    extension = extension.lower()
    return extension


def list_split(t_list, t_size):
    """ Generator that split list of elements into n chunks
    :param t_list: [list] - list of elements
    :param t_size: [int] - size of chunk
    :return generator of lists of chunks
    """

    new_length = int(len(t_list) / t_size)
    for i in range(0, t_size - 1):
        start = i * new_length
        yield t_list[start: start + new_length]
    yield t_list[t_size * new_length - new_length:]


def greyscale(t_images, t_save_folder):
    """ Transform color images to greyscale images
    :param t_images: [list] -  list of paths to the images
    :param t_save_folder: [string] - absolute path to folder for greyscale
     images
    :return [list] of paths to created greyscale images
    """

    grey_images = list()
    for img_path in t_images:
        print("Transforming " + img_path)

        img = Image.open(img_path)
        grey_img = img.convert("L")

        path, name, extension = parse_image_path(img_path)
        if 0 < len(t_save_folder):
            path = t_save_folder

        filename = "{path}{sep}{name}.{ext}".format(path=path, name=name,
                                                sep=str(os.sep), ext=extension)
        grey_img.save(filename)
        grey_images.append(filename)
        img.close()

    return grey_images


def parse_image_path(t_img_path):
    """ Parse path to image and return it's parts: path, image name, extension
    :param t_img_path: [string] - path to image
    :return: [tuple] of strings that hold path to image file, image name and
     image extension
    """

    img_path_parts = str.split(t_img_path, os.sep)
    path_parts, image_name = img_path_parts[:-1], img_path_parts[-1]
    path = os.sep.join(path_parts)

    img_name_parts = str.split(image_name, '.')
    image_name_parts, extension = img_name_parts[:-1], img_name_parts[-1]
    name = ".".join(image_name_parts)

    return path, name, extension


if __name__ == '__main__':
    main()