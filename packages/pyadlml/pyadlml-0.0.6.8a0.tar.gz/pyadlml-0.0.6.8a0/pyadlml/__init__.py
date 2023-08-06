import os

#from pyadlml.dataset.io import DATA_HOME_FOLDER_NAME, set_data_home
import pyadlml.dataset as dataset
from pyadlml.util import (
    ENV_PARALLEL,
    set_primary_color,
    set_diverging_color,
    set_secondary_color,
    set_sequential_color
)
# set data home folder to the current working directory
DATA_HOME_FOLDER_NAME = 'pyadlml_data_home'
DATA_HOME = [os.path.join(os.getcwd(),DATA_HOME_FOLDER_NAME)]

# default for parallel execution
os.environ[ENV_PARALLEL] = str(False)

set_primary_color('#2c3e50')
set_secondary_color('#e34d30')
set_diverging_color('RdBu') # RdGy
set_sequential_color('viridis') #BrwnYI, BurgYI, Burg