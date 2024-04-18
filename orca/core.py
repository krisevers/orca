# -*- coding: utf-8 -*-
from . import utils
from . import prior

import numpy as np
import json

# from mpi4py import MPI

class Orca:
    def __init__(self, num_simulations=1, num_threads=1, prior=None, verbose=False):
        self.num_simulations    = num_simulations
        self.num_threads        = num_threads
        self.prior              = prior
        self.verbose            = verbose

        self.F = []             # list of objects
        self.theta = None       # theta parameters
        self.psi = None         # psi observables

    """
    Base class for orca. Objects and callables can be appended to the orca object and run in sequence to obtain a theta-psi pair.
    Parameters are passed to the objects and callables depending on the object's signature.
    """

    def __call__(self, ):
        """
        Provide a summary of the components of the orca object
        """

        print('--------------------------------------------------')
        print('____________________ORCA SUMMARY__________________')
        print('--------------------------------------------------')
        print(' ')
        print('                     Components:                  ')
        print('theta -> \n\t', ''.join([f.__class__.__name__ + ' -> ' for f in self.F]), '\n-> psi')
        print(' ')
        print('Number of simulations: \t', self.num_simulations)
        print('Number of threads: \t', self.num_threads)
        print(' ')
        print('--------------------------------------------------')
        print(' ')

    def append(self, object, name=None):
        """
        Append a model to orca object
        """
        if name is not None:
            setattr(object, '__name__', name)
        self.F.append(object)

    def run(self, prior_file : str = None):

        # load theta file
        if prior_file is not None:
            self.prior = json.load(open(prior_file))

        # check if prior exists
        if self.prior is None and prior_file is None:
            raise ValueError('Prior not set and no prior file provided.')
        elif self.prior is None and prior_file is not None:
            self.prior = json.load(open(prior_file))

        # assign theta to the objects
        self.gen_theta()

        # check compatibility
        if not self._check_compatibility():
            raise ValueError('Incompatibility detected between objects. Please check the compatibility of the input and output types and shapes.')

        # run the orca object
        self.simulate(verbose=self.verbose)

        return self.psi, self.theta
    
    def set_prior(self, file, object : str, parameter : str, distribution : str, *args, **kwargs):
        """
        Generate or append to the theta dictionary
        """
        try:
            self.prior = json.load(open(file))
        except:
            self.prior = {}
        if object not in self.prior:
            self.prior[object] = {}
        if distribution not in self.prior[object]:
            self.prior[object][parameter] = {}

        if distribution == 'uniform':
            self.prior[object][parameter]['low'] = kwargs['low']
            self.prior[object][parameter]['high'] = kwargs['high']
            self.prior[object][parameter]['distribution'] = distribution
        elif distribution == 'normal':
            self.prior[object][parameter]['mean'] = kwargs['mean']
            self.prior[object][parameter]['std'] = kwargs['std']
            self.prior[object][parameter]['distribution'] = distribution

        json.dump(self.prior, open(file, 'w'))

    def gen_theta(self):
        """
        Generate and assign theta parameters to the objects
        """
        self.theta = np.empty(self.num_simulations, dtype=dict)

        theta_temp = {}
        for f in self.F:
            object = f.__class__.__name__
            if object in self.prior:
                if object not in theta_temp:
                    theta_temp[object] = {}
                for key in self.prior[object]:
                    theta_temp[object][key] = utils.sample(self.num_simulations, **self.prior[object][key])

        for s in range(self.num_simulations):
            self.theta[s] = {}
            for object in theta_temp:
                self.theta[s][object] = {}
                for key in theta_temp[object]:
                    self.theta[s][object][key] = theta_temp[object][key][s]

    def set_theta(self, s, f):
        """
        Set theta parameters to the object

        Parameters
        ----------
        s : int
            Index of the simulation
        f : object
            Object to set the parameters to
        """
        object = f.__class__.__name__
        if object not in self.theta:
            pass
        else:
            for key in self.theta[object]:
                setattr(f, key, self.theta[s][object][key])

    def simulate(self, verbose=False):

        self.psi = np.empty(self.num_simulations, dtype=dict)

        for s in range(self.num_simulations):
            self.psi[s] = {}
            for i, f in enumerate(self.F):
                self.set_theta(s, f)
                if i == 0:
                    self.psi[s][f.__class__.__name__] = f()
                else:
                    self.psi[s][f.__class__.__name__] = f(self.psi[s][self.F[i-1].__class__.__name__])

                if verbose:
                    print('Simulation {}/{}'.format(s+1, self.num_simulations), end='\r')


    def _check_compatibility(self):
        """
        Run one simulation to check the compatibility of the input and output types and shapes.
        """
        psi_test = {}
        for i, f in enumerate(self.F):
            try:
                self.set_theta(0, f)
                if i == 0:
                    psi_test[f.__class__.__name__] = f()
                else:
                    psi_test[f.__class__.__name__] = f(psi_test[self.F[i-1].__class__.__name__])
                    # print('Compatibility check passed between', self.F[i-1].__class__.__name__, 'and', f.__class__.__name__, ' : ', type(psi_test[self.F[i-1].__class__.__name__]), psi_test[self.F[i-1].__class__.__name__].shape)
            except:
                return False
            
        return True