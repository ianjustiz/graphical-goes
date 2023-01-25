
# SatAlyze
# Ian Justiz
import os
import sys
from netCDF4 import Dataset
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import boto3
from botocore import UNSIGNED
from botocore.config import Config

bucket_name = "noaa-goes16"


def fetch_obj(year, day, hour, subdirectory="ABI-L2-MCMIPF"):
    s3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))
    s3_client = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    s3_bucket = s3.Bucket(bucket_name)

    objects = list(s3_bucket.objects.filter(Prefix="{}/{}/{:03d}/{:02d}".format(subdirectory, year, day, hour)))

    inc = 0

    for obj in objects:
        if obj.key[-1] == "/":
            continue

        meta_data = s3_client.head_object(Bucket=bucket_name, Key=obj.key)
        total_length = int(meta_data.get('ContentLength', 0))
        local_name = "{}-{}_{}_{}-{}.nc".format(subdirectory, year, day, hour, inc)
        downloaded = 0

        # draw progress bar
        def progress(chunk):
            nonlocal downloaded
            downloaded += chunk
            done = int(50 * downloaded / total_length)
            sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
            sys.stdout.write(f" {total_length / (1 << 20):,.0f} MB")
            sys.stdout.flush()

        print(f'Downloading {obj.key}')

        inc += 1
        with open(local_name, 'wb') as f:
            s3_client.download_fileobj(bucket_name, obj.key, f, Callback=progress)

        print("\n")


fetch_obj(2023, 25, 2)












# g16nc = Dataset('OR_ABI-L1b-RadM1-M3C02_G16_s20171931811268_e20171931811326_c20171931811356.nc', 'r')
# radiance = g16nc.variables['Rad'][:]
# g16nc.close()
# g16nc = None
#
# fig = plt.figure(figsize=(6,6),dpi=200)
# im = plt.imshow(radiance, cmap='Greys_r')
# cb = fig.colorbar(im, orientation='horizontal')
# cb.set_ticks([1, 100, 200, 300, 400, 500, 600])
# cb.set_label('Radiance (W m-2 sr-1 um-1)')
# plt.show()
