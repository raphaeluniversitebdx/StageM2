import os
import napari
import tifffile
import numpy as np
import matplotlib.pyplot as plt

import bigfish
import bigfish.plot as plot
import bigfish.stack as stack
import bigfish.detection as detection
import bigfish.multistack as multistack

from copy import deepcopy
from dask.array.image import imread as imr
from bigfish.detection.utils import get_object_radius_pixel
from buildReferenceSpot import buildReferenceSpotFromImages
from runBigfishDetection import getSpotAndClusters, saveSpotsNPZ, reorderZstack



def adjust_threshold(mean_list, voxelRadius,objectRadius,images_input):


    '''
    Le but de cette fonction est de prendre la liste des moyennes de chaque image 
    afin de calculer une difference de moyenne d'une frame a l'autre pour ajuster 
    le threshold en fonction de cette difference de moyenne et du facteur calcule 
    '''
    images=[]    
    spots_list=[]
    mean_all_frames = mean(mean_list)
  
    spot_radius_px = detection.get_object_radius_pixel(
    voxel_size_nm=voxelRadius, 
    object_radius_nm=objectRadius, 
    ndim=3)


    for t in range(1,maxFrame,1):

    path = os.path.join(cell_Crop_Folder, nucleiStackForm+str(cellNumber)+'_t'+str(f"{t:03}")+".tif")
    rna = stack.read_image(path)
    images.append(rna)

    n=len(images)
    print("Total number of images : "+str(n))


    selectedThreshold_loop = selectedThreshold
    for rna in images:
        # LoG filter
        rna_log = stack.log_filter(rna, sigma=spot_radius_px)

        # local maximum detection
        mask = detection.local_maximum_detection(rna_log, min_distance=spot_radius_px)

        # thresholding
        threshold = detection.automated_threshold_setting(rna_log, mask)
        
        
        #adjust threshold

        variation = ((mean_list[i]/mean_list[i+1])-1)*100
        selectedThreshold_loop = (selectedThreshold_loop)-factor 
        print(selectedThreshold_loop)




        spots_, _ = detection.spots_thresholding(rna_log, mask, float(selectedThreshold_loop))
        spots_list.append(spots_)
    return spots_list


