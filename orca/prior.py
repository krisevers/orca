import json
import numpy as np
import pylab as plt

"""
Tools for creating and reading prior files and visualizing the prior distributions
"""

def prior(model : str, parameter : str, distribution : str, *args, **kwargs):
    """
    Generate or append to the theta dictionary
    """
    print('Appending prior...')
    try:
        prior = json.load(open('prior.json'))
    except:
        prior = {}
    if model not in prior:
        prior[model] = {}
    if distribution not in prior[model]:
        prior[model][parameter] = {}

    if distribution == 'uniform':
        prior[model][parameter]['low'] = kwargs['low']
        prior[model][parameter]['high'] = kwargs['high']
        prior[model][parameter]['distribution'] = distribution
    elif distribution == 'normal':
        prior[model][parameter]['mean'] = kwargs['mean']
        prior[model][parameter]['std'] = kwargs['std']
        prior[model][parameter]['distribution'] = distribution

    json.dump(prior, open('prior.json', 'w'))

def sample_prior(num_samples : int):
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
    prior = json.load(open('prior.json'))
    samples = {}
    for model in prior:
        samples[model] = {}
        for parameter in prior[model]:
            if prior[model][parameter]['distribution'] == 'uniform':
                samples[model][parameter] = np.random.uniform(prior[model][parameter]['low'], prior[model][parameter]['high'], num_samples)
            elif prior[model][parameter]['distribution'] == 'normal':
                samples[model][parameter] = np.random.normal(prior[model][parameter]['mean'], prior[model][parameter]['std'], num_samples)
    return samples

def plot_prior(file):

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