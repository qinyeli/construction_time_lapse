#!/usr/local/bin/python3

"""Converts all HEIC files in HEIC_PATH to JPEG and store in JPEG_PATH.

Expects JPEG_PATH already exits.
"""

import datetime
import os
import PIL
import pyheif
import pytz
import subprocess
import whatimage

HEIC_PATH = 'heic_img'
JPEG_PATH = 'jpeg_img'

def get_photo_date_taken(heic_filepath: str):
    """Gets the date on which photo was taken through a shell.
    """
    cmd = 'mdls %s' % os.path.join(HEIC_PATH, heic_filepath)
    output = subprocess.check_output(cmd, shell = True)
    lines = output.decode("ascii").split("\n")
    for l in lines:
        if "kMDItemContentCreationDate" in l:
            datetime_str = l.split("= ")[1]
            return datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S +0000')
    raise RuntimeError("Failed to find photo date for file %s" % heic_filepath)

def convert_to_and_save_as_jpeg(heic_filename: str, jpeg_filename: str):
    """Reads the HEIC file named heic_filename and save it as JPEG named jpeg_filename.
    """
    with open(os.path.join(HEIC_PATH, heic_filename), 'rb') as f:
        image_bytes = f.read()
        if whatimage.identify_image(image_bytes) != 'heic':
            raise RuntimeError('The given image is not heic.')
        image = pyheif.read_heif(image_bytes)
        pi = PIL.Image.frombytes(mode=image.mode, size=image.size, data=image.data)
        pi.save(os.path.join(JPEG_PATH, jpeg_filename), format="jpeg")

# Convert all HEIC file in HEIC_PATH and save as JPEG in JPEG_PATH.
# The date the photo was taken is appended to the jpeg name.
for heic_filename in os.listdir(HEIC_PATH):
    try:
        date_taken = get_photo_date_taken(heic_filename).astimezone(pytz.timezone('US/Pacific'))
    except RuntimeError:
        continue
    datetime_str = (date_taken + date_taken.utcoffset()).strftime('%y%m%d')
    jpeg_filename = datetime_str + ' ' + heic_filename.split('.')[0] + '.jpeg'
    convert_to_and_save_as_jpeg(heic_filename, jpeg_filename)
