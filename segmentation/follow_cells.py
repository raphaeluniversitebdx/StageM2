# -*- coding: utf-8 -*-
"""
@author: rtranchot
"""



import copy
from correct_cells import verify_array 
from alive_progress import alive_bar
import time
import numpy as np 
import os 


from pathlib import Path
import pandas as pd

import dask.array as da
import cv2  
import tifffile as tiff 


from tqdm import tqdm
from rich.pretty import pprint


def get_cells(img,labels,cellNumber):
    '''
    When given images and labels of shape (t,y,x) this function return the pixel value corresponding to a cell 
    '''
    res=[]
    img_cp=copy.deepcopy(img)
    img_cp=verify_array(img_cp)
    labels=verify_array(labels)

    
    for i in range(0,len(img)):
        label=labels[i]
        frame=img_cp[i]
        
        tmp_res = np.where(label!=cellNumber,0,frame )
        res.append(tmp_res)
        
    res = np.array(res)
    return res 


    
def get_cells_from_3D_stack_v2(stacks,labels,cellNumber):
    '''
    When given stacks of shape (t,z,y,x) and labels of shape (t,y,x) this function return the pixel value corresponding to a cell 
    '''
    res=[]
    img_cp=verify_array(stacks)
    labels=verify_array(labels)

    res = np.where(labels!=cellNumber,0,img_cp)
    #print("Done for cell ", cellNumber)
    return res 


def generate_background(movie_frame, background_signal):
    '''This function generate background for cells image according to a list of background signals 
    '''
    res =[]
    movie_frame=verify_array(movie_frame)
    res=np.where(movie_frame==0, np.array(background_signal),movie_frame)

    return res 

    
def crop_cells(labels):
    '''
    This function allow to crop an stack of shape t,z,y,x in a smaller with all the cells in it 
    '''
    cropped = []
    
    labels=verify_array(labels)
    try:
        min_y = np.min([np.min(np.where(label>0)[1]) for label in labels])
        max_y = np.max([np.max(np.where(label>0)[1]) for label in labels])
        min_x = np.min([np.min(np.where(label>0)[2]) for label in labels])
        max_x = np.max([np.max(np.where(label>0)[2]) for label in labels])
        
        #print(min_y,max_y,  min_x,max_x)
        cropped = labels[:, :, min_y:max_y+1, min_x:max_x+1]
    except ValueError as e:
        print(e)
    return cropped 



def crop_cells_v2(img,labels, cellNumber):
    
    '''
    This function allow to crop an stack of shape t,z,y,x in a smaller with all the cells in it 
    '''
    cropped = []
    
    img=verify_array(img)
    labels=verify_array(labels)
    try:
        min_y = np.min([np.min(np.where(label==cellNumber,img)[1]) for label in labels])
        max_y = np.max([np.max(np.where(label==cellNumber,img)[1]) for label in labels])
        min_x = np.min([np.min(np.where(label==cellNumber,img)[2]) for label in labels])
        max_x = np.max([np.max(np.where(label==cellNumber,img)[2]) for label in labels])
        
        #print(min_y,max_y,  min_x,max_x)
        cropped = img[:, :, min_y:max_y+1, min_x:max_x+1]
    except ValueError as e:
        print(e)
    return cropped 

def crop_cells_v3(labels):
    
    '''
    This function allow to crop an stack of shape z,y,x in a smaller with all the cells in it 
    '''
    cropped = []
    
    labels=verify_array(labels)
    try:
        min_y = np.min([np.min(np.where(label>0)[1]) for label in labels])
        max_y = np.max([np.max(np.where(label>0)[1]) for label in labels])
        min_x = np.min([np.min(np.where(label>0)[2]) for label in labels])
        max_x = np.max([np.max(np.where(label>0)[2]) for label in labels])
        
        #print(min_y,max_y,  min_x,max_x)
        cropped = labels[:, :, min_y:max_y+1, min_x:max_x+1]
    except ValueError as e:
        print(e)
        #return None 
    return cropped 


def crop_cells_with_background(img,labels, cellNumber):
    
    '''
    This function allow to crop an stack of shape t,z,y,x in a smaller with all the cells in it 
    '''
    img=verify_array(img)
    labels=verify_array(labels)
    
    min_y = np.min([np.min(np.where(label==cellNumber)[1]) for label in labels])
    max_y = np.max([np.max(np.where(label==cellNumber)[1]) for label in labels])
    min_x = np.min([np.min(np.where(label==cellNumber)[2]) for label in labels])
    max_x = np.max([np.max(np.where(label==cellNumber)[2]) for label in labels])

    #print(min_y,max_y,  min_x,max_x)
    cropped_img = img[:, :, min_y:max_y+1, min_x:max_x+1]
    cropped_mask = labels[:, :, min_y:max_y+1, min_x:max_x+1]
    return cropped_img, cropped_mask

def save_cells(img, folder, nameKey, imsQ,keyword, cellNumber=''):
    '''
    img : numpy or zarr core array of images 
    folder : directory where the file will be saved
    namekey : common pattern in the name of the images --> this will serve to give a name to the image saved 
    imsQ : common pattern in the name of the images (int)
    cellNumber : defaut = '' if the images correspond to a cell use the number of the cell here  
    keyword : keyword who will be add on the title of the saved file 
    '''
    extensionMov = ".tif"
    
    fullFolder = folder + "/" + keyword + "/"
    
    if not os.path.exists(fullFolder):
        os.makedirs(fullFolder)
            
    with alive_bar(len(img), title = "Saving frame",force_tty=True) as bar :
        for i in range(len(img)): 
            filename =fullFolder+ nameKey + imsQ + "_cell_" + str(cellNumber) + "_t" + f"{i+1:03}" + extensionMov
            try:
                tiff.imwrite(filename, img[i])
            except Exception as e:
                print(f"Error saving {filename}: {e}")
            time.sleep(0.1)
            bar()


