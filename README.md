# galX-C

galX-C is an automated software capable of processing thousands and thousands of raw lightcurves

## Documentation:

### Downloading

### Running the software

### Using modules independently

Some of the modules available in galX-C can be used independently for their purposes. Given below are the selected modules which can be used.

#### fitsplots and txtplots

#### fits2txt


#### Requirements:

- FITS or txt lightcurves. Lightcurves must have headers in the following format:
  - `['TIME_BIN', 'TIME_MIN', 'TIME', 'TIME_MAX', 'COUNTS', 'STAT_ERR', 'AREA', 'EXPOSURE', 'COUNT_RATE', 'COUNT_RATE_ERR']`
  - If headers are not present, make sure there are 10 columns and each column contains data pertaining to the above headers
  - Without these headers the program will not work. You can, however, edit the headers in the code. Headers can only be edited for txt files.
  - These lightcurves are extracted via CIAO using this software: xyz'
