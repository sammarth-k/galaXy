def plot(binnings=[500, 1000], figsize=(10, 6), mode="fits"):
    """ """
    # Modules part of Standard Library
    import glob
    import os
    import gc

    # modules which may not be installed
    try:
        from astropy.table import Table
        from astropy.io import fits
        import pandas as pd
        import numpy as np
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

    # to use module independently
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
    files = [file for file in glob.glob("*.fits")]

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

    # counter to count iterations
    itercount = 0
    total_files = len(files)
    chandra_bin = 3.241039999999654
    # begin processing
    for file in files:

        # get data from files
        hdu_list = fits.open(file, memmap=True)
        evt_data = Table(hdu_list[1].data)

        df = pd.DataFrame()
        df["Count"] = list(evt_data["COUNTS"])
        df["exp"] = list(evt_data["EXPOSURE"])

        # to eliminate unwanted observations (if needed)
        threshold = 20  # set to -1 to include all files

        # initialise variables
        count = 0
        counts = []

        # Creating counts array
        for index, row in df.iterrows():
            if df["exp"][index] > 0:
                count += df.Count[index]
            elif df["exp"][index] == 0:
                count += 0

            counts.append(count)

        # array for total_time
        time_array = [chandra_bin / 1000 * i for i in range(1, len(counts) + 1)]

        total_time = time_array[-1]
        total_counts = count

        # creating metadata
        metadata = {}
        # name of source
        file = file.split("_lc.fits")[0].split("_")
        # file = file[0].split("_")
        obsid = file[1]
        # source coordinates
        metadata["Source"] = file[0]
        # observation ID
        metadata["ObsID"] = obsid
        # net counts
        metadata["Counts"] = total_counts
        # to calculate observation time and count rate
        rate = total_counts / total_time
        # total observation time
        metadata["Obs. Time"] = total_time
        # total counts / total time
        metadata["Count Rate"] = rate

        filename = "_".join(file)

        if total_counts > threshold:

            # cumulative plots
            filesave = f"./app/images/cumulatives/cumulative_{itercount + 1}.png"

            # plotting
            plt.figure(figsize=figsize)
            plt.plot(time_array, counts)
            plt.xlabel("Time (ks)")
            plt.ylabel("Net Counts")
            plt.title(f"Cumulative Photon Count v/s Time Plot [{filename}]")
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

                # filename
                filesave = (
                    f"./app/images/lightcurves/{grpsize}/lightcurve_{itercount+1}.png"
                )

                photons_in_group = []

                group_size = int(grpsize / chandra_bin)

                temp1 = [
                    df.Count[i] if df.exp[i] > 0 else 0
                    for i in range(len(df.Count))
                    if df.exp[i] > 0
                ]

                # range: total number of df points over included bins --> temp3 of intervals
                for j in range(len(temp1) // group_size):
                    # len(temp1) of intervals total_time temp3 of bins in that interval
                    j = j * group_size
                    temp2 = 0
                    for k in range(group_size):
                        # sum of all photons within one interval
                        temp2 = temp2 + temp1[j + k]
                    # appends that sum to a list
                    photons_in_group.append(temp2)

                # group size commented out to get total counts per bin
                avg_phot = np.array(photons_in_group)  # /(3.241039999999654*group_size)

                avg = [i for i in avg_phot for j in range(group_size)]

                # getting NumPy array length of the array and increasing values by 1
                f = np.array(range(len(avg)))

                # adjusting for kiloseconds and multiplying each value in the array by the exposure time
                f = f * chandra_bin / 1000

                # customizing the plot
                plt.figure(figsize=(15, 9))
                plt.rc("text", usetex=False)
                plt.rc("font", family="sans serif")
                plt.xlabel(r"Time (ks)", fontsize=25)
                plt.ylabel(r"Photon Count", fontsize=25)
                plt.rc("xtick", labelsize=30)
                plt.rc("ytick", labelsize=22)
                plt.title(
                    f"Binned Photon Count {filename} for {group_size} bins = {grpsize} s"
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
        print(f"{itercount+1} of {total_files} processed")

        itercount += 1

        # dumping to JSON file (json module was creating problems)
        plotsdb = open("./app/databases/plotsdb.json", "a+")
        plotsdb.write('"' + f"{filename}" + '"' + f":{metadata},".replace("'", '"'))
        plotsdb.close()

    plotsdb = open("./app/databases/plotsdb.json", "a+")
    plotsdb.write(f'"Total files": {total_files}' + "}")
    plotsdb.close()
