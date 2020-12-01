import ast
import pandas as pd
import numpy as np


def string_to_vector(string):
    arr_str = " ".join(string.split()) # remove multiple spaces
    arr_str = arr_str.replace(" ",",") # replace single spaces with ,
    arr = np.array(ast.literal_eval(arr_str))
    arr = arr[0] # take best pose
    arr = np.expand_dims(arr, axis=0)
    arr = np.delete(arr, obj=2, axis=2) # remove confidence score
    arr = arr.reshape(1,50) # Flatten
    return arr

def concatenate_arrays(pandas_series):
    num_errors = 0
    prev_good_arr = np.zeros((1,50))
    all_coordinates = np.array([]).reshape(0,50)
    for arr_string in pandas_series:
        try:
            arr = string_to_vector(arr_string)
            prev_good_arr = arr
        except:
            arr = prev_good_arr
            num_errors = num_errors + 1
        all_coordinates = np.vstack((all_coordinates, arr)) #TODO: FIX
    print("Number of bad frames: {:d}".format(num_errors))
    return all_coordinates     
