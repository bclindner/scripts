#!/usr/bin/env python3

# romconsolidator.py
# Description: Parses a directory of ROM files, picks out duplicates, prompts
#  the user to decide which ones to keep, if any, and deletes any unwanted
#  duplicates.
# Usage: launch script in directory with files to fix
# Requires: default Python libraries
#
# dev notes:
# written around 2013 or so, before i started at Georgia Southern.
# could easily be adapted for most duplicate filename processing.
# comments were added in post in 2018 as it was being added to my git repo.
# one of my prouder hacks, honestly!

import os
# initialize some globals we'll be using in the loop
romname = "" # name of ROM we're currently checking duplicates for
romstack = [] # stack of ROMs with the same romname
# run through every file (listdir generally gets this alphabetically)
## NOTE: python documentation says listdir is in arbitrary order. maybe apply a sort?
for file in os.listdir("./"):
    # if the ROM name is the same as the one we're currently on:
    ## most ROMs are in format "<ROMNAME> (REGION).EXT", therefore we can get the <ROMNAME> by splitting at " ("
    if file.split(" (")[0] == romname:
        # add that to an array stack
        romstack.append(file)
    # if the ROM name is different than the current one, and os.listdir returned an alphabetical sort, that means that we most likely have reached the end of duplicates for that ROM and it's time to process
    else:
        # only consolidate if there's more than one ROM
        if len(romstack) > 1:
            print("consolidating: "+romname)
            # print out a list of all the ROMs to choose from, starting from 1
            i=0
            for rom in romstack:
                i = i+1
                print(str(i)+". "+rom)
            # prompt the user what to do with this set of ROMs
            ## -1 is added to the input to make it 0-indexed, as the list we printed earlier is 1-indexed for user friendliness
            choice = input("Keep which ROM? (type \"all\" for all, \"none\" for none) ")-1
            # if the choice isn't "all" then we have some culling to do
            if choice.lower is not "all":
                # if the user's choice corresponds to one of the numbers, pop that one and remove it from the stack
                if type(choice) is int and romstack[choice] is not None:
                    # romstack.pop() removes the choice from the array, preventing it from being deleted as will be done below
                    print("Keeping "+romstack.pop(choice)+".")
                # delete all items still in the stack
                for item in romstack:
                    os.remove(item)
        # now that the processing is done, reset the name of the ROM we're processing...
        romname = file.split(" (")[0]
        # ...and reset the stack with that as the first ROM
        romstack = [file]
