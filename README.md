[![Build Status](https://travis-ci.org/iamantony/images2grey.svg?branch=master)](https://travis-ci.org/iamantony/images2grey)   [![Coverage Status](https://coveralls.io/repos/iamantony/images2grey/badge.png)](https://coveralls.io/r/iamantony/images2grey)

images2grey
===========

Multi-thread python app for transformation of color images to grayscale images.

Tags
=======================
python, image, processing, greyscale, grayscale, grey, multithread

Usage
=======================

    $python images2grey.py PATH_TO_FOLDER -s RESULTS_FOLDER

* PATH_TO_FOLDER - absolute path to the folder with images that you want to transform
* -RESULTS_FOLDER - (optional) absolute path where greyscale images should be saved . If not set, original images will become greyscale.

Examples
=======================

Transform images in folder /home/my_user_name/images_folder to greyscale images:

    $ python images2grey.py /home/my_user_name/images_folder
    
Create greyscale copies of images in folder C:\\images and save them to C:\\some\\other\\folder:

    $ python images2grey.py C:\\images -s C:\\some\\other\\folder
    
Show help:

    $ python images2grey.py -h

Requirements
=======================

Python >= 2.6

Pillow (PIL) library

    $pip install Pillow
