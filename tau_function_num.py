# Derive the optical depth of HCO+, using HCO+/H13CO+ line ratios, under LTE condition. 

import numpy as np
import os
import scipy.constants as const
from scipy.optimize import fsolve

#setting plot parameters:
import matplotlib.pyplot as plt
import matplotlib.style
import matplotlib as mpl
mpl.style.use('classic')

#import montage_wrapper as montage

plt.rc('font', family='serif')
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.rc('font', size=10)
plt.rc('text', usetex=True)
fig_height  = 3.46456693        # width in inches
fig_width   = fig_height        # height in inches


freq_h13cop     = 86754.288E6 # Hz
freq_hcop       = 89188.526E6 # Hz
Tex             = 10.0        # K
abundance_ratio = 54.26       # 12C/13C ratio
redshift        = 0
Ta_ratio        = 10
input_data      = (Tex, abundance_ratio,redshift,Ta_ratio)

def term(freq,Tex,redshift):
    Tbg   = 2.73 * (redshift+1)
    term1 = (np.exp(const.h*freq/(const.k*Tex)))**(-1)
    term2 = (np.exp(const.h*freq/(const.k*Tbg)))**(-1)
    term  = const.h*freq/const.k * (term1 -term2)
    return term


def line_ratio(tau,*input_data):
    Tex,abundancer_ratio,redshift,Ta_ratio = input_data
    A           = abundance_ratio
    Term_hcop   = term(freq_hcop,Tex,redshift)
    Term_h13cop = term(freq_h13cop,Tex,redshift)
    C           = Term_hcop /Term_h13cop
    return (1-np.exp(-tau))/ (1- np.exp(-tau/A)) *C - Ta_ratio

# ---trying to know how to solve the equation without numerical issues.

Guessvalue = 0.1
tau        = fsolve(line_ratio, Guessvalue, args=(Tex, abundance_ratio,redshift,Ta_ratio))


plt.clf()
fig, ax1 = plt.subplots(figsize= (fig_width, fig_height))
for TaRatio in range(2, 100, 1):
    TaRatio = TaRatio *0.5
    tau   = fsolve(line_ratio, Guessvalue, args=(Tex, abundance_ratio,redshift,TaRatio))
    ax1.plot(TaRatio, tau,marker = 'x', linestyle='None')

ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_ylabel('tau')
ax1.set_xlabel('ratio')
fig.savefig('tau_function_num.pdf',bbox_inches='tight', dpi=300)

