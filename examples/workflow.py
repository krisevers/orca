import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import orca 

PATH = 'examples'
NAME = 'lorenz'

orca.init(PATH, NAME)

# Append models to the 
orca.append(name='Lorenz',      call='python -c "import lorenz; L = lorenz(); L()', description='Lorenz attractor simulation')

orca.prior(model='Lorenz', parameter='sigma', distribution='uniform', low=0, high=50)
orca.prior(model='Lorenz', parameter='rho',   distribution='uniform', low=0, high=50)
orca.prior(model='Lorenz', parameter='beta',  distribution='uniform', low=0, high=50)

samples = orca.sample_prior(num_samples=1000)

import IPython; IPython.embed()