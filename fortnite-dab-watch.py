#!/usr/bin/env python3

# fortnite-dab-watch.py:
# Description: Script that checks for dab emotes in the Fortnite store and
#  prints them.
# Usage: launch script daily after Fortnite store refresh
# Requires: Python 3, Requests lib, my notifs library
#
# dev notes: why did i do this
import requests
from notifs import sendMessage
import json

with open('fortnite-dab-watch.json') as file:
    config = json.load(file)

resp = requests.get('https://api.fortnitetracker.com/v1/store', headers={'TRN-Api-Key': config['apiKey']})
storeItems = resp.json()
dabItems = [item['name'] for item in storeItems if 'dab' in item['name'].lower()]
if len(dabItems) > 0:
    sendMessage("Dab items available in the Fortnite store today!\nItems on offer:\n"+'\n'.join(dabItems),config['notifs'])

