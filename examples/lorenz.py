import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from orca import Orca, utils

"""
Test model for orca.
"""

class Lorenz:
    def __init__(self):
        self.dt = 0.01
        self.sigma = 10
        self.rho = 28
        self.beta = 8/3
        self.state = np.random.randn(3)
        self.time = 0
        self.t_sim = 10

    def __call__(self):
        """run simulation for the set amount of time"""
        t_steps = int(self.t_sim / self.dt)
        states = np.zeros((t_steps, 3))
        for i in range(t_steps):
            states[i] = self.step()

        return states


    def step(self):
        x, y, z = self.state
        dx = self.sigma * (y - x)
        dy = x * (self.rho - z) - y
        dz = x * y - self.beta * z
        self.state += np.array([dx, dy, dz]) * self.dt
        self.time += self.dt
        return self.state

    def reset(self):
        self.state = np.random.randn(3)
        self.time = 0
        return self.state

    def get_state(self):
        return self.state

    def get_time(self):
        return self.time

    def set_state(self, state):
        self.state = state

    def set_time(self, time):
        self.time = time

class CrossCorr:
    def __init__(self):
        pass

    def __call__(self, states):
        return self.get_summary(states)


    def get_summary(self, states):

        # cross correlation
        x, y, z = states.T
        x = x - np.mean(x)
        y = y - np.mean(y)
        z = z - np.mean(z)
        x = x / np.std(x)
        y = y / np.std(y)
        z = z / np.std(z)
        cxy = np.correlate(x, y, mode='full')
        cyz = np.correlate(y, z, mode='full')
        czx = np.correlate(z, x, mode='full')
        cxy = cxy / np.max(cxy)
        cyz = cyz / np.max(cyz)
        czx = czx / np.max(czx)

        return np.concatenate([cxy, cyz, czx])


if __name__=='__main__':

    import numpy as np
    import pylab as plt

    O = Orca(num_simulations=1000, num_threads=1, verbose=True)

    # create lorenz object
    L = Lorenz()
    C = CrossCorr()

    O.append(L)
    O.append(C, 'statistics')    # if you want to save the output of the function, you need to specify the name of the output

    O.set_prior('examples/prior.json', 'Lorenz', 'sigma', 'uniform', low=0, high=20)
    O.set_prior('examples/prior.json', 'Lorenz', 'rho',   'uniform', low=0, high=50)
    O.set_prior('examples/prior.json', 'Lorenz', 'beta',  'uniform', low=0, high=10)

    # Run the orca object
    psi, theta = O.run('examples/prior.json')


    O() # Show summary of the orca object

    # Post-process the results
    means = np.array([np.mean(psi[s]['CrossCorr']) for s in range(O.num_simulations)])
    std   = np.array([np.std(psi[s]['CrossCorr']) for s in range(O.num_simulations)])

    sigma = np.array([theta[s]['Lorenz']['sigma'] for s in range(O.num_simulations)])
    rho   = np.array([theta[s]['Lorenz']['rho'] for s in range(O.num_simulations)])
    beta  = np.array([theta[s]['Lorenz']['beta'] for s in range(O.num_simulations)])

    plt.figure()
    plt.plot(sigma, means, 'o')
    plt.xlabel('sigma')
    plt.ylabel('CrossCorr')
    plt.show()