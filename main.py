# custom modules
import lcplot
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

print("Creating directories", end="\r")

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
    plotsdb.write("{")
    plotsdb.close()
except:
    print("The file plotsdb already exists")

# lightcurves
print("Lightcurve plotting starting...\n")
lc_type = input("Enter file extension of lightcurves (txt or fits): ")
header = int(input("""Do your files have headers in the following format:
    ['TIME_BIN', 'TIME_MIN', 'TIME', 'TIME_MAX', 'Count', 'STAT_ERR', 'AREA', 'exp', 'COUNT_RATE', 'COUNT_RATE_ERR']

If yes, enter 1, else enter 0

Enter option here: """))
print()
lcplot.plot(mode=lc_type.lower(), header=1)
# machine learning
print("Lightcurves successfully plotted...")