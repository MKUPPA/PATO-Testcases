import numpy as np
import matplotlib.pyplot as plt

def plot_convg():

    X = np.loadtxt('L2_convergence_NS.dat')

    plt.figure()
    plt.plot(X[:, 0], X[:, 1], label='L1')
    plt.plot(X[:, 0], X[:, 2], label='L2')
    plt.plot(X[:, 0], X[:, 3], label='L3')
    plt.plot(X[:, 0], X[:, 4], label='L4')
    plt.legend()
    plt.show()


def plot_flow_field():

    # HEGEL:: NS fluid model solution file
    # SI UNITS used: position [m], density [kg/m^3], number density [1/m^3], velocity [m/s], pressure [Pa], energy [J/kg], power [W/m^3], heat-flux [W/m^2], electric field [V/m], magnetic field [T]
    # x  rho  p  T  H  M  u  v

    X = np.loadtxt('flowfield_NS.dat')

    plt.figure()
    plt.plot(X[:, 0], X[:, -5], label='T')
    plt.legend()
    plt.tight_layout()
    plt.show()

    return

plot_convg()
plot_flow_field()
