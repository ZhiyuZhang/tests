## -- python 3 version 

import os
import numpy as np
def myradex(d,t,n,molecule,redshift):
    if  molecule  ==  "12C16O" or molecule == "12CO" or molecule == '12co':
        moledata = "12C16O_H2.dat"
    elif molecule ==  "13C16O" or molecule == "13CO" or molecule == '13co' :
        moledata = "13C16O_H2.dat"
    elif molecule ==  "12C18O" or molecule == "C18O" or molecule == 'c18o' :
        moledata = "12C18O_H2.dat"
    else:
        print('try other molecules')
    lowfreq           =  40*1e9
    highfreq          =  1500*1e9
    density           =  10**d
    mol_columndensity =  10**n
    temperature       =  10**t
    Tbg               =  2.73*(1+redshift)
    linewidth        =  1.
    f = open('configure.dat','w')
    f.write('  &rdxx_configure'+'\n')
    f.write("   rdxx_cfg%dir_transition_rates = '/data/my_lvg/'"+'\n')
    f.write('   rdxx_cfg%filename_molecule    = '+str(moledata)+'\n')
    f.write("   rdxx_cfg%dir_save             = './'"+'\n')
    f.write("   rdxx_cfg%filename_save        = 'output_mol.dat'"+'\n')
    f.write('   rdxx_cfg%freqmin              = '+str(lowfreq)+'\n')
    f.write('   rdxx_cfg%freqmax              = '+str(highfreq)+'\n')
    f.write('   rdxx_cfg%nTkin                = 1'+'\n')
    f.write('   rdxx_cfg%Tkin                 = '+str(temperature)+'\n')
    f.write('   rdxx_cfg%ndv                  = 1'+'\n')
    f.write('   rdxx_cfg%dv                   = 1D5'+'\n')
    f.write('   rdxx_cfg%nNcol_x              = 1'+'\n')
    f.write('   rdxx_cfg%Ncol_x               = '+str(mol_columndensity)+'\n')
    f.write('   rdxx_cfg%nn_x                 = 1'+'\n')
    f.write('   rdxx_cfg%n_x                  = 1D0 ! Does not matter when there is no continuum opacity.'+'\n')
    f.write('  rdxx_cfg%ndens                = 1  !'+'\n')
    f.write('  rdxx_cfg%n_H2                 = '+str( density)+'\n')
    f.write('  rdxx_cfg%n_HI                 = 0D0'+'\n')
    f.write('  rdxx_cfg%n_oH2                = 0D0 ! If zero, calculate from n_H2 assuming 3:1.'+'\n')
    f.write('  rdxx_cfg%n_pH2                = 0D0'+'\n')
    f.write('  rdxx_cfg%n_Hplus              = 0D0'+'\n')
    f.write('  rdxx_cfg%n_E                  = 0D0'+'\n')
    f.write('  rdxx_cfg%n_He                 = 0D0'+'\n')
    f.write('  rdxx_cfg%opH2eq3              = .false.'+'\n')
    f.write("  rdxx_cfg%geotype              = 'lvg'"+'\n')
    f.write('  rdxx_cfg%Tbg                  = '+str( Tbg)+'\n')
    f.write('  rdxx_cfg%provideLength        = .false.'+'\n')
    f.write('  rdxx_cfg%max_code_run_time    = 5.0 ! Max acceptable code run time (for a single param set) in seconds'+'\n')
    f.write('  rdxx_cfg%max_evol_time        = 1D10 ! Physical evol time in seconds '+'\n')
    f.write('  rdxx_cfg%rtol                 = 1d-7 ! Relative tolerance for the ode solver'+'\n')
    f.write('  rdxx_cfg%atol                 = 1d-20 ! Absolute tolerance for the ode solver'+'\n')
    f.write('  rdxx_cfg%verbose              = .false. ! Whether to print, out the running messages.'+'\n')
    f.write('/'+'\n')
    f.close()
    os.system('a.out')
    ladders  = np.genfromtxt('output_mol.dat', dtype=float,comments='!')
    return  ladders

