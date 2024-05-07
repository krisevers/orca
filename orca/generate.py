import json
from typing import List

def generate(rules : List):
    '''
    Generate a Snakefile which runs the workflow. Some default rules are always created as they belong in any simulation based inference project.
    '''

    file = _create_snakefile()

    # 
    default_rules = ['all', 'init', 'simulate', 'train', 'inference', 'analysis']


def _create_snakefile():
    file = open('Snakefile', 'w')
    return file

def _add_rule():
    pass