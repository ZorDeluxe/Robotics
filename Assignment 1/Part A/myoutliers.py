import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statistics
from scipy import stats



""" To test if the data point is an outlier """
def is_outlier(points, thresh=2.5):
    """
    Returns a boolean array with True if points are outliers and False 
    otherwise.

    Parameters:
    -----------
        points : An numobservations by numdimensions array of observations
        thresh : The modified z-score to use as a threshold. Observations with
            a modified z-score (based on the median absolute deviation) greater
            than this value will be classified as outliers.

    Returns:
    --------
        mask : A numobservations-length boolean array.

    References:
    ----------
        Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
        Handle Outliers", The ASQC Basic References in Quality Control:
        Statistical Techniques, Edward F. Mykytka, Ph.D., Editor. 
    """
    if len(points.shape) == 1:
        points = points[:,None]
    median = np.median(points, axis=0)    
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    modified_z_score = 0.6745 * diff / med_abs_deviation

    return abs(modified_z_score) > thresh


""" Iglewicz and Hoaglin's modified Z-score """ 
def outlier (points, distance, thresh=3.5):  
    
    error = points - distance
    median = statistics.median(error)    
    median_abs = statistics.median(abs(error))
    modified_z_score = 0.6745 * (error - median) / median_abs
        
    return abs(modified_z_score) > thresh

"""" Z-Score Algorithm """
def zScore (points, thresh=2.5):
    zScore = np.abs(stats.zscore(points))
    
    return zScore > thresh
                    
""" Moving average median filter """
def get_median_filtered(signal, threshold=3):
    signal = signal.copy()
    difference = np.abs(signal - np.median(signal))
    median_difference = np.median(difference)
    if median_difference == 0:
        s = 0
    else:
        s = difference / float(median_difference)
    mask = s > threshold
    signal[mask] = np.median(signal)
    return signal
