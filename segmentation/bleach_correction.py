import numpy as np 
from correct_cells import verify_array


'''
Prendre les images de cellules, les Z projeter, recuperer les valeurs de pixels, trier les clusters si ils sont present 
calculer des moyenne sur un nombre de pixel identique entre toute les frames, obtenir  la difference en fonction du temps 
corriger bleaching , spot de reference pondere 
'''


def get_intensity(img):
    '''
    This function return a list corresponding to the intensity of the cells 
    
    '''
    img=verify_array(img)
    res =[]
    for frame in img : 
        tmp = frame[frame>0]
        res.append(tmp)
    return res 


def erase_clusters(img,threshold):
    '''
    This function erase a percentage of highest value pixel in term of intensity according to a threshold 
    '''
    index_hi = []
    for frame in img : 
        tmp = []
        for i in range (0,len(frame)):
            if frame[i] > threshold:
                tmp.append(i)
        new_arr = np.delete(frame,tmp)
        index_hi.append(new_arr)
        #index_hi.append(tmp)


    return index_hi

def get_same_lenght(img):
    '''
    return the minimal length from all frames 
    '''

    return (len(min(img, key=len)))

def compute_var(mean_list):
    var_list = []
    for i in range (0,123):
        try :
            a = mean_list[i]
            b = mean_list[i+1]
            var = ((a/b)-1)*100
            var_list.append(var)
        except IndexError as e :
            print('Done')
    return var_list 


    # (i - i1) / i 