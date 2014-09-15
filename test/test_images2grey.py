__author__ = 'Antony Cherepanov'

import unittest
import os
import shutil
import images2grey
from PIL import Image


SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))
TEST_SAVE_FOLDER = SCRIPT_FOLDER + str(os.sep) + "test_folder"
BACKUP_FOLDER = SCRIPT_FOLDER + str(os.sep) + "backup"

TEST_IMG_1 = "test1.png"
TEST_IMG_2 = "test2.bmp"
TEST_GREY_IMG = "test_grey.jpg"

TEST_IMG_PATH_1 = SCRIPT_FOLDER + str(os.sep) + TEST_IMG_1
TEST_IMG_PATH_2 = SCRIPT_FOLDER + str(os.sep) + TEST_IMG_2
TEST_GREY_IMG_PATH = SCRIPT_FOLDER + str(os.sep) + TEST_GREY_IMG


class CheckArgumentsTest(unittest.TestCase):
    def test_valid_folder(self):
        self.assertTrue(images2grey.check_arguments(SCRIPT_FOLDER, ""))

    def test_invalid_folder(self):
        self.assertFalse(
            images2grey.check_arguments("/invalid/folder", ""))

    def test_invalid_save_folder(self):
        self.assertFalse(images2grey.check_arguments(SCRIPT_FOLDER, "../fake/"))

    def test_save_folder_creation(self):
        self.assertTrue(images2grey.check_arguments(SCRIPT_FOLDER,
                                                    TEST_SAVE_FOLDER))

    def tearDown(self):
        if os.path.exists(TEST_SAVE_FOLDER):
            try:
                shutil.rmtree(TEST_SAVE_FOLDER, True)
            except Exception as err:
                print("Error during folder remove: {0}".format(err))
                return


class GetImagesPathsTest(unittest.TestCase):
    def test_invalid_folder(self):
        self.assertEqual(images2grey.get_images_paths("../fake/"), list())

    def test_valid_folder(self):
        paths = [TEST_IMG_PATH_1, TEST_IMG_PATH_2, TEST_GREY_IMG_PATH]
        self.assertEqual(images2grey.get_images_paths(SCRIPT_FOLDER), paths)


class GetExtensionTest(unittest.TestCase):
    def test_get_extension(self):
        self.assertEqual(images2grey.get_extension(TEST_IMG_PATH_1), "png")
        self.assertEqual(images2grey.get_extension(TEST_IMG_PATH_2), "bmp")
        self.assertEqual(images2grey.get_extension(TEST_GREY_IMG_PATH), "jpg")

    def test_get_extension_several_dots(self):
        test_img_path = SCRIPT_FOLDER + str(os.sep) + "test.hey.jpeg"
        self.assertEqual(images2grey.get_extension(test_img_path), "jpeg")


class ParsePathTest(unittest.TestCase):
    def test_get_parts(self):
        self.assertEqual(images2grey.parse_image_path(TEST_IMG_PATH_1),
                         (SCRIPT_FOLDER, "test1", "png"))

        test_img_path = SCRIPT_FOLDER + str(os.sep) + "test.hey.png"
        self.assertEqual(images2grey.parse_image_path(test_img_path),
                         (SCRIPT_FOLDER, "test.hey", "png"))


class ListSplitTest(unittest.TestCase):
    def test_simple_list(self):
        simple = [1, 2, 3]
        result = images2grey.list_split(simple, len(simple))
        for i in range(len(simple)):
            self.assertEqual(next(result), simple[i:i+1])

    def test_big_list(self):
        big_list = [1, 2, 3, 4, 5]
        result = images2grey.list_split(big_list, 3)
        self.assertEqual(next(result), big_list[0:1])
        self.assertEqual(next(result), big_list[1:2])
        self.assertEqual(next(result), big_list[2:])
        self.assertRaises(StopIteration, lambda: next(result))


class ImageGreyscaleTest(unittest.TestCase):
    def setUp(self):
        if not os.path.exists(BACKUP_FOLDER):
            os.makedirs(BACKUP_FOLDER)

        shutil.copy(TEST_IMG_PATH_1, BACKUP_FOLDER)
        shutil.copy(TEST_IMG_PATH_2, BACKUP_FOLDER)
        shutil.copy(TEST_GREY_IMG_PATH, BACKUP_FOLDER)

    def test_greyscale(self):
        paths = [TEST_IMG_PATH_1, TEST_IMG_PATH_2, TEST_GREY_IMG_PATH]
        result_paths = images2grey.greyscale(paths, "")
        self.assertEqual(result_paths, paths)
        for path in result_paths:
            self.assertTrue(self.check_greyscale(path))

    def test_greyscale_with_path(self):
        paths = [TEST_IMG_PATH_1, TEST_IMG_PATH_2, TEST_GREY_IMG_PATH]
        os.makedirs(TEST_SAVE_FOLDER)
        result_paths = images2grey.greyscale(paths, TEST_SAVE_FOLDER)
        self.assertEqual(len(result_paths), len(paths))
        for path in result_paths:
            self.assertTrue(self.check_greyscale(path))

    def check_greyscale(self, t_path):
        img = Image.open(t_path)
        img.load()
        width, height = img.size
        for wdt in range(width):
            for hgt in range(height):
                # If pixel if grey, getpixel() will return one int value.
                # If it's color pixel, we will get tuple of integers.
                pixel = img.getpixel((wdt, hgt))
                if not isinstance(pixel, int):
                    img.close()
                    return False

        img.close()
        return True

    def tearDown(self):
        shutil.copy(BACKUP_FOLDER + str(os.sep) + TEST_IMG_1, SCRIPT_FOLDER)
        shutil.copy(BACKUP_FOLDER + str(os.sep) + TEST_IMG_2, SCRIPT_FOLDER)
        shutil.copy(BACKUP_FOLDER + str(os.sep) + TEST_GREY_IMG, SCRIPT_FOLDER)

        if os.path.exists(BACKUP_FOLDER):
            shutil.rmtree(BACKUP_FOLDER, True)

        if os.path.exists(TEST_SAVE_FOLDER):
            shutil.rmtree(TEST_SAVE_FOLDER, True)


class StartTest(unittest.TestCase):
    def setUp(self):
        if not os.path.exists(BACKUP_FOLDER):
            os.makedirs(BACKUP_FOLDER)

        shutil.copy(TEST_IMG_PATH_1, BACKUP_FOLDER)
        shutil.copy(TEST_IMG_PATH_2, BACKUP_FOLDER)
        shutil.copy(TEST_GREY_IMG_PATH, BACKUP_FOLDER)

    def test_start_slicing(self):
        os.makedirs(TEST_SAVE_FOLDER)
        images2grey.start(SCRIPT_FOLDER, TEST_SAVE_FOLDER)

        images = images2grey.get_images_paths(TEST_SAVE_FOLDER)
        self.assertEqual(len(images), 3)
        for path in images:
            self.assertTrue(self.check_greyscale(path))

    def check_greyscale(self, t_path):
        img = Image.open(t_path)
        img.load()
        width, height = img.size
        for wdt in range(width):
            for hgt in range(height):
                # If pixel if grey, getpixel() will return one int value.
                # If it's color pixel, we will get tuple of integers.
                pixel = img.getpixel((wdt, hgt))
                if not isinstance(pixel, int):
                    img.close()
                    return False

        img.close()
        return True

    def tearDown(self):
        shutil.copy(BACKUP_FOLDER + str(os.sep) + TEST_IMG_1, SCRIPT_FOLDER)
        shutil.copy(BACKUP_FOLDER + str(os.sep) + TEST_IMG_2, SCRIPT_FOLDER)
        shutil.copy(BACKUP_FOLDER + str(os.sep) + TEST_GREY_IMG, SCRIPT_FOLDER)

        if os.path.exists(BACKUP_FOLDER):
            shutil.rmtree(BACKUP_FOLDER, True)

        if os.path.exists(TEST_SAVE_FOLDER):
            shutil.rmtree(TEST_SAVE_FOLDER, True)


if __name__ == "__main__":
    unittest.main()
