# students have to fill in a dataframe of class genotypes and phenotypes
import numpy as np
import numpy.random as npr
from scipy.stats import linregress
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from time import time
from math import floor, log10, inf

number_of_SNPs = 5

def allele_frequencies():
    np.random.seed(42)
    f = npr.beta(4, 4, size=number_of_SNPs)
    return f

def simulate_genotypes(number_of_people=1,randomseed=None):
    # get allele frequencies
    probabilities = allele_frequencies()
    #set the random seed
    if randomseed is None:
        np.random.seed(np.int64(time()))
    else:
        np.random.seed(randomseed)
    #generate genotypes
    genotypes = np.empty((number_of_people, number_of_SNPs), dtype=int)
    for i in range(number_of_SNPs):
        genotypes[:, i] = npr.binomial(2, probabilities[i], size=number_of_people)
    return genotypes

def true_effect_sizes():
    return [0,-2,0,3,0]

def simulate_LDL_levels(genotypes, standard_deviation=15,randomseed=None):
    if randomseed is None:
        np.random.seed(np.int64(time()))
    else:
        np.random.seed(randomseed)
    #cast to an arary so that this works with list or array input
    genotypes = np.array(genotypes)
    # Simulate disease status for each individual
    m = true_effect_sizes()
    number_of_people, number_of_SNPs = genotypes.shape
    genetic_component = np.dot(genotypes, m)
    environmental_component = np.random.normal(0, standard_deviation, number_of_people)
    LDL_levels = environmental_component + genetic_component + 100
    return np.round(LDL_levels,1)

def create_dataframe(genotypes,LDL_levels):
  columns = [f"SNP {i+1}" for i in range(number_of_SNPs)]
  df = pd.DataFrame(genotypes,columns=columns)
  df["LDL Cholesterol Level (mg/dL)"] = LDL_levels
  df.index.name = 'Patient'
  return df

def line_of_best_fit(x, y):
    '''
    Create a line of best fit for each
    '''
    res = linregress(x, y)
    res = {"effect size (slope)":    np.round(res.slope,3),
           "intercept"  :    np.round(res.intercept,3),
           "p-value"    :    res.pvalue,
           "p-value in scientific notation" :  '{:.2E}'.format(res.pvalue)}
    return res
