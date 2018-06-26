#!/usr/bin/env python3

# splatgrab.py:
# Description: Grabs Splatoon 2 Miiverse posts from Twitter accounts based on hashtags, then crops, converts, and saves them to uncompressed 1-bit GIF images.
# Usage: launch script in any directory - captured posts will be placed in the same dir as the script
# Requires: tweepy, pillow/PIL, requests, default Python libs
#
# dev notes:
# this one was fun to write! i wanted to keep my posts on Splatoon 2 for posterity, but i hated the way they were posted (in blurry 1280x720), and the Splatoon 2 requires you to share your post on one of two social networks (Facebook and Twitter) for it to be visible to other players. i could easily pull them from the SD card on the console, but knowing me i would probably never bother to back up, let alone spend the time cropping and cleaning up the images.
# i already had an account set up for the posts, so i figured, "why not solve both problems with a little bit of Python?" i set up dev credentials, figured out tweepy and PIL, and wrote this script to watch my Switch sharing account, grab the image, crop it, process it, and save it. quite happy with this one!

import tweepy, requests, json, io, os
from time import sleep
from PIL import Image

# Configuration:
credentialfile = 'tweepy.json' # relative path to credentials
idsToFollow = [''] # twitter UIDs to follow in array form

# Cleans, converts saves a splatoon post as .gif
# Arguments:
# * file (fd): file to convert through the PythonImageLibrary
# * filename (string): name to save the file as
def convertSplatoonPost(file, filename):
    # crop tuple for post editor screenshots.
    # screenshots are more ideal for resizing (retaining the "blocky" unfiltered format), but the cursor may result in the cursor appearing as an anomaly in the final image.
    boxScreenshot = (160, 188, 1120, 548)
    # crop tuple for posts in + button large/filtered format. the blurriness of these images could potentially lead to some noise in the final, re-rendered image.
    # this is the default used for twitter posts, so it's used here
    boxPost = (0, 120, 1280, 600)
    # open the image
    old = Image.open(io.BytesIO(file))
    # crop the image with one of the previous crop tuples
    new = old.crop(boxPost)
    # resize to Miiverse post dimensions, using nearest neighbor algorithm to mitigate blurring/noise caused by filtering/compression, respectively
    new = new.resize([320, 120], Image.NEAREST)
    # convert to 2-color black-and-white format by converting to 1 bpp
    new = new.convert('1')
    # resave the image as gif - less space usage, and no noise due to the nature of the gif format using a limited color palette
    new.save(filename+'.gif')

# Converts SplatNet posts from Twitter into gifs
class StreamPostConverter(tweepy.StreamListener):
    # status handler
    def on_status(self, status):
        # if splatoon 2 hashtag and miiverse hashtag are both in there...
        if '#Splatoon2' in status.text and "#miiverse" in status.text:
            mediaurl = status.entities['media'][0]['media_url_https']
            # sanity check; if it's not jpg we don't want it
            if mediaurl[-3:] == "jpg":
                # download the image and post it!
                print('Got image from status '+status.id_str+'!')
                img = requests.get(mediaurl+':large')
                convertSplatoonPost(img.content, status.id_str)

    def on_error(self, status_code):
        print(str(status_code)+' error.')
        exit(1)

# Main loop: open the credential file and connect to the Twitter API
with open(credentialfile, encoding='utf-8') as creds_json:
    creds = json.load(creds_json)
    auth = tweepy.OAuthHandler(creds['consumer_key'], creds['consumer_secret'])
    auth.set_access_token(creds['token_key'], creds['token_secret'])
    # spool up an instance of our post converter
    listener = StreamPostConverter()
    # start the stream, set it to fire StreamPostConverter when the given acct posts
    print('starting stream...')
    stream = tweepy.Stream(auth=auth, listener=listener)
    stream.filter(follow=idsToFollow)
