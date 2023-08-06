# GHOST
"At the last dim horizon, we search among ghostly errors of observations for landmarks that are scarcely more substantial. The search will continue. The urge is older than history. It is not satisfied and it will not be oppressed."
--Edwin Hubble

Welcome to GHOST, the database for supernovae and their host galaxies. This database contains ~16k sources in PS1, which were used to predict supernova classes in Gagliano et al. (2020). Installation instructions for the analysis tools are below.

# Installation
1. Create a clean conda environment.

2. Run the following code:
```bash
pip install astro_ghost
```

Or, download this repo and run
```bash
python setup.py install
```
from the main directory.

# Example Usage
```python

import os
import sys
from astro_ghost.PS1QueryFunctions import getAllPostageStamps
from astro_ghost.TNSQueryFunctions import getTNSSpectra
from astro_ghost.NEDQueryFunctions import getNEDSpectra
from astro_ghost.ghostHelperFunctions import *
from astro_ghost.classifier import classify
from astropy.coordinates import SkyCoord
from astropy import units as u
import pandas as pd
from datetime import datetime

#we want to include print statements so we know what the algorithm is doing
verbose = 1

#download the database from ghost.ncsa.illinois.edu
#note: real=False creates an empty database, which
#allows you to use the association methods without
#needing to download the full database first

#create a list of the supernova names and their skycoords (these three are from TNS)
snName = ['SN 2021os', 'SN 2020aerc']

snCoord = [SkyCoord(180.7253405*u.deg, +5.6147629*u.deg, frame='icrs'),\
SkyCoord(358.64857935*u.deg, +34.8807245*u.deg, frame='icrs')]

# run the association algorithm!
# this first checks the GHOST database for a SN by name, then by coordinates, and
# if we have no match then it manually associates them.
# The starcut parameter can be 'normal', 'gentle', or 'aggressive'
hosts = getTransientHosts(snName, snCoord, verbose=verbose, starcut='normal')

# classify transients
predictions = classify(hosts, verbose=verbose)

#create directories to store the host spectra, the transient spectra, and the postage stamps
hSpecPath = "./hostSpectra/"
tSpecPath = "./SNspectra/"
psPath = "./hostPostageStamps/"
paths = [hSpecPath, tSpecPath, psPath]
for tempPath in paths:
    if not os.path.exists(tempPath):
        os.makedirs(tempPath)

transients = pd.DataFrame({'Name':snName, 'RA':[x.ra.deg for x in snCoord], 'DEC':[x.dec.deg for x in snCoord]})

#get postage stamps and spectra
getAllPostageStamps(hosts, 120, psPath, verbose) #get postage stamps of hosts
getNEDSpectra(hosts, hSpecPath, verbose) #get spectra of hosts
getTNSSpectra(transients, tSpecPath, verbose) #get spectra of transients (if on TNS)

# Helper functions for querying the database
supernovaCoord = [SkyCoord(344.5011708333333*u.deg, 6.0634388888888875*u.deg, frame='icrs')]
galaxyCoord = [SkyCoord(344.50184181*u.deg, 6.06983149*u.deg, frame='icrs')]
snName = ["PTF10llv"]
table = fullData()

# 1. Get the entry corresponding to a specific transient by its name (or coordinates)
#    note: The coordinate/name is passed as a list, so multiple entries can be
#          queried simultaneously
#    This function returns the matches as a pandas dataframe (df) along with
#    a list of the sources not found (by name or coordinate)
df, notFound = getDBHostFromTransientCoords(supernovaCoord)
df, notFound = getDBHostFromTransientName(snName)

# 2. Print summary statistics about a particular host galaxy system or set of systems from a supernova
getHostStatsFromTransientName(snName)
getHostStatsFromTransientCoords(supernovaCoord)

# 3. Get stats about the supernovae associated with a host galaxy
galaxyName = ['UGC 12266']
getTransientStatsFromHostName(galaxyName)
getTransientStatsFromHostCoords(galaxyCoord)

# 4. get an image of the field by coordinates
tempSize = 400 #size in pixels
band = ['grizy']
getcolorim(galaxyCoord[0].ra.deg, galaxyCoord[0].dec.deg, size=tempSize, filters=band, format="png")

# 5. get an image of the host galaxy system associated with a supernova (by supernova name)
getHostImage(snName, save=0)

# 6. Find all supernova-host galaxy matches within a certain search radius (in arcseconds)
coneSearchPairs(supernovaCoord[0], 1.e3)

# 7. Classify supernovae as core-collapse or SN Ia based on host galaxy information
feature_list, dataML_preprocessed, labels_df2, names = preprocess_dataframe(hosts, nclass=2, PCA=False)
dataML_matrix_scaled = preprocessing.scale(dataML_preprocessed)
rf = load_classifier()
names = hosts['TransientName'].values
class_predictions = rf.predict(dataML_matrix_scaled, labels_df2.values)
for i in np.arange(len(class_predictions)):
    print("%s is predicted to be a %s." % (names[i], class_predictions[i]))

```

The database of supernova-host galaxy matches can be found at http://ghost.ncsa.illinois.edu/static/GHOST.csv, and retrieved using the getGHOST() function. This database will need to be created before running the association pipeline. Helper functions can be found in ghostHelperFunctions.py for querying and getting quick stats about SNe within the database, and tutorial_databaseSearch.py provides example usages. The software to associate these supernovae with host galaxies is also provided, and tutorial.py provides examples for using this code.


# GHOST Viewer
In addition to these software tools, a website has been constructed for rapid viewing of many objects in this database. It is located at ghost.ncsa.illinois.edu.  Json files containing supernova and host information can be found at http://ghost.ncsa.illinois.edu/static/json.tar.gz. host spectra, SN spectra, and SN photometry are found at http://ghost.ncsa.illinois.edu/static/hostSpectra.tar.gz, http://ghost.ncsa.illinois.edu/static/SNspectra.tar.gz, and http://ghost.ncsa.illinois.edu/static/SNphotometry.tar.gz.
