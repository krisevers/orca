import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from orca import prior

prior.set_prior('examples/prior.json', 'Lorenz', 'sigma', 'normal', mean=10, std=2)
prior.set_prior('examples/prior.json', 'Lorenz', 'rho',   'normal', mean=28, std=4)
prior.set_prior('examples/prior.json', 'Lorenz', 'beta',  'normal', mean=2, std=0.5)

x = prior.sample('examples/prior.json', 10)

prior.plot('examples/prior.json')