# custom modules
import fitsplots as fp

# Modules part of Standard Library
import glob
import os
import json
import gc

# modules which may not be installed
try:
    from astropy.table import Table
    from astropy.io import fits
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('agg')
    plt.ioff()

except:
    print("""Please make sure the following modules have been installed:
        1. pandas
        2. matplotlib
        3. astropy
    """)

# app directory
try:
    os.mkdir("./app")
except:
    pass

# databases directory
try:
    os.mkdir("./app/databases")
except:
    pass

# create JSON files
try:
    plotsdb = open("./app/databases/plotsdb.json", "w")
    plotsdb.close()
except:
    print("The file plotsdb already exists")
