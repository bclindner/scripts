#!/usr/bin/env bash

# convert-to-youtube-playlists.sh:
# Description: Converts a list of YouTube links into playlists on the site itself.
# Usage: ./convert-to-youtube-playlists.sh [file of links to get]
# Requires: bash, firefox, cat, head, tail, grep, wc (most GNU/Linux systems should have most of this save for maybe firefox)
#
# dev notes:
# at some point in one of the discord servers i frequent, me and some other folks on the server got to posting a ton of really good game soundtracks.
# we never really got around to compiling all of them into a list, and so all the stuff we posted faded into the message history.
# at some point i scraped the channel (using bclindner/discord-msggrab) as part of an effort to archive a channel we were about to delete, so i went ahead and scraped the channel we were posting in as well to see if i could parse that out.
# i managed to isolate just the youtube links, but looking through the list proved difficult.
# after some googling i came across this stackexchange question: https://webapps.stackexchange.com/questions/72787/how-to-create-a-youtube-playlist-from-a-list-of-links
# i was able to rewrite it into this little script in about 5 minutes, which gave me a set of playlists i could combine into a single playlist.
# it's actually taking me longer to write this than the script, haha.
# this implementation is somewhat buggy; it may open one redundant playlist just to be safe. i didn't put much thought into the while loop.
# regardless, it works! mostly stored in this git repo for future reference.

# file to get the links from (the first arg)
FILE=$1
# counter for the pagination loop
I=50
# rough while loop to ensure it gets all lines
# this process must be done 50 lines at a time because youtube will only parse playlists of 50 videos at most
while [ $((I - 50)) -lt $(cat $FILE | wc -l) ]; do
  # this pipeline is really dumb so let me explain:
  # it takes 50 lines,
  # removes other arguments (remove stuff after the ampersand),
  # takes the last 11 chars (this cuts it down to just the youtube video id),
  # replaces newlines with commas,
  # and removes the last comma for cleanliness
  LINKS=$(head gng-bangers-playlist -n$I | tail -n50 | cut -f1 -d"&" | grep -o '.\{11\}$' | tr "\n" , | head -c-1)
  # generate the link
  LINK=http://www.youtube.com/watch_videos?video_ids=$LINKS
  # open it in a new firefox tab
  firefox -new-tab $LINK
  # increment the counter
  I=$((I + 50))
done
