
# SatAlyze
# Ian Justiz and Bed Pandey
import os
import sys
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np

import boto3
from botocore import UNSIGNED
from botocore.config import Config

import datetime
from datetime import timedelta


def fetch_with_params(base_time=datetime.datetime.utcnow(), offset=12, bucket_name = "noaa-goes16", subdirectory="ABI-L2-MCMIPF"):
    # Begin search /offset/ hours from base time
    incrementer = base_time - timedelta(hours=offset)
    
    # Fetch all objects until directory no longer exists

    while fetch_obj(incrementer.year, int(incrementer.strftime("%j")), incrementer.hour, bucket_name, subdirectory) != -1:
        incrementer = incrementer + timedelta(hours=1)


def get_time_file(filename):
    start_index = 1+filename.find('s')

    # Throw -1 if s not found in given file
    if start_index == -1:
        return -1
    
    search_from = filename[start_index:]

    # Slice substring to get time
    year = search_from[0:4]
    day = search_from[4:7]
    hour = search_from[7:9]
    minute = search_from[9:11]
    second = search_from[11:13]

    # Create new time object
    date_form = datetime.datetime.strptime("{}-{}-{}-{}-{}".format(year,day,hour,minute,second) , "%Y-%j-%H-%M-%S")

    # Return epoch time
    return int(date_form.timestamp())


def fetch_obj(year, day, hour, bucket_name, subdirectory):
    # Store variables for AWS server interfacing
    s3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))
    s3_client = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    s3_bucket = s3.Bucket(bucket_name)
    
    # Retrieve list of objects in given directory
    objects = list(s3_bucket.objects.filter(Prefix="{}/{}/{:03d}/{:02d}".format(subdirectory, year, day, hour)))

    inc = 0

    # If no objects matching parameters found, return -1
    if len(objects) == 0:
        return -1
    
    # For each individual file in a directory
    for obj in objects:
        if obj.key[-1] == "/":
            continue
        
        # Fetch metadata and size of file
        meta_data = s3_client.head_object(Bucket=bucket_name, Key=obj.key)
        total_length = int(meta_data.get('ContentLength', 0))
        
        # Generate a path based on file structure in AWS server
        path = "{}/{}".format(bucket_name, subdirectory)
        if not os.path.isdir(path):
            os.makedirs(path)

        local_name = "{}/{}.nc".format(path, get_time_file(obj.key))
        downloaded = 0

        # Draw progress bar and filesize (BUGGY on many systems)
        def progress(chunk):
            nonlocal downloaded
            downloaded += chunk
            done = int(50 * downloaded / total_length)
            sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
            sys.stdout.write(f" {total_length / (1 << 20):,.0f} MB")
            sys.stdout.flush()

        print(f'Downloading {obj.key}')

        # Store file locally
        inc += 1
        with open(local_name, 'wb') as f:
            s3_client.download_fileobj(bucket_name, obj.key, f, Callback=progress)

        print("\n")

