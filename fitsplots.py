def plot(binnings=[500, 1000], figsize = (10,6)):
    '''

    '''
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

        # counter to count iterations
        itercount = 0
        total_files = len(files)

    # begin processing
    for file in files:

        # metadata dict
        metadata = {}

        # get data from files
        hdu_list = fits.open(file, memmap=True)
        evt_data = Table(hdu_list[1].data)

        try:
            del df, f
            gc.collect()
        except:
            pass
        df = pd.DataFrame()
        df['Count'] = list(evt_data['COUNTS'])
        df['exp'] = list(evt_data['EXPOSURE'])

        # to eliminate unwanted observations (if needed)
        threshold = 20  # set to -1 to include all files

        if np.sum(df.Count) > threshold:

            # cumulative plots
            filesave = "./app/images/cumulatives/cumulative_" + \
                str(itercount+1) + ".png"  # name to save file by

            # initialise variables
            count = 0
            tups = []
            times = 0.0

            # Build DataFrame
            for index, row in df.iterrows():
                if df['exp'][index] > 0:
                    count = count + row['Count']
                    times = times + 3.241039999999654/1000
                    tups.append((times, count))
                elif df['exp'][index] == 0:
                    count = count + 0
                    times = times + 3.241039999999654/1000
                    tups.append((times, count))

            # plotting
            df2 = pd.DataFrame(tups, columns=["Time", "Count"])
            ax = df2.plot(x="Time", y="Count", kind="line", legend=True, figsize=(
                15, 9), title="Cumulative Photon Count v/s Time Plot [" + str(itercount+1) + "]")

            # customisation
            f = plt.gcf()
            plt.rc('text', usetex=False)
            plt.rc('font', family='sans serif')
            plt.xlabel(r'Time (ks)', fontsize=25)
            plt.ylabel(r'Photon Count', fontsize=25)
            plt.rc('xtick', labelsize=30)
            plt.rc('ytick', labelsize=22)
            f.savefig(filesave)
            plt.close()

            # creating metadata

            # name of source
            file = file.split("_lc.fits")
            file = file[0].split("_")
            obsid = file[1]

            # source coordinates
            metadata["Source"] = file[0]

            # observation ID
            metadata["ObsID"] = obsid

            # net counts
            metadata["Counts"] = count

            # to calculate observation time and count rate
            rate = count/times

            # total observation time
            metadata['Obs. Time'] = times

            # total counts / total time
            metadata['Count Rate'] = rate

            # lightcurves with binnings
            for grpsize in binnings:

                # filename
                filesave = f"./app/images/lightcurves/{grpsize}/lightcurve_{itercount+1}.png"

                photons_in_group = []

                group_size = int(grpsize/3.24)

                temp1 = []

                for i in range(len(df.Count)):
                    if df.exp[i] > 0:
                        temp1.append(df.Count[i])

                temp3 = len(temp1)

                # range: total number of df points over included bins --> temp3 of intervals
                for j in range(temp3//group_size):
                    j = j*group_size  # temp3 of intervals times temp3 of bins in that interval
                    temp2 = 0
                    for k in range(group_size):
                        # sum of all photons within one interval
                        temp2 = temp2 + temp1[j+k]
                    # appends that sum to a list
                    photons_in_group.append(temp2)

                # group size commented out to get total counts per bin
                # /(3.241039999999654*group_size)
                avg_phot = np.array(photons_in_group)
                temp1 = list(range(len(temp1)))  # //group_size))
                temp1 = np.array(temp1)

                # ---------------------------

                avg = []
                nums = 0

                for i in avg_phot:
                    for j in range(group_size):
                        avg.append(i)  # average photons per bin
                        nums += 1

                # getting NumPy array length of the array and increasing values by 1
                f = np.array(range(nums))
                # adjusting for kiloseconds and multiplying each value in the array by the exposure time
                f = f*3.241039999999654/1000

                # customizing the plot
                plt.figure(figsize=(15, 9))
                plt.rc('text', usetex=False)
                plt.rc('font', family='sans serif')
                plt.xlabel(r'Time (ks)', fontsize=25)
                plt.ylabel(r'Photon Count', fontsize=25)
                plt.rc('xtick', labelsize=30)
                plt.rc('ytick', labelsize=22)
                plt.title(
                    f"Binned Photon Count {file[0]} [{itercount+1}] for {group_size} bins = {grpsize} s")
                plt.plot(f, avg)

                # adjusting the scale of axis
                upper = np.max(avg)
                plt.yticks(np.arange(0, upper+1, 3))

                f = plt.gcf()

                f.savefig(filesave)

                plt.close()
                f.clear()

            # progress
            print(f"{itercount+1} of {total_files} processed")

            # close fits
            hdu_list.close()

            itercount += 1

        else:
            # Build DataFrame
            count, times = 0, 0
            for index, row in df.iterrows():
                if df['exp'][index] > 0:
                    count = count + row['Count']
                    times = times + 3.241039999999654/1000
                elif df['exp'][index] == 0:
                    count = count + 0
                    times = times + 3.241039999999654/1000

        # creating metadata

            # name of source
            file = file.split("_lc.fits")
            file = file[0].split("_")
            obsid = file[1]

            # source coordinates
            metadata["Source"] = file[0]

            # observation ID
            metadata["ObsID"] = obsid

            # net counts
            metadata["Counts"] = count

            # to calculate observation time and count rate
            rate = count/times

            # total observation time
            metadata['Obs. Time'] = times

            # total counts / total time
            metadata['Count Rate'] = rate

            # close fits
            hdu_list.close()

            itercount += 1

    # dumping to JSON file
    plotsdb = open("./ap/databases/plotsdb.json", "w+")

    # in case of empty file
    try:
        jsonfile = json.loads(plotsdb)
    except:
        jsonfile = {}

    jsonfile[f"{file}"] = metadata
    jsonfile = json.dumps(jsonfile)
    plotsdb.write(jsonfile)
    plotsdb.close()