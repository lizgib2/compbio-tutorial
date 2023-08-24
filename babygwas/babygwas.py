# students have to fill in a dataframe of class genotypes and phenotypes
import numpy as np
import numpy.random as npr
from scipy.stats import linregress
import pandas as pd
import matplotlib.pyplot as plt
​
def simulate_genotypes(N, L):
    # Function to simulate genotypes
    ps = npr.beta(4, 4, size=L)
    G = np.empty((N, L), dtype=int)
​
    for i in range(L):
        gen = npr.binomial(2, ps[i], size=N)
        G[:, i] = gen
​
    return G
​
def simulate_disease(G, beta, epsilon):
    # Simulate disease status for each individual
    G = (G - G.mean(axis=1, keepdims=True)) / G.std(axis=1, keepdims=True)
    N, L = G.shape
    genetic_component = np.dot(G, beta)
    D = np.random.normal(0, np.sqrt(epsilon), N) + genetic_component
    D = np.where(D > 0.5, 1, 0)
    return D
​
def generate_beta(L, non_zero_effect_size=0.5):
    # Generate a beta vector with zeros everywhere apart from three fixed loci
    beta = np.zeros(L)
    fixed_indices = [0, 5, 7]
    beta[fixed_indices] = [7,4,4]
    return beta
​
# the code Liz wrote
def linear_regression(x,y):
    '''
    A simple linear regression of your genotype (x)
    versus your trait status (y)
    '''
    res = linregress(x,y)
    return res.slope,res.intercept,res.pvalue
​
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
