# galaXy
<p align="center">
 <a href="LICENSE.txt"><img src = "https://img.shields.io/github/license/sammarth-k/chandralc?logo=MIT"></a> <a herf="https://python.org" target="_blank"><img src="https://img.shields.io/badge/Made%20with-Python-306998.svg"></a> <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
 
galaXy is an automated software capable of processing thousands and thousands of raw lightcurves

It is an upgraded version of `<a href="https://github.com/sammarth-k/galaXy.lc">`galaXy.lc`</a>` with a better UI, ML capabilities and more analysis features.

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
