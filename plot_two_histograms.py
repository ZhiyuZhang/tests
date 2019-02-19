import matplotlib.pyplot as plt
import astropy.io.ascii
import numpy as np
import os
from matplotlib.ticker import NullFormatter
import matplotlib.style
import matplotlib as mpl
from scipy.optimize      import curve_fit
from astropy.convolution import Gaussian1DKernel, convolve

mpl.style.use('classic')
mpl.rcParams['axes.linewidth'] = 0.5
from matplotlib import rc
rc('font',**{'family':'sans-serif',})
from matplotlib import rcParams
rcParams['font.sans-serif'] = ['Arial']
import matplotlib.pylab as pylab
params = {'legend.fontsize': 12,
         'axes.labelsize'  : 12,
         'axes.titlesize'  : 12,
         'xtick.labelsize' : 12,
         'ytick.labelsize' : 12}

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype']  = 42

pylab.rcParams.update(params)


def gaussian(x,a,x0,sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))



size_mm      = 89# mm
size_inchs   = size_mm * 0.039370078740158 # to inch
size_inchs_H = size_inchs*0.8

nullfmt = NullFormatter()         # no labels
# definitions for the axes
left, width    = 0.1, 0.65
bottom, height = 0.1, 0.65
bottom_h       = left_h    = left + width + 0.02


rect_scatter = [left   , bottom   , width , height]
rect_histx   = [left   , bottom_h , width , 0.2]
rect_histy   = [left_h , bottom   , 0.2   , height]

# start with a rectangular Figure
plt.clf()
plt.figure(1, figsize=(8, 8))

#f, ax1    = plt.subplots(1,figsize = (size_inchs,size_inchs_H))
ax1       = plt.axes(rect_scatter)
axHistx   = plt.axes(rect_histx)
axHisty   = plt.axes(rect_histy)

table    = astropy.io.ascii.read('quality.dat')
index    = table['!index']
allan    = table['Allan_deviation']
rms      = table['Rms_ratio']
goodness = table['goodness']

ax1.scatter(allan, rms, marker='o' , s=2        , color='blue' , label=r'Global ratio or nuclei' , lw=0.5)
ax1.set_xlabel("Allan Deviation")
ax1.set_ylabel("RMS Deviation")


# now determine nice limits by hand:
xbinwidth =  0.05 
xmax      = np.max(np.fabs(allan))
xmin      = np.min(np.fabs(allan))
xlimu     = (int(xmax/xbinwidth) + 1) * xbinwidth
xliml     = (int(xmin/xbinwidth) + 1) * xbinwidth

ybinwidth = 0.01
ymax      = np.max(np.fabs(rms))
ymin      = np.min(np.fabs(rms))
ylimu     = (int(ymax/ybinwidth) + 1) * ybinwidth
yliml     = (int(ymin/ybinwidth) + 1) * ybinwidth

ax1.set_xlim(xliml, xlimu)
ax1.set_ylim(yliml, ylimu) 

cm    = plt.cm.get_cmap('RdYlBu_r')

xbins = np.arange(np.min(allan), np.max(allan), xbinwidth)
ybins = np.arange(np.min(rms),   np.max(rms),   ybinwidth)

axHistx.hist(allan, bins=xbins)
axHistx.set_xlim(xliml, xlimu)




Y,X    = np.histogram(allan, xbins.shape[0])
x_span = X.max()-X.min()
C      = [cm(((x-X.min())/x_span)) for x in X]
axHistx.bar(X[:-1],Y,color=C,width=X[1]-X[0])
print(X[1]-X[0])


p0                   = ([400     , 1.0 , 0.2  ])   # peak , mean , width 
param_bounds         = ([0       , 0.8 , 0  ],
                        [1000    , 1.5 , 1  ])
popt,pcov            = curve_fit(gaussian, X[:15], Y[:15], p0=p0, bounds=param_bounds)
a,b,c                = popt
print(a,b,c)
axHistx.plot(X+(X[1]-X[0])/2, gaussian(X,a,b,c),color='red',linewidth=1.5,label='Individual fit')



axHisty.set_ylim(yliml, ylimu)

Y,X    = np.histogram(rms, ybins.shape[0])
x_span = X.max()-X.min()
C      = [cm(((x-X.min())/x_span)) for x in X]
axHisty.barh(X[:-1],Y,color=C,height=X[1]-X[0])

axHistx.xaxis.tick_top()
axHisty.yaxis.tick_right()

p0                   = ([400     , 1.0 , 0.2  ])   # peak , mean , width 
param_bounds         = ([0       , 0.8 , 0  ],
                        [1000    , 1.5 , 1  ])
popt,pcov            = curve_fit(gaussian, X[:15], Y[:15], p0=p0, bounds=param_bounds)
a,b,c                = popt
print(a,b,c)
axHisty.plot( gaussian(X,a,b,c), X+(X[1]-X[0])/2,color='red',linewidth=1.5,label='Individual fit')


os.system('rm   two_histograms.pdf')
plt.savefig(   'two_histograms.pdf', bbox_inches='tight', pad_inches=0.1)
os.system("open two_histograms.pdf")


