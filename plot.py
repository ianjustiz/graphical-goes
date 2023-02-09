import os
from netCDF4 import Dataset
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np


def process_file_Longwave(filename, directory):
    # Open the NetCDF File
    g16ir = Dataset(filename, 'r')
    band1 = g16ir.variables['CMI_C01'][:]

    # Create variables to store output directory. Make directory if needed
    ir_directory = "{}/ir".format(directory)
    if not os.path.isdir(ir_directory):
        os.makedirs(ir_directory)
    
    save_to = "{}".format(str(filename).replace(directory, ir_directory).replace(".nc",".png"))

    # Get the Brightness Temperature band
    ref_ir = np.ma.array(np.sqrt(g16ir.variables['CMI_C14'][:]), mask=band1.mask)

    # Normalize IR band 
    cleanir = g16ir.variables['CMI_C14'][:]
    cir_min = 200.0
    cir_max = 305.0
    cleanir_c = (cleanir - cir_min) / (cir_max - cir_min)
    cleanir_c = np.maximum(cleanir_c, 0.0)
    cleanir_c = np.minimum(cleanir_c, 1.0)
    cleanir_c = np.float64(cleanir_c)
    
    # Apply colormapping to greyscale image
    color_schema = cm.nipy_spectral(np.minimum(cleanir_c, .99))
    
    # Generate alpha mask for off Earth locations. Stack colormap into blended image
    mask = np.where(band1.mask == True)
    alpha = np.ones(band1.shape)
    alpha[mask] = 0.0
    blended = np.dstack([color_schema[:,:,2], color_schema[:,:,1], color_schema[:,:,0], alpha])

    # Plot it! Without axis & labels
    fig = plt.figure(figsize=(6,6),dpi=300)
    plt.imshow(blended)
    plt.axis('off')
    fig.gca().set_axis_off()
    fig.gca().xaxis.set_major_locator(matplotlib.ticker.NullLocator())
    fig.gca().yaxis.set_major_locator(matplotlib.ticker.NullLocator())

    fig.savefig(save_to, transparent=True, bbox_inches = 'tight', pad_inches = 0)

    plt.close()


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

    fig.savefig(save_to, transparent=True, bbox_inches = 'tight', pad_inches = 0)
    plt.clf()

    # Plot no-ir version!
    fig = plt.figure(figsize=(6,6),dpi=300)
    plt.imshow(blended_noir)
    plt.axis('off')
    fig.gca().set_axis_off()
    fig.gca().xaxis.set_major_locator(matplotlib.ticker.NullLocator())
    fig.gca().yaxis.set_major_locator(matplotlib.ticker.NullLocator())

    fig.savefig(save_to_noir, transparent=True, bbox_inches = 'tight', pad_inches = 0)
    plt.close()


def process_all(directory):
    # Iterate through all files in given directory
    files = os.listdir(directory)
    for path in files:
        local_path = "{}/{}".format(directory, path)

        # For each .nc file, process the modes and subsequently delete
        if ".nc" in str(local_path):
            print("Procesing {}".format(local_path))

            process_file_TrueColor(local_path, directory)
            process_file_Longwave(local_path, directory)

            os.remove(local_path)
