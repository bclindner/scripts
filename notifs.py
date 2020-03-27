#!/usr/bin/env python3

# notifs.py
# Description: Simple Python library that allows sending push notifications.
# Usage: N/A (library)
# Requires: Python 3, Python requests library
#
# dev notes:
# a simple little library I broke out of a script from a class project.
# pretty straightforward stuff, just hitting the REST APIs for certain services.
# i should note this is not fault-tolerant; if stuff explodes it doesn't really
# notify you.
# may fix that later.
import requests

def sendMessage(msg, config):
    if 'groupme' in config:
        sendGroupMeMessage(msg, config['groupme'])
    if 'pushover' in config:
        sendPushoverNotif(msg, config['pushover'])
    if 'discord' in config:
        sendDiscordMessage(msg, config['discord'])

# GroupMe integration
def sendGroupMeMessage(msg, config):
    # get the GroupMe Bot ID
    gmid = config['apiKey']
    # Send the message
    requests.post(url='https://api.groupme.com/v3/bots/post', json={
            "bot_id": gmid,
            "text": msg
        })

# Pushover integration
def sendPushoverNotif(msg, config):
    # Pushover App ID
    pushoverappkey = config['appKey']
    # List of keys to send
    pushoveruserkeys = config['userKeys']
    # Send a message for each user key
    for userkey in pushoveruserkeys:
        requests.post(url='https://api.pushover.net/1/messages.json', json=
            {
                "token": pushoverappkey,
                "user": userkey,
                "message": msg,
            }
        )

# Discord integration
def sendDiscordMessage(msg, config):
    # Bot Token
    token = config['botToken']
    # List of channels to send to
    channels = config['channels']
    # Send a message for each channel
    for channel in channels:
        resp = requests.post(url='https://discordapp.com/api/channels/'+channel+"/messages", json=
            {
                "content": msg
            }, headers=
            {
                "Authorization": "Bot "+token
            }
        )
        print(resp.text)
