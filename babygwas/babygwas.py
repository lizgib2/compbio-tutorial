# students have to fill in a dataframe of class genotypes and phenotypes
import numpy as np
import numpy.random as npr
from scipy.stats import linregress
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

number_of_SNPs = 5

def simulate_genotypes(number_of_people):
    # Function to simulate genotypes
    probabilities = npr.beta(4, 4, size=number_of_SNPs)
    genotypes = np.empty((number_of_people, number_of_SNPs), dtype=int)

    for i in range(number_of_SNPs):
        genotypes[:, i] = npr.binomial(2, probabilities[i], size=number_of_people)

    return genotypes

def true_effect_sizes(non_zero_effect_size=0.5):
    # Generate a beta vector with zeros everywhere apart from three fixed loci
    m = np.zeros(number_of_SNPs)
    fixed_indices = [0,1,4]
    m[fixed_indices] = [-5,7,-4]
    return m

def simulate_LDL_levels(genotypes, standard_deviation=12):
    # Simulate disease status for each individual
    m = true_effect_sizes()
    normalized_genotypes = (genotypes - genotypes.mean(axis=1, keepdims=True)) / genotypes.std(axis=1, keepdims=True)
    number_of_people, number_of_SNPs = normalized_genotypes.shape
    genetic_component = np.dot(normalized_genotypes, m)
    random_component = np.random.normal(0, standard_deviation, number_of_people)
    LDL_levels = random_component + genetic_component + 125
    return LDL_levels

def create_dataframe(genotypes,LDL_levels):
  columns = [f"SNP {i+1}" for i in range(number_of_SNPs)]
  df = pd.DataFrame(genotypes,columns=columns)
  df["LDL Cholesetrol Level"] = LDL_levels
  return df

def linear_regression(x,y):
    '''
    A simple linear regression of your genotype (x)
    versus your trait status (y)
    '''
    res = linregress(x,y)
    return res.slope,res.intercept,res.pvalue

def gwas(genotypes, phenotypes):
    '''
    Conduct SNPwise regressions to get your GWAS values
    '''
    sumstats = dict()
    sumstats['snp'] = []
    sumstats['effect'] = []
    sumstats['intercept'] = []
    sumstats['pvalue'] = []
    # transpose the genotypes matrix to be SNPs X individuals
    genotypes_t = np.transpose(genotypes)
    i = 0
    # run GWAS per snp
    for x in genotypes_t:
        gwas_res = linear_regression(x, phenotypes)
        sumstats['snp'].append(i)
        sumstats['effect'].append(gwas_res[0])
        sumstats['intercept'].append(gwas_res[1])
        sumstats['pvalue'].append(gwas_res[2])
        i += 1
    return(sumstats)
