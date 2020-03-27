#!/usr/bin/env python3

# d2l-bulkdlfix.py
# Description: Parses a directory of Desire2Learn bulk-downloaded zipped
#  submissions and trims unwanted metadata that D2L prepends to each filename.
# Usage: launch script in directory with files to fix
# Requires: Python 2 or 3
#
# dev notes:
# written around late 2015 to early 2016 for TA work.
# i later got used to downloading individually, so this script got very little use.
# sparsely commented, but comments were added in 2018 to add to my git repository.


import os,re
# ls/dir
zips = os.listdir(".")
# parse over each file
for zip in zips:
    # extension check so any incorrect submissions aren't caught in the fixer
    if zip[-3:] == "zip":
        # keep the old zip name to print later
        old = zip
        # cut the metadata from the start of the filename
        ## real filename starts after AM- or PM- so regex works here
        new = re.split("[AP]M-",zip)
        if len(new) == 1: # hacky sanity check to ensure the split worked
            continue
        # print original filenames for logging purposes
        print(str(old)," > ",str(new[1]))
        # perform the rename
        os.rename(old,new[1])
