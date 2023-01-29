from plot import process_all
from fetch import fetch_with_params
import json
import os

# process_file_TrueColor()
# process_file_Longwave() # add political boundaries for longwave or in post-processing

satellite_buckets = ["noaa-goes16", "noaa-goes18"]
satellite_bands = ["ABI-L2-MCMIPF", "ABI-L2-MCMIPC"]

fd_dict = {
    "maint_size": 78,
    "time_interval": 10,
    "width": 2310,
    "height": 2310
}

con_dict = {
    "maint_size": 156,
    "time_interval": 5,
    "width": 2325,
    "height": 1395
}

# METADATA FILE CONTENTS:
# -Maintenance file size (i.e. 180)
# -Interval between GOES updates (i.e. 5 mins)
# -Most recent file date (i.e. 1/27/23 17:58 UTC)


def setup_directories():
    for bucket in satellite_buckets:
        for band in satellite_bands:
            directory = "{}/{}".format(bucket, band)

            if not os.path.isdir(directory):
                os.makedirs(directory)
            
            with open("{}/info.json".format(directory), "w") as f:
                if band == "ABI-L2-MCMIPF":
                    json.dump(fd_dict, f)
                else:
                    json.dump(con_dict, f)
            
            fetch_with_params(bucket_name=bucket, subdirectory=band, offset=6)
            process_all(directory)

def update_directories():
    for bucket in satellite_buckets:
        for band in satellite_bands:
            directory = "{}/{}".format(bucket, band)
        
        

setup_directories()

                   # EVERY FIVE MINUTES #

# IF BELOW maintenance size (check beforehand) : Fetch with positive offset until size is met

# Otherwise: 
# Get date of most recently downloaded file in each directory 

# Parse string date to datetime object

# Determine directory location to be checked for next file

# Call fetch_with_params with negative offset

# ----- #

# Call plot.py on entire directory to process files to pngs

# Check maintenance filesize, compare to directory size

# Truncate excess images (oldest first)
