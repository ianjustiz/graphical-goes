#!/usr/bin/env python
import os
from netCDF4 import Dataset
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys

import datetime
from datetime import timedelta

import pathlib

# Run this as
# ./plot.py <MCMIP netcdf file> <output.png>

#if len(sys.argv) < 1:
#	print("Usage: ./plot.py <MCMIP netcdf file>")
#	sys.exit()
#
#import_from = sys.argv[1]
#export_to = sys.argv[1].replace('.nc','.png')

# today = datetime.datetime.utcnow()
# incrementor = today - timedelta(hours=12)

# subdirectory = "ABI-L2-MCMIPC"

# year = incrementor.year
# day = (int)(incrementor.strftime("%j"))
# hour = incrementor.hour
# count = 1

# pat = "{}-{}_{}_{}-{}.nc".format(subdirectory, year, day, hour, count)

directory = "noaa-goes16/ABI-L2-MCMIPF"


def process_file_TrueColor(filename, directory):
    # Open the NetCDF File
    g16nc = Dataset(filename, 'r')
    band1 = g16nc.variables['CMI_C01'][:]

    # Create variables to store output directory. Make directory if needed
    fc_directory = "{}/fc".format(directory)
    noir_directory = "{}/noir".format(directory)
    if not os.path.isdir(noir_directory):
        os.makedirs(noir_directory)
    if not os.path.isdir(fc_directory):
        os.makedirs(fc_directory)

    save_to = "{}".format(str(filename).replace(directory, fc_directory).replace(".nc",".png"))
    save_to_noir = "{}".format(str(filename).replace(directory, noir_directory).replace(".nc",".png"))

    # Get the Blue, Red, and Veggie bands + gamma correct
    ref_blue = np.ma.array(np.sqrt(g16nc.variables['CMI_C01'][:]), mask=band1.mask)
    ref_red = np.ma.array(np.sqrt(g16nc.variables['CMI_C02'][:]), mask=band1.mask)
    ref_veggie = np.ma.array(np.sqrt(g16nc.variables['CMI_C03'][:]), mask=band1.mask)

    # Make the green band using a linear relationship
    ref_green = np.ma.copy(ref_veggie)
    gooddata = np.where(ref_veggie.mask == False)
    ref_green[gooddata] = 0.48358168 * ref_red[gooddata] + 0.45706946 * ref_blue[gooddata] + 0.06038137 * ref_veggie[gooddata]

    # Prepare the Clean IR band by converting brightness temperatures to greyscale values
    cleanir = g16nc.variables['CMI_C13'][:]
    cir_min = 90.0
    cir_max = 313.0
    cleanir_c = (cleanir - cir_min) / (cir_max - cir_min)
    cleanir_c = np.maximum(cleanir_c, 0.0)
    cleanir_c = np.minimum(cleanir_c, 1.0)
    cleanir_c = 1.0 - np.float64(cleanir_c)
    
    # Make an alpha mask so off Earth alpha = 0
    mask = np.where(band1.mask == True)
    alpha = np.ones(band1.shape)
    alpha[mask] = 0.0
    blended = np.dstack([np.maximum(ref_red, cleanir_c), np.maximum(ref_green, cleanir_c), np.maximum(ref_blue, cleanir_c), alpha])
    blended_noir = np.dstack([np.maximum(ref_red, 0), np.maximum(ref_green, 0), np.maximum(ref_blue, 0), alpha])

    # Plot it! Without axis & labels
    fig = plt.figure(figsize=(6,6),dpi=300)
    plt.imshow(blended)
    plt.axis('off')
    fig.gca().set_axis_off()
    fig.gca().xaxis.set_major_locator(matplotlib.ticker.NullLocator())
    fig.gca().yaxis.set_major_locator(matplotlib.ticker.NullLocator())

    # Plot no-ir version!
    fig.savefig(save_to, transparent=True, bbox_inches = 'tight', pad_inches = 0)
    plt.clf()

    fig = plt.figure(figsize=(6,6),dpi=300)
    plt.imshow(blended_noir)
    plt.axis('off')
    fig.gca().set_axis_off()
    fig.gca().xaxis.set_major_locator(matplotlib.ticker.NullLocator())
    fig.gca().yaxis.set_major_locator(matplotlib.ticker.NullLocator())

    fig.savefig(save_to_noir, transparent=True, bbox_inches = 'tight', pad_inches = 0)
    plt.clf()
    


    os.remove(filename)
    



for filepath in pathlib.Path(directory).glob('**/*'):
    process_file_TrueColor(filepath, directory)


# for filename in files:
#     print(filename)
#     if filename.endswith('.nc'):
#         process_file_TrueColor(filename)
        
        # Update file incrementor to next
        # if(count == 11):
        #     incrementor = incrementor + timedelta(hours=1)
            
        #     year = incrementor.year
        #     day = (int)(incrementor.strftime("%j"))
        #     hour = incrementor.hour
        #     count = 0
        # else:
        #     count += 1
        
        #path = "{}-{}_{}_{}-{}.nc".format(subdirectory, year, day, hour, count)


