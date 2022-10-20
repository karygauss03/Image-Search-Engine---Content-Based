#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import argparse
# import the Image and TAGS classes from Pillow (PIL)
from PIL import Image
from PIL.ExifTags import TAGS

import uuid # for image meta data ID
import datetime # for image meta data timestamp






"""
Function that uses PIL's TAGS class to get an image's EXIF
meta data and returns it all in a dict
"""
def get_image_exif(img):
    # use PIL to verify image is not corrupted
    img.verify()

    try:
        # call the img's getexif() method and return EXIF data
        exif = img._getexif()
        exif_data = {}

        # iterate over the exif items
        for (meta, value) in exif.items():
            try:
                # put the exif data into the dict obj
                exif_data[TAGS.get(meta)] = value
            except AttributeError as error:
                print ('get_image_meta AttributeError for:', file_name, '--', error)
    except AttributeError:
        # if img file doesn't have _getexif, then give empty dict
        exif_data = {}
    return exif_data

"""
Function to create new meta data for the Elasticsearch
document. If certain meta data is missing from the orginal,
then this script will "fill in the gaps" for the new documents
to be indexed.
"""
def create_exif_data(img, clas, split):

    # create a new dict obj for the Elasticsearch doc
    es_doc = {}
    es_doc["size"] = img.size

    # call the method to have PIL return exif data
    exif_data = get_image_exif(img)

    # get the PIL img's format and MIME
    es_doc["image_format"] = img.format
    es_doc["image_mime"] = Image.MIME[img.format]

    # get datetime meta data from one of these keys if possible
    if 'DateTimeOriginal' in exif_data:
        es_doc['datetime'] = exif_data['DateTimeOriginal']

    elif 'DateTime' in exif_data:
        es_doc['datetime'] = exif_data['DateTime']

    elif 'DateTimeDigitized' in exif_data:
        es_doc['datetime'] = exif_data['DateTimeDigitized']

    # if none of these exist, then use current timestamp
    else:
        es_doc['datetime'] = str( datetime.datetime.now() )

    # create a UUID for the image if none exists
    if 'ImageUniqueID' in exif_data:
        es_doc['uuid'] = exif_data['ImageUniqueID']
    else:
        # create a UUID converted to string
        es_doc['uuid'] = str( uuid.uuid4() )
    
    es_doc['classe'] = clas
    es_doc['family'] = split
    
    # return the dict
    return es_doc

