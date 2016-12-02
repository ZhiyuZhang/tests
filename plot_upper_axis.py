import numpy as np
from scipy.constants import *
import matplotlib.pyplot as plt
import sys,os
from   astropy.io import ascii
import astropy.units as u

def ghz_to_um(ghz_value):
     lam = (ghz_value * u.GHz).to(u.um, equivalencies=u.spectral())
     return lam.value

def um_to_ghz(um_value):
     freq = (um_value * u.um).to(u.GHz, equivalencies=u.spectral())
     return freq.value

# -------------------------------------------
# 1). define a plot and setup it to have two axes (twiny)
# -------------------------------------------


fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twiny()

# Add some extra space for the second axis at the bottom
fig.subplots_adjust(bottom=0.2)


# -------------------------------------------
# 2). read data   
# -------------------------------------------

data = ascii.read('data_new.dat')
X = data['col0']
Y = data['col1']



# -------------------------------------------
# 3). plot data with simple X-axis  (in Freq GHz)
# -------------------------------------------

ax1.plot(X,Y)
ax1.set_xlabel(r"Original x-axis: $X$")

# -------------------------------------------
# 4). Calculate the limits of both sides of the X-axis in um, with -5 of the step 
# -------------------------------------------

# from the limits of frequencies, decide how many wavelengths are needed to put in as axis labels  
# Then calculate what are the frequencies corresponding to these labels  

wavelength = np.arange(int(np.max( ghz_to_um(X)  )), int(np.min( ghz_to_um(X)  )),-3)
frequency  = um_to_ghz(wavelength) 


# -------------------------------------------
# 5). Calculate the locations of the new labels corresponding to the limits in relative location (from 0 to 1) 
# -------------------------------------------

new_tick_locations = (frequency - np.min(X) ) / (np.max(X)-np.min(X))

# -------------------------------------------
# 6). define the tick function for converting the values  
# -------------------------------------------

def tick_function(X):
    V = 1 / X  
    return ["%.3f" % z for z in V]

#--------------------------------------------
# 7). Move twinned axis ticks and label from bottom to top 
#--------------------------------------------

ax2.xaxis.set_ticks_position("top")
ax2.xaxis.set_label_position("top")

# Offset the twin axis below the host
ax2.spines["top"].set_position(("axes", 1.))

#--------------------------------------------
# Turn on the frame for the twin axis, but then hide all but the bottom spine
#--------------------------------------------

ax2.set_frame_on(True)
ax2.patch.set_visible(False)
for sp in ax2.spines.values():
    sp.set_visible(False)
ax2.spines["bottom"].set_visible(True)

ax2.set_xticklabels(tick_function(new_tick_locations))
ax2.set_xticks(new_tick_locations)
ax2.set_xticklabels(wavelength.astype(str))
ax2.set_xlabel(r"Modified x-axis: $1/X$")
fig.savefig('plot.pdf')
os.system("open plot.pdf")


