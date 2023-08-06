import os
from os.path import join

os.environ['MODULES_PATH'] = join(os.getcwd(), 'soil_app', 'modules')
os.environ['DATA_STRUCTURES_PATH'] = join(os.getcwd(), 'soil_app', 'data_structures')
