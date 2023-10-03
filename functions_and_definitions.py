# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 21:27:51 2023

@author: iolab
"""
import easygui as easygui
from PIL import Image
import os, os.path
# import sys


# =============================================================================
# The following function as its name suggests, it shows a text and an image
# provided by the program using the python module, easygui
# =============================================================================
def show_image_and_message(image, user_message):
    msg = user_message
    choices = ["Continue", "Cancel"]
    if image == None or image == '':
        reply = easygui.buttonbox(msg, choices=choices)
    else:
        reply = easygui.buttonbox(msg, image=image, choices=choices)
    return reply

# =============================================================================
# This function get a name of a file with its extension
# and returns a complete path. 
# The path is built from the current directory and a folder where all 
# the pictures reside
# As final result, we have a absolute path containing the entire link
# =============================================================================
def locating_image_and_returning_its_path(picture_name):
    if picture_name == None or picture_name == '':
        return None
    else:
        current_working_directory = os.getcwd()
        picture_folder = "cal_pics"
        picture_to_evaluate = os.path.join(current_working_directory, picture_folder, picture_name)
        return picture_to_evaluate
    

# =============================================================================
# The following function resize a pictute by a hard-coded
# given percentage size
# it does return a picture object
# the user can just call this function on a picture and the result
# can be just "shown" using the .show() built-in function.
# =============================================================================
def resizing_original_picture_by_percentage(picture_to_evaluate):
    current_working_directory = os.getcwd()
    picture_folder = "cal_pics"
    picture_to_evaluate = os.path.join(current_working_directory, picture_folder, picture_to_evaluate)
    image = Image.open(picture_to_evaluate)
    width, height = image.size
    percentage_size = 0.11
    new_size = (int(width*percentage_size), int(height * percentage_size))
    new_picture = image.resize(new_size)
    return new_picture