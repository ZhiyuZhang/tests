from   astropy.io import ascii
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
from   astropy.io import fits
import scipy.optimize
from   astropy.modeling import models, fitting
from   scipy.stats import norm



plt.clf()
f, (ax1, ax2, ax3, ax4) = plt.subplots(4, sharex=True, sharey=True)

## load data 
fluxes           = np.loadtxt("fluxes.dat")


# - make statistics p-value test 
scipy.stats.mstats.normaltest(fluxes)

## Following  http://stackoverflow.com/questions/7805552/fitting-a-histogram-with-python  

bins             = np.linspace(0, 1, 40)
n, bins, patches = ax1.hist(fluxes, bins, normed=1, facecolor='green', alpha=0.75)
(mu, sigma)      = norm.fit(fluxes)
y                = mlab.normpdf( bins, mu, sigma)
l                = ax1.plot(bins, y, 'r--', linewidth=2, label='mlab.normpdf')
ax1.legend( loc=7, borderaxespad=0.)

## Make personal  Gaussian fitting 

bins             = np.linspace(0, 1, 40)
(mu, sigma)      = norm.fit(fluxes)
x                = (bins+0.015)[0:(40-1)]
g_init           = models.Gaussian1D(amplitude=1, mean=0.3, stddev=0.1)   ##
fit_g            = fitting.LevMarLSQFitter()
g                = fit_g(g_init, x, n)
n, bins, patches = ax2.hist(fluxes, bins, normed=1, facecolor='green', alpha=0.75)
l                = ax2.plot(bins, g(bins), 'r--', linewidth=2,label='user fitting')
ax2.legend( loc=7, borderaxespad=0.)



## use stats.normalpdf  

bins             = np.linspace(0, 1, 40)
(mu, sigma)      = norm.fit(fluxes)
y                = norm.pdf( bins, mu, sigma)
n, bins, patches = ax3.hist(fluxes, bins, normed=1, facecolor='green', alpha=0.75)
l                = ax3.plot(bins, y, 'r--', linewidth=2, label='stats.norm.pdf')
ax3.legend( loc=7, borderaxespad=0.)



## use stats.normalpdf, after masking the largest value at 1.43 

fluxes           = fluxes[np.where(fluxes < 0.8)] 
bins             = np.linspace(0, 1, 40)
(mu, sigma)      = norm.fit(fluxes)
y                = norm.pdf( bins, mu, sigma)
n, bins, patches = ax4.hist(fluxes, bins, normed=1, facecolor='green', alpha=0.75)
l                = ax4.plot(bins, y, 'r--', linewidth=2, label='stats.norm.pdf-mask')
ax4.legend(loc=7, borderaxespad=0.)


# - make statistics p-value test again to the masked fluxes array
scipy.stats.mstats.normaltest(fluxes)



plt.savefig('test_hist_Gaussian_fit.pdf')



