#!/usr/bin/env python3

## Validate all HTML files through Validator.nu.

import urllib.request as url
import json
import os

# pwd
dir = os.listdir('.')
# check if any files are html
for listing in dir:
    if listing[-4:] == "html":
        # open valid files
        with open(listing) as file:
            print('[INFO] found file '+listing+'. validating...')
            # send them to validator.nu
            req = url.Request('http://html5.validator.nu?out=json')
            req.add_header('Content-Type','text/html')
            req.data = file
            with url.urlopen(req) as res:
                # set flag for errors
                errors = False
                # get messages and parse them
                msgs = json.load(res)['messages']
                for msg in msgs:
                    # if there are errors, output them
                    if msg['type'] == "error":
                        # set errored flag
                        errors = True
                        print('[ERR!] on line '+str(msg['lastLine'])+", column "+str(msg['lastColumn'])+": "+msg['message'])
                # say if there were errors or not based on flag
                if errors:
                    print("[ERR!] there were errors")
                else:
                    print("[INFO] no errors found")
