# -*- coding: utf-8 -*-
"""
@author: rtranchot
"""


import os
import numpy as np
import scipy.ndimage as ndi
from correct_cells import verify_array 



def get_centroid(img,labels=None,cellNumber=None):
    '''
    For an hyperstack of shape (t,z,y,x) this function return the centroid of each image 
    '''
    img = verify_array(img)
    labels = verify_array(labels)
    
    
    res2=[]
    time = img.shape[0]
    z_3d = img.shape[1]
    
    #print(time,z_3d)
    for t in range(0,time) :
        res=[]
        for z in range(0,z_3d): 
            tmp=[]
            cy, cx = ndi.center_of_mass(img[t][z],labels[t][z],cellNumber)
            tmp.append(cy)
            tmp.append(cx)

            res.append(tmp) # get a list of z centroids for a frame in t | example if z = 36 len(res)=36
        res2.append(res) # get a list of t centroids for t | example if t = 123 len(res2)=123
    res2 = np.array(res2)
    return res2



def compute_avg_centroid(centroid_list):
    '''
    This function return a list of mean for a centroid list of an hyperstack 
    Example for an hyperstack of shape (t,z,y,x) this will return a list of list of lenght t. 
    The mean will be done on the centroid list corresponding to a z 
    '''
    res = []
    for i in range(0,len(centroid_list)):
        
        avg_centroid = np.mean(centroid_list[i],axis=0)
        res.append(avg_centroid)
    
    return res 




def center_image_for_z(images,labels,cellNumber):
    '''
    This function compute a list of centroid for each frames in a hyperstack of shape [t,z,y,x] 
    Then use it to compute a list of centroid mean for each frames in t 
    Then compute an average mean throughout the movie 
    And use it to move the image of the hyperstack by computing offsets between the average mean and the centroid list for the hyperstack
    
    ________________________
    
    This function return the centered images and the masks as numpy array
    
    '''
    res_images=[]
    res_labels=[]
    #get lists of centroid for the cell
    HS_centroid_list = get_centroid(images,labels,cellNumber)
    HS_centroid_mean = compute_avg_centroid(HS_centroid_list)
    #avg_mean = np.mean(HS_centroid_mean,axis=0)

    img_mean = verify_array(images[0][0]) #get center of the movie 
    avg_mean = ndi.center_of_mass(img_mean)
    offsets = [avg_mean - ctr for ctr in HS_centroid_list] #3d list of centroid for 1 frame in t
    for t in range(0,len(images)): 
        #center the movies and labels 
        tmp_image = [np.roll(img,(int(offset[0]), int(offset[1])), axis=(0,1)) for img, offset in zip(images[t],offsets[t])]
        tmp_label = [np.roll(img,(int(offset[0]), int(offset[1])), axis=(0,1)) for img, offset in zip(labels[t],offsets[t])]
        
        res_images.append(tmp_image)
        res_labels.append(tmp_label)
    
    res_images = np.array(res_images)
    res_labels = np.array(res_labels)
    
    return res_images, res_labels
    



