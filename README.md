# orca
Orca provides tools for sequentially running generative models to obtain a well organized dataset of parameters and their associated observables from model simulations.

When appending your models a file is generated: `orca.json`. This file contains all information about the full generative process, i.e. which models are going to be executed and how they should be called. To run the models in sequence, sample from the predefined prior (`prior.json`) and receive the simulation results (simulation output `psi` and parameters `theta`) use the `O.run(prior.json)` function call. 

## Applications
* Biophysical modelling where multiple layers of generative and observational models are required.
* Inference and analysis of relationships between model parameters and observables (Simulation Based Inference).

## Installation
To install the required dependencies, you can use the `requirements.txt` file provided in the repository. Run the following command:

```sh
pip install -r requirements.txt
```

## Usage

A simple working example is given with a simple lorenz system connected to a observation model which computes the cross correlation between the simulated variables.

A prior file can be create by running

```python
from orca import prior

set_prior('prior.json', 'Lorenz', 'sigma', 'uniform', low=0, high=20)
set_prior('prior.json', 'Lorenz', 'rho',   'uniform', low=0, high=50)
set_prior('prior.json', 'Lorenz', 'beta',  'uniform', low=0, high=10)
```

The orca class can be called and models can be appended and run. The following shows a simple workflow for loading models, appending them to the `orca` object and running using the prior file created above.

```python
from orca import Orca

from examples.lorenz import Lorenz, CrossCorr

# create the orca object
O = Orca(num_simulations=100)

# create the model objects (these should have a call function)
L = Lorenz()
C = CrossCorr()

# Append the models to the orca object in the right order (such that output of L is the input of C)
O.append(L)
O.append(C)

# run the simulations
psi, theta = O.run('prior.json')

# print a summary of the orca object
O()
```