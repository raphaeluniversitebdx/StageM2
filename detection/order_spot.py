# -*- coding: utf-8 -*-
"""
@author: rtranchot
"""


from alive_progress import alive_bar
from datetime import datetime
from copy import deepcopy 
import numpy as np 
import time
import csv 
import os 
import sys 

import sys
import os

# Ajoutez le répertoire parent au sys.path
chemin_du_repertoire_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if chemin_du_repertoire_parent not in sys.path:
    sys.path.append(chemin_du_repertoire_parent)

# Maintenant, vous pouvez importer le module
from follow_cells import *



def sort_spot_list(spot_list,mipSequenceCell,distance=2):
    '''
    The goal of this function is to sort spot which are on the side of a cell to improve the computing of the reference spot
    spot_list : numpy array corresponding to a numpy array of spots through the whole movie
    mipSequenceCell : 2D projection of the movie
    distance : distance in pixel beetwen the cell and the background 
    _____________________________________________________________
    return a new spot list throughout the movie 

    '''
    
    res=[]
    i=0
    count=0
    for spot_frame in spot_list : 
        tmp=[]
        
        for spot in spot_frame: 
            
            z=spot[0]
            y=spot[1]
            x=spot[2]
            
            #negative 
            test_y_n=y-distance
            test_x_n=x-distance
            #positive
            test_y_p=y+distance
            test_x_p=x+distance
            #test coordinate of spots to verify if they are at the border of a cell 
            test_mip_1=np.array(mipSequenceCell[i][test_y_n][test_x_n])
            test_mip_2=np.array(mipSequenceCell[i][test_y_p][test_x_p])
            test_mip_3=np.array(mipSequenceCell[i][test_y_n][test_x_p])
            test_mip_4=np.array(mipSequenceCell[i][test_y_p][test_x_n])
            
            
            if test_mip_1==0 or test_mip_2==0  or test_mip_3==0  or test_mip_4 ==0 :
                count=count+1
            else : 
                tmp.append(spot)
        # if there is no spots
        if len(tmp)==0:
            tmp=np.empty((0,3))
            res.append(tmp)
                    
        res.append(np.array(tmp))
        i=i+1
    
    
    print('eliminated spots :', count)
    return res

def order_clusters_frames(clustersFrames,mipSequenceCell,threshold ):
    '''
    The goal of this function is to order the clusters frames by the intensity of the corresponding pixels

    clustersFrames : coordinate of the clusters throughout the movie
    mipSequenceCell : 2D projection of the movie
    threshold : a specific value below which the a specific value for a candidate clusters will be eliminated  
    ___________________________________________________
    return a new list of clusters frame 
    '''
    res = []
    with alive_bar(len(clustersFrames), title = "order cluster frame",force_tty=True) as bar :
        for i in range(len(clustersFrames)):
            frame = clustersFrames[i]
            tmp =[]
            id = 0
            for j in range(len(frame)):
                y_coord = frame[j][1]
                x_coord = frame[j][2]
                #test value of pixel of the image
                test = np.array(mipSequenceCell[i][y_coord:y_coord+1,x_coord:x_coord+1])
                val = test[0][0]
                if val < threshold : 
                    print(i,val)
                tmp.append(val)
            try :
                # test if there is no value in tmp > threshold
                if max(tmp) < threshold :
                    res.append([np.zeros(5)])
                else :
                    index_max = tmp.index(max(tmp))
                    #print(max(tmp), index_max)
                    #print(frame)
                    res.append([frame[index_max]])

            except ValueError as e:
                res.append([np.zeros(5)])
            time.sleep(0.1)
            bar()
        
    
        return res 

def compare_array(array,array_list):
    '''
    This function compare an array with an array list 
    '''
    res=[]
    for a in array_list : 
        cr = np.equal(array[...,-1],a[...,-1])
        cr = np.any(cr,axis=0)
        res.append(cr)
        
    return res 

def sort_clustersFrames(clustersFrames,mipSequenceCell,threshold,perc=1):
    '''
    This function sort a list of numpy array according to a threshold corresponding to the intensity of the mipSequenceCell's pixels 
    ________________________________________________________
    clustersFrames : list of clusters Frames throughout the movie should be of shape [z,y,x,n,i]
    mipSequenceCell : a 2D movie of a cell
    threshold : a threshold of intensity 
    perc : a percentage of clusters that should be conserved
    ________________________________________________________
    return a list of sorted clustersFrames by intensity 

    '''

    clustersFrames_cp = deepcopy(clustersFrames)
    res = []
    i = 0 
    with alive_bar(len(clustersFrames_cp), title = "sort cluster frame",force_tty=True) as bar : 
        for frames in clustersFrames_cp: 
            tmp = []
            tmp_res = []
            for cand in frames :
                y = cand[1]
                x = cand[2]
                
                test = np.array(mipSequenceCell[i][y:y+1, x:x+1])
                
                val = test[0][0]
                #if val < threshold: 
                    #print(val)
                tmp.append(val) 
            #print(i, np.array(tmp))
            
            
            try : 
                if max(tmp)<threshold:
                    res.append([np.zeros(5)])
                    
                else : 
                    # print('i = ', i,'len frames = ', int(len(frames)*perc))
                    for j in range(0,int(len(frames)*perc)):
                        index_max = tmp.index(max(tmp)) #index of most intense point of images 
                        fmax = deepcopy(frames[index_max]) # get corresponding clusters coordinates 
                        cp = compare_array(fmax,tmp_res)

                        #print(i,j, fmax, frames, index_max)
                        if np.any(cp)!= True :
                            #print("!= True")
                            tmp_res.append(fmax)
                        tmp.pop(index_max) # pop max point 
                        
                        
                        frames = frames.tolist()
                        frames.pop(index_max) # pop corresponding clusters 
                        frames = np.array(frames)
                        #print('after \n ', frames)
                    res.append(tmp_res)
            except ValueError as e : 
                #print(i, tmp, test)
                print(e)
                res.append([np.zeros(5)])
            time.sleep(0.1)
            bar()
            i = i+1 
        return res 



def merge_clusters_frame(res,mipSequenceCell,diffxy,diffz,perc=0.5):
    '''
    This function compute coordinate of clusters Frame with the compatible neighboor to get a better quantification 

    ______________________________________________________
    res : an array corresponding to a list of sorted clusters with the clusters[0] always corresponding to the most intense pixel 
    mipSequenceCell : a 2D movie of a cell
    diffxy, diffz : a radius in pixel for the 3 dimensions 
    perc : percentage of tolerance of intensity for perc=0.5 an the most intense pixel = 2000, the tolerance will be from a range of 1000 to 2000
    ____________________________________________________
    return a list of merged clusters according to the coordinate and the intensities 
    ___________________________________________________
    exemple : b = merge_clusters_frame(a,mipSequenceCell,diffxy=5,diffz=1) 
    '''

    # prendre en compte 
    res2 = deepcopy(res)
    p = 0
    i=0
    new_clusters_frames = []
    
    for frames in res2 :
        tc = frames[0]
        tmp = [tc]
        
        threshold = np.array(mipSequenceCell[i][tc[1]][tc[2]])*perc
        #print(i, threshold)
        for cluster in frames[1:]:
            # define tests in 3 dimensions
            test_z = tc[0] - cluster[0]
            test_y = tc[1] - cluster[1]
            test_x = tc[2] - cluster[2]

            # define test on intensity 
            test_array_a = np.array(mipSequenceCell[i][cluster[1]][cluster[2]])
            test_array_b =  np.array(mipSequenceCell[i][tc[1]][tc[2]])
            test_array =  int(test_array_a) - int(test_array_b) 

            if -diffxy <=test_y <= diffxy and -diffxy <=test_x <= diffxy and -diffz <= test_z <= diffz :
                if -threshold <= test_array <= +threshold : 
                    tmp.append(cluster)
                    
        
        for t in tmp[1:] :
            #average the coordinate of the clusters 
            tc[0] = (tc[0]+t[0])/2 
            tc[1] = (tc[1]+t[1])/2
            tc[2] = (tc[2]+t[2])/2

            # sum of the molecules 
            tc[3] = tc[3] + t[3]
        i=i+1
        new_clusters_frames.append([tc])
    return new_clusters_frames

def get_all_clusters(images,threshold,size):
    '''
    This function return a list of array corresponding to all the pixel corresponding to the most intense regions of a cell 
    '''
    res=[]
    i = 0
    for frames in images : 
        tmp = np.where(frames>threshold)
        coord = []
        for px in range(0,len(tmp[0])):
            z = tmp[0][px]
            y = tmp[1][px]
            x = tmp[2][px]
            if len(coord) < size : 
                coord.append([z,y,x,i])
        res.append(coord)
        i = i+1 
    return res 

def move_sorted_clustersFrames(liste, elem_to_move, new_position): 
    '''
    This function is useful to move manually a clusters in a list to choose the actual clusters before the computing of the neighbors 
    _________________________________________________
    liste : list of the clustersFrame at time t 
    elem_to_move : np.array of the element to move 
    new_position : position where the element to move should be at
    _________________________________________________

    return a list of the clusters frame in time t 
    ________________________________________________
    exemple : a[2] = move_sorted_clustersFrames(a[2], np.array(a[2][1]), 0) 
    '''
    try : 
        current = liste.index(elem_to_move)
    except ValueError as e : 
        print(e) 
        current = int(input('Enter the position of the array : '))
    liste = liste[:current]+liste[current+1:]
    liste.insert(new_position, elem_to_move)

    return liste 

def create_index(clustersFrames):
    index = 0
    res=[]
    for frame in clustersFrames : 
        
        #frame[-1]=index
        
        frame[0][-1] = index
        res.append(frame)
        index = index + 1 
        
    return res


def save_csv_file(homeFolder,nameKey,imsQ,cellNumber,selectedThreshold,alpha,beta,gamma,c):
    '''
    This function save information about clusters frame in a csv file.
    The csv file a saved in a special folder created in function of the day and the name of the movie 
    ___________________________________________________
    homeFolder : the folder where the movie folder is 
    nameKey : the movie folder which should have the same name as the movie file 
    imsQ : the last number of the movie folder's name can be empty 
    cellNumber : the number of the cells 
    selectedThreshold : selected threshold for the detection of the spots and clusters 
    alpha,beta,gamma : selected parameters 
    c : clustersFrame list to save 
    ________________________________________________
    return nothing 


    '''
    b = np.concatenate(c)
    entete = ['z','y','x','n_molecule','minute']
    date = datetime.today().strftime('%Y_%m_%d')
    
    savepath_subfolder = date + '_' + nameKey + imsQ +  '/'
    savepath_folder = homeFolder+nameKey+imsQ + '/' + savepath_subfolder
    savepath_name_file = nameKey + imsQ + '_TS' +'_cell_' + cellNumber
    savepath_param = '_bleach_correction_sort_ref_spots'+  str(alpha) +'_' + str(beta) + '_' + str(gamma) + '_thres_' + str(selectedThreshold)
    savepath = savepath_folder + savepath_name_file + savepath_param +  '.csv'  
    
    if not os.path.exists(savepath_folder):
        os.makedirs(savepath_folder)
    
    with open(savepath, 'w', newline='') as csv_file :
        writer = csv.writer(csv_file)
        writer.writerow(entete)
        writer.writerows(b)
    
    print('saved on ', savepath)



def sort_spot_list_mask(spot_list,mipSequenceCell,mask,cellNumber):
    '''
    The goal of this function is to sort spot which are on the side of a cell to improve the computing of the reference spot
    spot_list : numpy array corresponding to a numpy array of spots through the whole movie
    mipSequenceCell : 2D projection of the movie
    '''

    test_cell = get_cells(mipSequenceCell,mask,int(cellNumber))
    res=[]
    i=0
    count=0
    for spot_frame in spot_list : 
        tmp=[]
        
        for spot in spot_frame: 
            
            z=spot[0]
            y=spot[1]
            x=spot[2]
            
            #test_cell = np.max(test_cell, axis=1)
            
          
            if test_cell[i][y][x]!=0 : 
                tmp.append(spot)
            else : 
                count=count+1
            
        # if there is no spots
        if len(tmp)==0:
            tmp=np.empty((0,3))
            res.append(tmp)
                    
        res.append(np.array(tmp))
        i=i+1
    
    
    print('eliminated spots :', count)
    return res