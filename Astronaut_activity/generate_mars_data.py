import numpy as np

np.random.seed(42)

outputfile = 'mars_measurements.csv'

n = 128
HR_mean = 55
HR_var  = 5
SV_mean = 130
SV_var  = 10

subject_numbers = np.arange(1,n+1)
HR = np.random.normal(HR_mean, HR_var, size=n)
SV = np.random.normal(SV_mean, SV_var, size=n)

data = np.vstack([subject_numbers, HR, SV]).T
np.savetxt(outputfile, data, delimiter=',')
