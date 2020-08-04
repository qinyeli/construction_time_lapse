#!/usr/local/bin/python3

"""Converts all JPEG files in JPEG_PATH into an MOV movie.

Expects the JPEG files to be named in the format 'YYMMDD filename.jpeg'.
"""

import cv2
import datetime
import os

JPEG_PATH = 'jpeg_img'
jpeg_filenames = sorted(os.listdir(JPEG_PATH))
jpeg_filenames.remove('.DS_Store')

# Get the frame size.
frame = cv2.imread(os.path.join(JPEG_PATH, jpeg_filenames[0]))
height, width, layers = frame.shape

# # Figure out the duration of each frame.
# # Expects the format of each filename to be something like '181213 IMG_0028.jpeg'
# duration = []
# prev_datetime = None
# curr_datetime = None
# for filename in jpeg_filenames:
#     prev_datetime = curr_datetime
#     curr_datetime = datetime.datetime.strptime(filename.split()[0], '%y%m%d')
#     if prev_datetime is None:
#         continue
#     duration.append((curr_datetime - prev_datetime).days)
# duration.append(int(sum(duration) / len(duration)))

fourcc = cv2.VideoWriter_fourcc(*'avc1')
video = cv2.VideoWriter('mp6_construction.mov', fourcc, 4, (width, height))
for i in range(len(jpeg_filenames)):
    filename = jpeg_filenames[i]
    video.write(cv2.imread(os.path.join(JPEG_PATH, filename)))
cv2.destroyAllWindows()
video.release()