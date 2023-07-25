import numpy as np
from scipy.stats import linregress

def linear_regression(x,y):
    """Performs a linear regression and returns the slope, intercept, and pvalue"""
    res = linregress(x,y)
    return res.slope,res.intercept,res.pvalue