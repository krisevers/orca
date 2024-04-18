import numpy as np

def sample(num_samples, *args, **kwargs):
    """
    Sample from a distribution
    """
    if kwargs['distribution'] == 'uniform':
        return np.random.uniform(low=kwargs['low'], high=kwargs['high'], size=num_samples)
    elif kwargs['distribution'] == 'normal':
        return np.random.normal(loc=kwargs['mean'], scale=kwargs['std'], size=num_samples)