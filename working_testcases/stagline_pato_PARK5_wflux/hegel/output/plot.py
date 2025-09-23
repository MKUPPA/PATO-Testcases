import sys
import numpy as np
import matplotlib.pyplot as plt

tw = str(sys.argv[1])


def plot_imp_resid():


    #TimeWindow  Iteration  ResAbs(q)  ResRel(q)  ResDrop(q)  ResAbs(p)  ResAbs(flux_CO)
    #1       1   2.28797195e+06   4.90882215e+00   1.00000000e+00   9.38939602e-01   3.37839635e-13

    filename = '/home/mkuppa/libraries/hegel_git/hegel_27_01_25_wPRECICE/runs/stagline_pato_PARK5/hegel/exec/precice-HEGEL-convergence.log'
    #filename = 'bak_park5/precice-HEGEL-convergence.log'

    X           = np.loadtxt(filename, skiprows=1)[:, 2:]
    label_lst   = ['ResAbs(q)', 'ResRel(q)', 'ResDrop(q)', 'ResAbs(p)', 'ResAbs(flux_CO)']
    
    xaxis = np.arange(1, 1+X.shape[0])

    plt.figure()
    plt.plot(xaxis, X[:, 0], label=f'{label_lst[0]}')
    plt.xlabel('# Iterations')
    plt.ylabel('Residual')
    plt.legend()
    plt.tight_layout()
    plt.savefig('Resid_abs_q.png', bbox_inches='tight', pad_inches=0.1)
    plt.show()

    plt.figure()
    plt.plot(xaxis, X[:, 1], label=f'{label_lst[1]}')
    plt.xlabel('# Iterations')
    plt.ylabel('Residual')
    plt.legend()
    plt.tight_layout()
    plt.savefig('Resid_rel_q.png', bbox_inches='tight', pad_inches=0.1)
    plt.show()

    plt.figure()
    plt.plot(xaxis, X[:, 2], label=f'{label_lst[2]}')
    plt.xlabel('# Iterations')
    plt.ylabel('Residual')
    plt.legend()
    plt.tight_layout()
    plt.savefig('Resid_drop_q.png', bbox_inches='tight', pad_inches=0.1)
    plt.show()

    plt.figure()
    plt.plot(xaxis, X[:, 3], label=f'{label_lst[3]}')
    plt.xlabel('# Iterations')
    plt.ylabel('Residual')
    plt.legend()
    plt.tight_layout()
    plt.savefig('Resid_abs_p.png', bbox_inches='tight', pad_inches=0.1)
    plt.show()

    plt.figure()
    plt.plot(xaxis, X[:, 4], label=f'{label_lst[4]}')
    plt.xlabel('# Iterations')
    plt.ylabel('Residual')
    plt.legend()
    plt.tight_layout()
    plt.savefig('Resid_flux_CO.png', bbox_inches='tight', pad_inches=0.1)
    plt.show()


    return 


def plot_convg():

    X = np.loadtxt('L2_convergence_NS_NLTE.dat')

    plt.figure()
    plt.plot(X[:, 0], X[:, 1], label='L1')
    plt.plot(X[:, 0], X[:, 2], label='L2')
    plt.plot(X[:, 0], X[:, 3], label='L3')
    plt.plot(X[:, 0], X[:, 4], label='L4')
    plt.legend()
    plt.xlabel('No.of iterations')
    plt.tight_layout()
    plt.savefig(f'L2_conv.png', bbox_inches='tight', pad_inches=0.1)
    plt.show()


def plot_flow_field():

    # HEGEL:: NS_NLTE fluid model solution file
    # SI UNITS used: position [m], density [kg/m^3], number density [1/m^3], velocity [m/s], pressure [Pa], energy [J/kg], power [W/m^3], heat-flux [W/m^2], electric field [V/m], magnetic field [T]
    # x  X_em  X_N  X_O  X_C  X_N2  X_NO  X_O2  X_CO  X_CO2  X_CN  X_C2  X_C3  X_N2p  X_NOp  X_Np  X_O2p  X_Op  X_COp  X_CNp  X_Cp  Th  Tve  rho  p  H  Mf  u  v

    labels = ['X_em',  'X_N',  'X_O',  'X_C',  'X_N2',  'X_NO',  'X_O2',  'X_CO',  'X_CO2',  'X_CN',  'X_C2',  'X_C3',  'X_N2p',  'X_NOp',  'X_Np',  'X_O2p',  'X_Op',  'X_COp',  'X_CNp',  'X_Cp']
    
    labels_ion   = ['Ye', 'YN2p', 'YNOp', 'YNp', 'YO2p', 'YOp', 'YCOp', 'YCNp', 'yCp']
    labels_atom  = ['YN', 'YO', 'YC']
    labels_molec = ['YN2', 'YNO', 'YO2', 'YCO', 'YCO2', 'YCN', 'YC2', 'YC3']

    cols_ion   = [1,13,14,15,16,17,18,19,20] 
    cols_atom  = [2,3,4]
    cols_molec = [5,6,7,8,9,10,11,12]

    X = np.loadtxt('flowfield_NS_NLTE.dat')

    plt.figure()
    plt.plot(X[:, 0], X[:, -7], label='Tve')
    plt.plot(X[:, 0], X[:, -8], label='T')
    plt.legend()
    plt.xlabel('x')
    plt.tight_layout()
    plt.savefig(f'stag_T_{tw}.png', bbox_inches='tight', pad_inches=0.1)
    plt.show()

    plt.figure()
    plt.plot(X[:, 0], X[:, -5], label='p')
    plt.legend()
    plt.xlabel('x')
    plt.tight_layout()
    plt.savefig(f'stag_p_{tw}.png', bbox_inches='tight', pad_inches=0.1)
    plt.show()
    

    ion_ind = []
    ion_lab = []

    plt.figure()
    c=0
    for i in cols_ion:

        plt.plot(X[:, 0], X[:, i], label=f'{labels_ion[c]}')

        if np.max(X[:, i]) > 1e-6:
            ion_ind.append(i)
            ion_lab.append(c)

        c=c+1


    plt.legend()
    plt.xlabel('x')
    plt.ylabel('Mole fraction')
    plt.yscale('log')
    plt.ylim([1e-6, 1])
    plt.tight_layout()
    plt.savefig(f'stag_ion_{tw}.png', bbox_inches='tight', pad_inches=0.1)
    plt.show()

    atom_ind = []
    atom_lab = []

    plt.figure()
    c=0
    for i in cols_atom:
        
        plt.plot(X[:, 0], X[:, i], label=f'{labels_atom[c]}')
        
        if np.max(X[:, i]) > 1e-6:
            atom_ind.append(i)
            atom_lab.append(c)

        c=c+1

    plt.legend()
    plt.xlabel('x')
    plt.ylabel('Mole fraction')
    plt.yscale('log')
    plt.ylim([1e-6, 1])
    plt.tight_layout()
    plt.savefig(f'stag_atom_{tw}.png', bbox_inches='tight', pad_inches=0.1)
    plt.show()

    molec_ind = []
    molec_lab = []

    plt.figure()
    c=0
    for i in cols_molec:

        plt.plot(X[:, 0], X[:, i], label=f'{labels_molec[c]}')

        if np.max(X[:, i]) > 1e-6:
            molec_ind.append(i)
            molec_lab.append(c)

        c=c+1

    plt.legend()
    plt.xlabel('x')
    plt.ylabel('Mole fraction')
    plt.yscale('log')
    plt.ylim([1e-6, 1])
    plt.tight_layout()
    plt.savefig(f'stag_molec_{tw}.png', bbox_inches='tight', pad_inches=0.1)
    plt.show()

    plt.figure()
    for i in range(len(ion_ind)):

        plt.plot(X[:, 0], X[:, ion_ind[i]], label=f'{labels_ion[ion_lab[i]]}')


    for i in range(len(atom_ind)):

        plt.plot(X[:, 0], X[:, atom_ind[i]], label=f'{labels_atom[atom_lab[i]]}')

    for i in range(len(molec_ind)):

        plt.plot(X[:, 0], X[:, molec_ind[i]], label=f'{labels_molec[molec_lab[i]]}')


    plt.legend()
    plt.xlabel('x')
    plt.ylabel('Mole fraction')
    plt.yscale('log')
    plt.ylim([1e-6, 1])
    plt.tight_layout()
    plt.savefig(f'stag_sp_{tw}.png', bbox_inches='tight', pad_inches=0.1)
    plt.show()


    return


def plot_wpoint():

    # Time  Coordinate0  Coordinate1  T  q  mdot0  mdot1  p  y_em  y_N  y_O  y_C  y_N2  y_NO  y_O2  y_CO  y_CO2  y_CN  y_C2  y_C3  y_N2p  y_NOp  y_Np  y_O2p  y_Op  y_COp  y_CNp  y_Cp  flux_em  flux_N  flux_O  flux_C  flux_N2  flux_NO  flux_O2  flux_CO  flux_CO2  flux_CN  flux_C2  flux_C3  flux_N2p  flux_NOp  flux_Np  flux_O2p  flux_Op  flux_COp  flux_CNp  flux_Cp
    
    file = '/home/mkuppa/libraries/hegel_git/hegel_27_01_25_wPRECICE/runs/stagline_pato_PARK5/hegel/exec/precice-SolidSolver-watchpoint-stagnation-point.log'
    #file = 'bak_park5/precice-SolidSolver-watchpoint-stagnation-point.log'
    
    labels=['T', 'q', 'mdot0', 'mdot1', 'p']
    
    cols_ion   = [8, 20, 21, 22, 23, 24, 25, 26, 27]
    labels_ion = ['Ye', 'YN2p', 'YNOp', 'YNp', 'YO2p', 'YOp', 'YCOp', 'YCNp', 'yCp']

    cols_atom   = [9, 10, 11]
    labels_atom = ['YN', 'YO', 'YC']

    cols_molec   = [12, 13, 14, 15, 16, 17, 18, 19]
    labels_molec = ['YN2', 'YNO', 'YO2', 'YCO', 'YCO2', 'YCN', 'YC2', 'YC3']

    cols_ionf   = [28, 40, 41, 42, 43, 44, 45, 46, 47]
    labels_ionf = ['Ye', 'YN2p', 'YNOp', 'YNp', 'YO2p', 'YOp', 'YCOp', 'YCNp', 'yCp']

    cols_atomf   = [29, 30, 31]
    labels_atomf = ['YN', 'YO', 'YC']

    cols_molecf   = [32, 33, 34, 35, 36, 37, 38, 39]
    labels_molecf = ['YN2', 'YNO', 'YO2', 'YCO', 'YCO2', 'YCN', 'YC2', 'YC3']


    X = np.loadtxt(file, skiprows=1)

    for i in range(5):
        plt.figure()
        plt.plot(X[:, 0], X[:, 3+i], '.-', label=f'{labels[i]}')

        if i == 0:
            sig  = 5.67e-8
            em   = 0.9
            Trad = (X[:, 4]/(em*sig))**(0.25)
            plt.plot(X[:, 0], Trad, '.-', label='T rad eqb')

        plt.legend()
        plt.xlabel('Time')
        if i == 1:
            plt.yscale('log')
        plt.tight_layout()
        plt.savefig(f'watchpoint_{labels[i]}.png', bbox_inches='tight', pad_inches=0.1)
        plt.show()


    # ion mass fractions
    plt.figure()
    c=0
    for i in cols_ion:

        plt.plot(X[:, 0], X[:, i], '.-', label=f'{labels_ion[c]}')
        c=c+1

    plt.legend()
    plt.yscale('log')
    plt.xlabel('Time')
    plt.ylabel('Mass fraction')
    plt.ylim([1e-7, 1])
    plt.tight_layout()
    plt.savefig(f'watchpoint_ionY.png', bbox_inches='tight', pad_inches=0.1)
    plt.show()

    # atomic mass fractions
    plt.figure()
    c=0
    for i in cols_atom:
        plt.plot(X[:, 0], X[:, i], '.-', label=f'{labels_atom[c]}')
        c=c+1

    plt.legend()
    plt.yscale('log')
    plt.xlabel('Time')
    plt.ylim([1e-7, 1])
    plt.ylabel('Mass fraction')
    plt.tight_layout()
    plt.savefig(f'watchpoint_atomY.png', bbox_inches='tight', pad_inches=0.1)
    plt.show()

    # molecular mass fractions
    plt.figure()
    c=0
    for i in cols_molec:
        plt.plot(X[:, 0], X[:, i], '.-', label=f'{labels_molec[c]}')
        c=c+1

    plt.legend()
    plt.yscale('log')
    plt.xlabel('Time')
    plt.ylim([1e-7, 1])
    plt.ylabel('Mass fraction')
    plt.tight_layout()
    plt.savefig(f'watchpoint_molecY.png', bbox_inches='tight', pad_inches=0.1)
    plt.show()

    # ion mass flux
    plt.figure()
    c=0
    for i in cols_ionf:
        plt.plot(X[:, 0], X[:, i], '.-', label=f'{labels_ionf[c]}')
        c=c+1

    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Mass flux')
    plt.ylim([-1e-8, 1e-8])
    plt.tight_layout()
    plt.savefig(f'watchpoint_ionMF.png', bbox_inches='tight', pad_inches=0.1)
    plt.show()

    # atomic mass flux
    plt.figure()
    c=0
    for i in cols_atomf:
        plt.plot(X[:, 0], X[:, i], '.-', label=f'{labels_atomf[c]}')
        c=c+1

    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Mass flux')
    plt.ylim([-0.01, 0.01])
    plt.tight_layout()
    plt.savefig(f'watchpoint_atomMF.png', bbox_inches='tight', pad_inches=0.1)
    plt.show()

    # molecular mass flux
    plt.figure()
    c=0
    for i in cols_molecf:
        plt.plot(X[:, 0], X[:, i], '.-', label=f'{labels_molecf[c]}')
        c=c+1

    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Mass flux')
    plt.ylim([-0.01, 0.01])
    plt.tight_layout()
    plt.savefig(f'watchpoint_molecMF.png', bbox_inches='tight', pad_inches=0.1)
    plt.show()

    return 

plot_imp_resid()
plot_convg()
plot_wpoint()
plot_flow_field()
