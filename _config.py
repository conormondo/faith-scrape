import os
from os.path import dirname, join
import sys
import json

config_paths = {
    '_env': join(sys.exec_prefix, dirname(__file__), 'settings.json'),
    '_home': join(os.path.expanduser('~'), dirname(__file__), 'settings.json'),
    '_global': f'/{dirname(__file__)}/settings.json',
    '_default': join(dirname(dirname(os.path.realpath(__file__))), 'settings.json'),
}


def get_configpath() -> str:
    for path in config_paths.keys():
        if os.path.exists(config_paths[path]):
            return config_paths[path]
    return config_paths['_default']


def get_config(runtime=False) -> dict:
    '''Sets up option for future debug running by adding options at runtime'''
    if runtime:
        with open(get_configpath(), 'r') as f:
            return json.load(f)
    else:
        with open(get_configpath(), 'r') as f:
            return json.load(f)


class _Config:
    '''
    Attributes
    -------------
    All properties in the settings.json file pulled in 1:1 except locations.
    Locations return a tuple from the json objects array to make for better url params.
    
    '''
    
    @property
    def API_KEY(self):
        return get_config(True)['API_KEY']
    
    @property
    def GOOGLE_URL(self):
        return get_config(True)['GOOGLE_URL']
    
    @property
    def SEARCH_LOCATIONS(self):
        cords = get_config(True)['SEARCH_LOCATIONS']
        return[(c['lat'], c['lon']) for c in cords]

    @property
    def ZIP_CODES_TO_CHECK(self):
        zips = get_config(True)['ZIP_CODES_TO_CHECK']
        return[str(z) for z in zips]
    
    @property
    def PHRASES(self):
        return get_config(True)['PHRASES']
    
    @property
    def FILTER_TYPE(self):
        return get_config(True)['FILTER_TYPE']
    
    @property
    def FIELDS_TO_USE(self):
        return get_config(True)['FIELDS_TO_USE']
    
    
CONFIG = _Config()