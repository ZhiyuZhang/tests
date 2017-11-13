## -- python 3 version 

import os
import numpy as np
def radex(d,t,n,molecule,redshift):
    if  molecule  ==  "12C16O" or molecule == "12CO" or molecule == '12co':
        moledata = "co.dat"
    elif molecule ==  "13C16O" or molecule == "13CO" or molecule == '13co' :
        moledata = "13co.dat"
    elif molecule ==  "12C18O" or molecule == "C18O" or molecule == 'c18o' :
        moledata = "c18o.dat"
    else:
        print('try other molecules')
    lowfreq           =  40
    highfreq          =  1500
    density           =  10**d
    mol_columndensity =  10**n
    temperature       =  10**t
    Tbg               =  2.73*(1+redshift)
    linewidth        =  1.
    f = open('configure.dat','w')
    f.write(  str(moledata)+'\n')
    f.write( 'output_mol.dat'+'\n')
    f.write(str(lowfreq) + " " + str(highfreq)+'\n')
    f.write(str(temperature)+'\n')
    f.write('1' +'\n')
    f.write('H2'+'\n')
    f.write(str( density)+'\n')
    f.write(str( Tbg)+'\n')
    f.write(str(mol_columndensity)+'\n')
    f.write(str(linewidth)+'\n')
    f.write('0'+'\n')
    f.close()
    os.system('radex < configure.dat ')
    ladders  = np.genfromtxt('output_mol.dat', dtype=float,comments='!',skip_header=13)
    return  ladders

