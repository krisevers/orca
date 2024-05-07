from .core import *
from .model import *
from .prior import *
from .train import *
from .analysis import *
from .generate import *
from .run import *

import os
import json

def init(path : str, name : str):
    '''
    Create a project directory and initialize it with an empty orca.json file.
    '''
    print('Initializing project...')
    if not os.path.exists(path + '/' + name):
        os.makedirs(path + '/' + name)
    
    # Change the current working directory to the project directory
    os.chdir(path + '/' + name)

    # Create an empty orca.json file
    json.dump({}, open('orca.json', 'w'))

def clear(path : str, name : str):
    '''
    Clean up a project directory by removing it
    '''
    pass