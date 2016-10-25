from   astropy.io import ascii
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
from   astropy.io import fits
import scipy.optimize
from   astropy.modeling import models, fitting
from   scipy.stats import norm


## load data 
fluxes           = np.loadtxt("fluxes.dat")


## Following  http://stackoverflow.com/questions/7805552/fitting-a-histogram-with-python  

bins             = np.linspace(0, 1, 40)
n, bins, patches = plt.hist(fluxes, bins, normed=1, facecolor='green', alpha=0.75)
(mu, sigma)      = norm.fit(fluxes)
y                = mlab.normpdf( bins, mu, sigma)
l                = plt.plot(bins, y, 'r--', linewidth=2)
plt.show()

## Make personal  Gaussian fitting 

bins             = np.linspace(0, 1, 40)
n, bins, patches = plt.hist(fluxes, bins, normed=1, facecolor='green', alpha=0.75)
(mu, sigma)      = norm.fit(fluxes)
x                = (bins+0.015)[0:(40-1)]
g_init           = models.Gaussian1D(amplitude=1, mean=0.3, stddev=0.1)   ##
fit_g            =  fitting.LevMarLSQFitter()
g                =  fit_g(g_init, x, n)
l                = plt.plot(bins, g(bins), 'r--', linewidth=2)
plt.show()


