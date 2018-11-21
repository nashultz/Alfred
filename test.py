#imports
import asyncio
import copy
from datetime import datetime
import functools
import gettext
import io
import json
import os
import pickle
import re
import sys
import tempfile
import time
import traceback

from contextlib import redirect_stdout
from io import BytesIO
from operator import itemgetter
from time import strftime

import aiohttp
import dateparser
import hastebin
from dateutil import tz
from dateutil.relativedelta import relativedelta

import discord
from discord.ext import commands

from alfred import checks
from alfred import pkmn_match
from alfred import utils
from alfred.bot import AlfredBot
from alfred.errors import custom_error_handling
from alfred.logs import init_loggers

# Importing Pytesseract for OCR
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2
import urllib.request as urlr
import numpy as np

filename = 'raidscreenshot3.png'
greyscaleimgresized = 'greyscaleimgrs.png'
timeimg = 'timeimg.png'
gymnameimg = 'gymnameimg.png'
print('Scanning image...')
# Download image from message
# try:
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as resp:
#             data = await resp.read()
#             with open(filename, "wb") as f:
#                 f.write(data)
# except asyncio.TimeoutError:
#     return False
# print("Done.")

# Save image in Greyscale
print("Saving greyscale image...")
greyscimg = cv2.imread(filename, 0)
cv2.imwrite(greyscaleimgresized, greyscimg)
print("Done.")

# Resize to specified size for consistancy
print("Resizing image...")
img = cv2.imread(greyscaleimgresized)
r = 800.0 / img.shape[1]
dim = (800, int(img.shape[0] * r))
resized = cv2.resize(img, dim)
cv2.imwrite(greyscaleimgresized, resized)
print("Done.")

# Crop image for time detection
print("Cropping image to extract time...")
timg = cv2.imread(greyscaleimgresized)
timeimage = timg[0:40, 0:800]
cv2.imwrite(timeimg, timeimage)
print("Done.")

m = cv2.imread(timeimg)
h, w, bpp = np.shape(m)
for py in range(0, h):
    for px in range(0, w):
        if m[py][px][0] > 45 and m[py][px][1] > 45 and m[py][px][2] > 45:
            m[py][px][0] = 255
            m[py][px][1] = 255
            m[py][px][2] = 255
cv2.imwrite(timeimg, m)

# Extract time from image
print("Extracting time...")
ptime = pytesseract.image_to_string(Image.open(timeimg))
p = re.compile('(([0-9])?[0-9]:[0-9][0-9]( [AP]M)?)')
if p.search(ptime):
    time = p.search(ptime).group(1)
    fmat = '%I:%M %p'
    posttime = datetime.strptime(time, fmat).strftime('%H:%M:%S')
else:
    # Convert white text to black
    print("Inverting white text to black...")
    m = cv2.imread(timeimg)
    m = (255 - m)
    cv2.imwrite(timeimg, m)
    print("Done.")
    # m = cv2.imread(timeimg)
    # h, w, bpp = np.shape(m)
    # for py in range(0, h):
    #     for px in range(0, w):
    #         if m[py][px][0] < 70 and m[py][px][1] < 70 and m[py][px][2] < 70:
    #             m[py][px][0] = 0
    #             m[py][px][1] = 0
    #             m[py][px][2] = 0
    # cv2.imwrite(timeimg, m)
    ptime = pytesseract.image_to_string(Image.open(timeimg))
    p = re.compile('(([0-9])?[0-9]:[0-9][0-9]( [AP]M)?)')
    if p.search(ptime):
        time = p.search(ptime).group(1)
        fmat = '%I:%M %p'
        posttime = datetime.strptime(time, fmat).strftime('%H:%M:%S')
    else:
        posttime = datetime.datetime.now().strftime('%H:%M')
if posttime:
    print("Time posted: {}".format(posttime))
else:
    print("No time detected.")

# Crop image for gym name detection
print("Cropping image to extract gym name...")
gimg = cv2.imread(greyscaleimgresized)
gymimage = gimg[60:150, 160:800]
cv2.imwrite(gymnameimg, gymimage)
print("Done.")

# Convert white text to black
print("Inverting white text to black...")
m = cv2.imread(gymnameimg)
m = (255 - m)
cv2.imwrite(gymnameimg, m)
print("Done.")

print("Inverting white text to black...")
m = cv2.imread(gymnameimg)
h, w, bpp = np.shape(m)
for py in range(0, h):
    for px in range(0, w):
        if m[py][px][0] > 50 and m[py][px][1] > 50 and m[py][px][2] > 50:
            m[py][px][0] = 255
            m[py][px][1] = 255
            m[py][px][2] = 255
cv2.imwrite(gymnameimg, m)

# Extract gym name from image


print(pytesseract.image_to_string(Image.open(gymnameimg)))
print('Done.')
