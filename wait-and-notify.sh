#!/usr/bin/bash

# wait-and-notify.sh
# Description: Wait for a site to come back up and send a notification through Pushover and libnotify.
# Usage: Set variables and run ./wait-and-notify.sh
# Requires: bash, ping, curl, notify-send
#
# dev notes:
# whipped this up in a couple minutes after getting tired of manually checking for DNS propagation.
# dead simple, and kept here so i don't have to rewrite all of it later.

# URL to watch
URL=
# interval to watch (in seconds)
INTERVAL=15
# Pushover API app token
PUSHOVERTOKEN=
# Pushover API user token
PUSHOVERUSER=
# Message to send (via notify-send and Pushover)
MESSAGE=
until ping -c 1 $URL
do
  sleep 15
done
curl -X POST -d "token=$PUSHOVERTOKEN" -d "user=$PUSHOVERUSER" -d "message=$MESSAGE" https://api.pushover.net/1/messages.json
notify-send "$MESSAGE"
