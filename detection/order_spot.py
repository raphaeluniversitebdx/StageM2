from alive_progress import alive_bar
import time
import numpy as np 
from copy import deepcopy 
def order_clusters_frames(clustersFrames,mipSequenceCell,threshold ):

    res = []
    with alive_bar(len(clustersFrames), title = "order cluster frame",force_tty=True) as bar :
        for i in range(len(clustersFrames)):
            #print('clustersFrames', i)
            frame = clustersFrames[i]
            tmp =[]
            id = 0
            for j in range(len(frame)):
                y_coord = frame[j][1]
                x_coord = frame[j][2]

                test = np.array(mipSequenceCell[i][y_coord:y_coord+1,x_coord:x_coord+1])
                val = test[0][0]
                if val < threshold : 
                    print(i,val)
                tmp.append(val)

            try :
                # possibilite de rajouter une condition 
                # pour filtrer les sites de transcription uniquement en rajoutant un threshold de 1000
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
    '''This function sort a list of numpy array according to a threshold corresponding to the intensity of the mipSequenceCell's pixels 
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
                print(i, tmp, test)
                print(e)
                res.append([np.zeros(5)])
            time.sleep(0.1)
            bar()
            i = i+1 
        return res 




def merge_clusters_frame(res,diff):
    '''
    This function compute coordinate of clusters Frame with the compatible neighboor to get a better quantification 
    '''
    res2 = deepcopy(res)
    p = 0
    new_clusters_frames = []
    for frames in res2 :
        tc = frames[0]
        tmp = [tc]
        for cluster in frames[1:]:
            test_z = tc[0] - cluster[0]
            test_y = tc[1] - cluster[1]
            test_x = tc[2] - cluster[2]

            if -diff <=test_y <= diff and -diff <=test_x <= diff and -diff <= test_z <= diff :
                # print('frame :', p,'y :',test_y,'x :',test_x)
                tmp.append(cluster)
        
        for t in tmp[1:] :
            #average the coordinate of the clusters 
            tc[0] = (tc[0]+t[0])/2 
            tc[1] = (tc[1]+t[1])/2
            tc[2] = (tc[2]+t[2])/2

            # sum of the molecule 
            tc[3] = tc[3] + t[3]
            
        new_clusters_frames.append([tc])
        p = p+1
        
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
    try : 
        current = liste.index(elem_to_move)
    except ValueError as e : 
        print(e) 
        current = int(input('Enter the position of the array : '))
    liste = liste[:current]+liste[current+1:]
    liste.insert(new_position, elem_to_move)

    return liste 

def create_index2(clustersFrames):
    index = 0
    res=[]
    for frame in clustersFrames : 
        
        #frame[-1]=index
        
        frame[0][-1] = index
        res.append(frame)
        index = index + 1 
        
    return res