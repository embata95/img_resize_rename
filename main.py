from PIL import Image
import os
from os.path import isfile
import imghdr
import re


def replace_non_alpha(bad_name):
    new_name = re.sub(r"[^a-zA-Z0-9]", "_", bad_name)
    return new_name


def get_clear_name(file_name):
    temp_name = replace_non_alpha(''.join(file_name.split('.')[:-1]))
    return temp_name


def is_format_valid(ext):
    if ext == '':
        return True
    if not ext.startswith('.'):
        ext = '.' + ext
    return ext.lower() in Image.EXTENSION


def get_format(file_name):
    if desired_format == '':
        curr_format = f".{file_name.split('.')[-1]}"
    else:
        curr_format = desired_format
    return curr_format


Image.init()
new_file_path, folder_command, file_command = None, None, None
images_path = input('Enter the relative path to the images folder. \nFor current path enter . \n')
while not os.path.exists(images_path):
    print('Please enter a valid location on your OS!')
    images_path = input('Enter the relative path to the images folder: ')
new_folder_name = input('Enter the name of the folder for the updated images: ')
while os.path.exists(os.path.join(images_path, new_folder_name)) and folder_command != '1':
    folder_command = input(f"{os.path.join(images_path, new_folder_name)} already exists! Enter 1 to continue or 2 to enter a new name: \n")
    if folder_command == '2':
        new_folder_name = input('Enter the name of the folder for the updated images: ')
desired_format = input('Enter the desired extension of the file. For example .jpg: \nLeave blank if you want to keep the otiginal format: ')
while not is_format_valid(desired_format):
    print(f"{desired_format} is not a valid extension!")
    desired_format = input('Enter the desired extension of the file. For example .jpg: \nLeave blank if you want to keep the otiginal format: ')
max_width = input('Enter the max width of the image in pixels: ')
while not max_width.isdigit():
    print(f"Width should be a whole number \n{max_width} is not a number")
    max_width = input('Enter the max width of the image in pixels: ')
max_height = input('Enter the max height of the image in pixels: ')
while not max_height.isdigit():
    print(f"Height should be a whole number \n{max_height} is not a number")
    max_height = int(input('Enter the max height of the image in pixels: '))
print_name = input('If you want the new image names to be printed enter 1, otherwise enter 0: ') == '1'
if desired_format != '' and not desired_format.startswith('.'):
    desired_format = '.' + desired_format
os.chdir(images_path)
for curr_file in os.listdir():
    if isfile(curr_file) and imghdr.what(curr_file) in ['jpeg', 'png']:
        img_name = get_clear_name(curr_file)
        image = Image.open(curr_file)
        if get_format(curr_file).lower() != '.png':
            image = image.convert('RGB')
        image.thumbnail((int(max_width), int(max_height)))
        if not os.path.exists(new_folder_name):
            os.mkdir(new_folder_name)
        final_name = img_name + get_format(curr_file)
        new_file_path = os.path.join(new_folder_name, final_name)
        while os.path.exists(new_file_path) and file_command != '1':
            file_command = input(f"{final_name} already exists! Enter 1 to continue or 2 to enter a new name: ")
            if file_command == '2':
                img_name = input(f"Enter new name for file {final_name}: ")
                img_name = replace_non_alpha(img_name)
                final_name = img_name + get_format(curr_file)
                new_file_path = os.path.join(new_folder_name, final_name)
        image.save(new_file_path)
        file_command = None
        if print_name:
            print(final_name)

if new_file_path:
    print(f"Your images can be found in {new_folder_name}")
else:
    print(f"No image files found in {images_path}")