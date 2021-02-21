import time
import htmlcode

# start stopwatch
begin = time.time()

# try to import modules
try:
    from astropy.table import Table
    from astropy.io import fits
    import pandas as pd
    import numpy as np
    import glob, os
    import matplotlib.pyplot as plt

except:
    print("""Please make sure the following modules have been installed:

        1. pandas
        2. matplotlib
        3. astropy

    """)


print("""

Hello and welcome to galaXy! This program is capapble of generating an interactive database for your X-Ray files.

Before we begin, we need the following details to be inputted by you:

    1. Binnings - the value (in seconds) of bins for lightcurves. Please enter comma separated values.

    2. File Deletion - Do you wish to delete your files after the web app has been generated? (y/n)

    3. Image Dimensions (inches) as CSV (l,b)

    4. Name of Galaxy

""")

binnings = list(map(int,input("Enter your binnings here (no spaces between commas and numbers): ").split(",")))

deletion = input("Enter either 'y' or 'n' if you want to delete your files after the webapp has been generated: ")

plotsize = tuple(map(int, input("Enter figure dimensions (l,b) as comma separated values: ").split(",")))

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

# lightcureves directory
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
itercount = 0
total_files = len(files)

# begin processing
for file in files:
    
    # get data from files
    hdu_list = fits.open(file, memmap=True)
    evt_data = Table(hdu_list[1].data)

    # initialising DataFrame
    df = pd.DataFrame()
    df['Count'] = list(evt_data['COUNTS'])
    df['exp'] = list(evt_data['EXPOSURE'])

      
    # to eliminate unwanted observations (if needed)
    threshold = 35 # set to -1 to include all files currently

    if np.sum(df['Count']) > threshold:

        # cumulative plots
        filesave = "./app/images/cumulatives/cumulative_" + str(itercount+1) + ".png" # name to save file by

        # initialise variables
        count = 0
        tups=[]
        times = 0.0

        # Build DataFrame
        for index, row in df.iterrows():
            if df['exp'][index]>0:
                count = count + row['Count']
                times = times + 3.241039999999654/1000
                tups.append((times,count))
            elif df['exp'][index]==0:
                count = count + 0
                times = times + 3.241039999999654/1000
                tups.append((times,count))

        # plotting
        df2 = pd.DataFrame(tups, columns =["Time", "Count"])
        ax = df2.plot(x="Time", y="Count", kind="line", legend=True, figsize=(15,9), title="Cumulative Photon Count v/s Time Plot [" + str(itercount+1) + "]")
       
        # customisation
        f = plt.gcf()
        plt.rc('text', usetex=False)
        plt.rc('font', family='sans serif')
        plt.xlabel(r'Time (ks)', fontsize=25)
        plt.ylabel(r'Photon Count',fontsize=25)
        plt.rc('xtick', labelsize=30)
        plt.rc('ytick', labelsize=22)
        f.savefig(filesave)
        plt.close()

        # creating metadata

        # name of source
        file = file.split("_lc.fits")
        file = file[0].split("_")
        obsid = file[1]
        all_files.append({"Source":file[0],"ObsID":obsid,"Counts":count})

        # to calculate observation time and count rate
        rate = count/times
        all_files[itercount]['Obs. Time'] = times
        all_files[itercount]['Count Rate'] = rate

        # lightcurves with binnings
        for grpsize in binnings:

            # filename
            filesave = f"./app/images/lightcurves/{grpsize}/lightcurve_{itercount+1}.png"

            photons_in_group = []

            group_size = int(grpsize/3.24) # changable

            temp1 = []

            for i in range(len(df.Count)):
                if df.exp[i] > 0:
                    temp1.append(df.Count[i])

            temp3 = len(temp1)

            for j in range(temp3//group_size): #range: total number of df points over included bins --> temp3 of intervals
                j = j*group_size #temp3 of intervals times temp3 of bins in that interval
                temp2 = 0
                for k in range(group_size):
                    temp2 = temp2 + temp1[j+k] #sum of all photons within one interval
                photons_in_group.append(temp2) #appends that sum to a list

            # group size commented out to get total counts per bin
            avg_phot = np.array(photons_in_group)#/(3.241039999999654*group_size)
            temp1 = list(range(len(temp1)))#//group_size))
            temp1 = np.array(temp1)

            #---------------------------
            
            avg = []
            nums = 0
        
            for i in avg_phot:
                for j in range(group_size):
                    avg.append(i) #average photons per bin
                    nums += 1

            
            #getting NumPy array length of the array and increasing values by 1
            f = np.array(range(nums))
            #adjusting for kiloseconds and multiplying each value in the array by the exposure time
            f = f*3.241039999999654/1000

            #customizing the plot
            plt.figure(figsize=(15,9))
            plt.rc('text', usetex=False)
            plt.rc('font', family='sans serif')
            plt.xlabel(r'Time (ks)', fontsize=25)
            plt.ylabel(r'Photon Count',fontsize=25)
            plt.rc('xtick', labelsize=30)
            plt.rc('ytick', labelsize=22)
            plt.title(f"Binned Photon Count {file} + [{itercount+1}] for {grpsize} bins = {grpsize*3.24104} s")
            plt.plot(f, avg)

            #adjusting the scale of axis
            upper = np.max(avg)
            plt.yticks(np.arange(0,upper+1,3))

            f = plt.gcf()

            f.savefig(filesave)
            
            plt.close()
        
        #progress
        print(f"{itercount+1} of {total_files} processed")

        # close fits
        hdu_list.close()

        itercount += 1


    else:
        # Build DataFrame
        count,times=0,0
        for index, row in df.iterrows():
            if df['exp'][index]>0:
                count = count + row['Count']
                times = times + 3.241039999999654/1000
            elif df['exp'][index]==0:
                count = count + 0
                times = times + 3.241039999999654/1000
          # creating metadata

        # name of source
        file = file.split("_lc.fits")
        file = file[0].split("_")
        obsid = file[1]
        all_files.append({"Source":file[0],"ObsID":obsid,"Counts":count})

        # to calculate observation time and count rate
        rate = count/times
        all_files[itercount]['Obs. Time'] = times
        all_files[itercount]['Count Rate'] = rate

        #progress
        print(f"{itercount+1} of {total_files} processed")

        # close fits
        hdu_list.close()

        itercount += 1
# delete files after processing
if deletion == "y":
    print("Deleting files...")
    for file in files:
        os.remove(file)
    
    print("Your files have been successfully deleted!\n\n")

print("Beginning webapp generation...")

# html file
app = open("./app/index.html", "w",encoding="utf-8")

# css and js
try:
    os.mkdir("./app/css")
except:
    pass

try:
    os.mkdir("./app/js")
except:
    pass

# making css and js files
css = open("./app/css/style.css","w")
js = open("./app/js/script.js","w")

# building html
towrite = htmlcode.head(name) + htmlcode.table_top(binnings=binnings)

for curr_file in range(1,len(all_files)+1):
    towrite += htmlcode.table_row(dict=all_files[curr_file-1],count=curr_file,binnings=binnings)

towrite += htmlcode.table_bottom()
app.write(towrite)

# building css and js
js.write(htmlcode.js(str(all_files)))
css.write(htmlcode.css())

# adding logo
logo = open("./app/images/logo.svg","w")
logo.write(htmlcode.logo())
logo.close()

print("Your webapp is ready to go! Open index.html to see it in action!")

# end stopwatch
end = time.time() 

# close files
app.close()
css.close()
js.close()

# stats
print(f"Total runtime of the program was {end - begin}") 