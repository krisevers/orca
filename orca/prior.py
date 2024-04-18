import json
import numpy as np
import pylab as plt

"""
Tools for creating and reading prior files and visualizing the prior distributions
"""

def set_prior(file, object : str, parameter : str, distribution : str, *args, **kwargs):
    """
    Generate or append to the theta dictionary
    """
    try:
        prior = json.load(open(file))
    except:
        prior = {}
    if object not in prior:
        prior[object] = {}
    if distribution not in prior[object]:
        prior[object][parameter] = {}

    if distribution == 'uniform':
        prior[object][parameter]['low'] = kwargs['low']
        prior[object][parameter]['high'] = kwargs['high']
        prior[object][parameter]['distribution'] = distribution
    elif distribution == 'normal':
        prior[object][parameter]['mean'] = kwargs['mean']
        prior[object][parameter]['std'] = kwargs['std']
        prior[object][parameter]['distribution'] = distribution

    json.dump(prior, open(file, 'w'))

def sample(file, num_samples : int):
    """
    Sample from the prior distributions

    Parameters
    ----------
    file : str
        Path to the prior file
    num_samples : int
        Number of samples to generate

    Returns
    -------
    dict
        Dictionary of samples
    """
    prior = json.load(open(file))
    samples = {}
    for object in prior:
        samples[object] = {}
        for parameter in prior[object]:
            if prior[object][parameter]['distribution'] == 'uniform':
                samples[object][parameter] = np.random.uniform(prior[object][parameter]['low'], prior[object][parameter]['high'], num_samples)
            elif prior[object][parameter]['distribution'] == 'normal':
                samples[object][parameter] = np.random.normal(prior[object][parameter]['mean'], prior[object][parameter]['std'], num_samples)
    return samples

def plot(file):

    prior = json.load(open(file))
    for object in prior:
        for parameter in prior[object]:
            if prior[object][parameter]['distribution'] == 'uniform':
                x = np.linspace(prior[object][parameter]['low'], prior[object][parameter]['high'], 100)
                y = np.ones(100) / (prior[object][parameter]['high'] - prior[object][parameter]['low'])
                plt.plot(x, y, label=f'{object}.{parameter}')
            elif prior[object][parameter]['distribution'] == 'normal':
                x = np.linspace(prior[object][parameter]['mean'] - 3 * prior[object][parameter]['std'], prior[object][parameter]['mean'] + 3 * prior[object][parameter]['std'], 100)
                y = 1 / (prior[object][parameter]['std'] * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - prior[object][parameter]['mean']) / prior[object][parameter]['std'])**2)
                plt.plot(x, y, label=f'{object}.{parameter}')
    plt.legend()
    plt.show()