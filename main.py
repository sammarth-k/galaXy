import time
import gc

import htmlcode

# start stopwatch
begin = time.time()

# try to import modules
try:
    from astropy.table import Table
    from astropy.io import fits
    import pandas as pd
    import numpy as np
    import glob
    import os
    import matplotlib.pyplot as plt
    import matplotlib

    matplotlib.use("agg")
    plt.ioff()

except:
    print(
        """Please make sure the following modules have been installed:
        1. pandas
        2. matplotlib
        3. astropy
    """
    )


print(
    """
Hello and welcome to galaXy! This program is capapble of generating an interactive database for your Chandra X-ray Observatory lightcurves!.

Before we begin, we need the following details to be inputted by you:
    1. Binnings - the value (in seconds) of bins for lightcurves. Please enter comma separated values.
    2. File Deletion - Do you wish to delete your files after the web app has been generated? (y/n)
    3. Image Dimensions (inches) as CSV (l,b)
    4. Name of Galaxy
"""
)

binnings = list(
    map(
        int,
        input(
            "Enter your binnings here (no spaces between commas and numbers): "
        ).split(","),
    )
)

deletion = input(
    "Enter either 'y' or 'n' if you want to delete your files after the webapp has been generated: "
)

plotsize = tuple(
    map(
        int,
        input("Enter figure dimensions (l,b) as comma separated values: ").split(","),
    )
)

name = input("Enter name of galaxy: ")


# app directory
try:
    os.mkdir("./app")
except:
    pass

# images directory
try:
    os.mkdir("./app/images")
except:
    pass

# get all required files in directory
os.chdir("./")
files = []
for file in glob.glob("*.fits"):
    files.append(file)

# cumulative directory
try:
    os.mkdir("./app/images/cumulatives")
except:
    pass

# lightcurves directory
try:
    os.mkdir("./app/images/lightcurves")
except:
    pass

# directory for each bin size
for binning in binnings:
    try:
        os.mkdir(f"./app/images/lightcurves/{binning}")
    except:
        pass

# all files in a list of dictionaries
all_files = []

# counter to count iterations
ITERCOUNT = 0
TOTAL_FILES = len(files)
CHANDRA_BIN = 3.241039999999654

# begin processing
for file in files:

    # get data from files
    hdu_list = fits.open(file, memmap=True)
    evt_data = Table(hdu_list[1].data)

    try:
        del df, f
        gc.collect()
    except:
        pass

    # get data from files
    hdu_list = fits.open(file, memmap=True)
    evt_data = Table(hdu_list[1].data)

    df = pd.DataFrame()
    df["Count"] = list(evt_data["COUNTS"])
    df["exp"] = list(evt_data["EXPOSURE"])

    # to eliminate unwanted observations (if needed)
    THRESHOLD = 20  # set to -1 to include all files

    # initialise variables
    COUNT = 0
    counts = []

    # Creating counts array
    for index, row in df.iterrows():
        if df["exp"][index] > 0:
            COUNT += df.Count[index]
        elif df["exp"][index] == 0:
            COUNT += 0

        counts.append(COUNT)

    # array for total_time
    time_array = [CHANDRA_BIN / 1000 * i for i in range(1, len(counts) + 1)]

    total_time = time_array[-1]
    total_counts = COUNT

    # creating metadata

    # name of source
    file = file.split("_lc.fits")[0].split("_")
    obsid = file[1]
    all_files.append({"Source": file[0], "ObsID": obsid, "Counts": total_counts})

    # to calculate observation time and count rate
    all_files[ITERCOUNT]["Obs. Time"] = total_time
    all_files[ITERCOUNT]["Count Rate"] = total_counts / total_time

    FILENAME = "_".join(file)

    # to eliminate unwanted observations (if needed)
    THRESHOLD = 20  # set to -1 to include all files

    if total_counts > THRESHOLD:

        # cumulative plots
        filesave = f"./app/images/cumulatives/cumulative_{ITERCOUNT + 1}.png"

        # plotting
        plt.figure(figsize=plotsize)
        plt.plot(time_array, counts)
        plt.xlabel("Time (ks)")
        plt.ylabel("Net Counts")
        plt.title(f"Cumulative Photon Count v/s Time Plot [{FILENAME}]")
        plt.rc("text", usetex=False)
        plt.rc("font", family="sans serif")
        plt.xlabel(r"Time (ks)", fontsize=25)
        plt.ylabel(r"Photon Count", fontsize=25)
        plt.rc("xtick", labelsize=30)
        plt.rc("ytick", labelsize=22)

        # save figure
        f = plt.gcf()
        f.savefig(filesave)
        plt.close()

        # lightcurves with binnings
        for grpsize in binnings:

            # FILENAME
            filesave = (
                f"./app/images/lightcurves/{grpsize}/lightcurve_{ITERCOUNT+1}.png"
            )

            photons_in_group = []

            group_size = int(grpsize / 3.24)

            temp1 = [
                df.Count[i] if df.exp[i] > 0 else 0
                for i in range(len(df.Count))
                if df.exp[i] > 0
            ]

            # range: total number of df points over included bins --> temp3 of intervals
            for j in range(len(temp1) // group_size):
                j = (
                    j * group_size
                )  # temp3 of intervals times len(temp1) of bins in that interval
                temp2 = 0
                for k in range(group_size):
                    # sum of all photons within one interval
                    temp2 = temp2 + temp1[j + k]
                photons_in_group.append(temp2)  # appends that sum to a list

            # group size commented out to get total counts per bis
            avg_phot = np.array(photons_in_group)  # /(3.241039999999654*group_size)

            avg = [i for i in avg_phot for j in range(group_size)]

            # getting NumPy array length of the array and increasing values by 1
            f = np.array(range(len(avg)))
            # adjusting for kiloseconds and multiplying each value in the array by the exposure time
            f = f * CHANDRA_BIN / 1000

            # customizing the plot
            plt.figure(figsize=plotsize)
            plt.rc("text", usetex=False)
            plt.rc("font", family="sans serif")
            plt.xlabel(r"Time (ks)", fontsize=25)
            plt.ylabel(r"Photon Count", fontsize=25)
            plt.rc("xtick", labelsize=30)
            plt.rc("ytick", labelsize=22)
            plt.title(
                f"Binned Photon Count for {FILENAME} for {group_size} bins = {grpsize} s"
            )
            plt.plot(f, avg)

            # adjusting the scale of axis
            upper = np.max(avg)
            plt.yticks(np.arange(0, upper + 1, 3))

            f = plt.gcf()
            f.savefig(filesave)
            plt.close()
            f.clear()

    # close fits
    hdu_list.close()

    # progress
    # print(f"Progress: {ITERCOUNT+1} of {TOTAL_FILES} processed", end="\r)

    ITERCOUNT += 1

print("Plots successfully generated...")

# delete files after processing
if deletion == "y":
    print("Deleting files...")
    for file in files:
        os.remove(file)

    print("Your files have been successfully deleted!\n\n")

print("Beginning webapp generation...")

# css and js
try:
    os.mkdir("./app/css")
except:
    pass

try:
    os.mkdir("./app/js")
except:
    pass

# building html
with open("./app/index.html", "w", encoding="utf-8") as app:
    towrite = htmlcode.head(name) + htmlcode.table_top(binnings=binnings)

    for curr_file in range(1, len(all_files) + 1):
        towrite += htmlcode.table_row(
            dict=all_files[curr_file - 1], count=curr_file, binnings=binnings
        )

    towrite += htmlcode.table_bottom()
    app.write(towrite)

# building css and js
with open("./app/js/script.js", "w") as js:
    js.write(htmlcode.js(str(all_files)))

with open("./app/css/style.css", "w") as css:
    css.write(htmlcode.css())

# adding logo
with open("./app/images/logo.svg", "w") as logo:
    logo.write(htmlcode.logo())
    logo.close()

print("Your webapp is ready to go! Open index.html to see it in action!")

# end stopwatch
end = time.time()

# stats
print(f"Total runtime of the program was {end - begin}")
