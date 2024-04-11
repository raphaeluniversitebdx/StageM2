# Import


import os
from pathlib import Path
import pandas as pd

import dask.array as da
import cv2  
import tifffile as tiff 

import numpy as np
from tqdm import tqdm
from rich.pretty import pprint
from alive_progress import alive_bar
import time

# Functions 

def get_cells_number(labels):
    '''
    Return the number of the latest cell detected by ultrack
    '''
    labels = verify_array(labels)
    print("previous number of cells : ", np.max(labels))
    return np.max(labels)


def count_cells(labels):
    '''
    Return the number of counted cell 
    '''
    labels = verify_array(labels)
    res = np.unique(labels)
    res = np.count_nonzero(res)
    print("actual max number of cells : ", res)
    return res 



def verify_array(labels):
    '''
    Convert labels to numpy array
    '''
    if not isinstance(labels, np.ndarray):

        if isinstance(labels,list):
            labels = np.array(labels)

        if isinstance(labels, da.core.Array):
            labels = labels.compute()

    return labels


def get_cells_numbers_on_all_frames(labels):
    '''
    Return a percentage and a list of cells present in all frames 
    '''
    labels = verify_array(labels)
    get_cells_number(labels) 
    nb_max = count_cells(labels)
    frame_cell_list=[]
    
    
    # get lists of all labels for each frames 
    for label in labels : 
        cell_list=np.unique(label)
        
        frame_cell_list.append(cell_list)

    # get list of frames 0
    frame_0 = frame_cell_list[0]

    res = list(set.intersection(*map(set,frame_cell_list)))
    print("number of cells present from first to last frame : ",len(res)-1)
    print("percentage of cells present from first to last frame : ", ((len(res)-1)/nb_max)*100, "%")

    percentage = ((len(res)-1)/nb_max)*100
    return percentage,res 



def delete_cells(labels,cell):
    '''
    Delete cell from all frames 
    '''
    res = []
    labels = verify_array(labels)

    for label in labels:
        for y in range(0,label.shape[0]):
            for x in range (0,label.shape[1]):
                if label[y][x] == cell:
                    label[y][x]=0
        res.append(label)
    print("cell ",cell, "has been deleted on all frames")
    return res 

def extends_cells(labels,cellpose,cellNumber,applyNUmber,minLen): # retravailler cette fonction pour eviter de manipuler d'autre cellules --> utiliser les coordonnees x,y 
    '''
    The goal of this function is to use cellpose label to draw 
    '''
    res=[]
    labels = verify_array(labels)
    cellpose = verify_array(cellpose)

    with alive_bar(len(labels), title = "extends frame",force_tty=True) as bar :
        for z in range(minLen,labels.shape[0]):
            for y in range(0,labels.shape[1]):
                for x in range(0,labels.shape[2]):
                    if cellpose[z][y][x]==cellNumber :
                        if labels[z][y][x]==0:
                            
                            labels[z][y][x]=applyNUmber
            res.append(labels[z])
            time.sleep(0.1)
            bar()
        print("Cell ", applyNUmber, " has been drawed" )
    return res

def merge_neighboor_cells(parent_cell, child_cell,labels):
    '''
    The goal of this fonction is to merge neighboors cells where cellpose detect them as two when there is only one cell
    
    '''
    res=[]
    labels = verify_array(labels)
    
    for label in labels:
        for y in range (0, label.shape[0]):
            for x in range (0,label.shape[1]):
                if label[y][x] == child_cell:
                    label[y][x]=parent_cell
        res.append(label)
        

    print("Cell ", parent_cell, "has been joined to cell ", child_cell)
    return res


def save_zarr_images(img, folder, nameKey, imsQ,keyword, cellNumber=''):
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
            
    img = verify_array(img)
    with alive_bar(len(img), title = "Saving frame",force_tty=True) as bar :
        for i in range(len(img)):  # No need for range(0, 10)
            filename =fullFolder+ nameKey + imsQ + "_" + keyword + "_" + str(cellNumber) + "_t" + f"{i+1:03}" + extensionMov
            try:
                tiff.imwrite(filename, img[i])
                #print("Done for", filename)
            except Exception as e:
                print(f"Error saving {filename}: {e}")
            time.sleep(0.1)
            bar()



def save_layers(img,name):
    extensionMov = ".tif"
    fullFolder = name + '/'
    if not os.path.exists(fullFolder):
        os.makedirs(fullFolder)
    img = verify_array(img)
    with alive_bar(len(img), title = "Saving frame",force_tty=True) as bar :
        for i in range(len(img)):  # No need for range(0, 10)
            filename = fullFolder + name + "_t" + f"{i+1:03}" + extensionMov
            try:
                tiff.imwrite(filename, img[i])
                #print("Done for", filename)
            except Exception as e:
                print(f"Error saving {filename}: {e}")
            time.sleep(0.1)
            bar()