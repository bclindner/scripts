#!/usr/bin/bash

# altcase.py:
# Description: A oneliner for ripping online media straight to a desired format.
# Usage: ./ripoff.sh [url to rip] [file+extension to save as]
# Requires: youtube-dl and ffmpeg
# dev notes: this is technically a oneliner that's no more than syntactic sugar
# on top of what youtube-dl can theoretically already do, and it's technically
# less efficient, but honestly, i need something that just works for a task
# like this, and this does the job wonderfully.
if ! [ -x "$(command -v youtube-dl)" ]; then
  echo "This command needs youtube-dl (pip install youtube-dl)."
  return 1
fi
if ! [ -x "$(command -v ffmpeg)" ]; then
  echo "This command needs ffmpeg."
  return 1
fi
youtube-dl $1 -o - | ffmpeg -i pipe:0 $2
