import json

def append(name : str, call : str = None, **kwargs):
    print('Appending model...')
    
    try:
        config = json.load(open('orca.json'))
    except:
        raise ValueError('No orca.json file found. Please run orca.init() first.')

    if 'models' not in config:
        config['models'] = {}

    if name not in config['models']:
        config['models'][name] = {}
    else:
        raise ValueError('Model name already exists. Please use a different name.')

    if call is not None:
        config['models'][name]['call'] = call
    else:
        raise ValueError('Model should have a call description. Make sure the call takes and produces compatible inputs and outputs.')


    for key, value in kwargs.items():
        config['models'][name][key] = value

    json.dump(config, open('orca.json', 'w'))

def chain(source : str, target : str):
    '''
    Chain source and target model together such that the source output is the target input.
    '''
    pass