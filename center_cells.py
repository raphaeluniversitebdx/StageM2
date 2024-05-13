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



def center_a_cell(cell):
    '''
    This function use the above function and other operations to compute a whole cell 
    '''
    HS_centroid_list = get_centroid(cell)
    HS_centroid_mean = compute_avg_centroid(HS_centroid_list)
    avg_mean = np.mean(HS_centroid_mean,axis=0)

    offsets = [avg_mean - ctr for ctr in HS_centroid_mean]
    ctr_stacks = [np.roll(img, (int(offset[1]), int(offset[0])), axis=(0,1)) for img, offset in zip(cell,offsets )]
    ctr_stacks = np.array(ctr_stacks)

    return ctr_stacks 


def get_centroid_labels(img,labels,cellNumber):
    '''
    For an hyperstack of shape (t,z,y,x) this function return the centroid of each image 
    '''
    img = verify_array(img)
    labels = verify_array(labels)
    
    res2=[]
    for t in range(0,len(img)) :
        res=[]
        for z in img[t] : 
            tmp=[]
            cy, cx = ndi.center_of_mass(z,labels[t],cellNumber)
            tmp.append(cy)
            tmp.append(cx)

            res.append(tmp) # get a list of z centroids for a frame in t | example if z = 36 len(res)=36
        res2.append(res) # get a list of t centroids for t | example if t = 123 len(res2)=123
    res2 = np.array(res2)
    return res2


def center_a_cell_with_labels(cells,labels,cellNumber):
    '''
    This function use the above function and other operations to compute a whole cell 
    '''
    HS_centroid_list = get_centroid(cells,labels,cellNumber)
    HS_centroid_mean = compute_avg_centroid(HS_centroid_list)

    del HS_centroid_list 

    avg_mean = np.mean(HS_centroid_mean,axis=0)
    offsets = [avg_mean - ctr for ctr in HS_centroid_mean]

    del HS_centroid_mean 
    
    ctr_stacks = [np.roll(img, (int(offset[1]), int(offset[0])), axis=(0,1)) for img, offset in zip(cells,offsets )]
    ctr_stacks = np.array(ctr_stacks)
    
    ctr_masks = [np.roll(img, (int(offset[1]), int(offset[0])), axis=(0,1)) for img, offset in zip(labels,offsets )]
    ctr_masks = np.array(ctr_masks)

    return ctr_stacks, ctr_masks