#!/usr/bin/env python3

# mastodon-massban.py:
# Description: Ban all users on a Mastodon instance which have recently logged
# in with a given IP.
# Usage: Set the necessary variables below, then run ./mastodon-massban.py
# Requires: python3 with the "mastodon.py" package
# dev notes: does what it says on the tin. written in about 2 minutes to handle
# a problem on mastodon.technology and refined a bit thereafter.

from mastodon import Mastodon

# IP of the accounts to ban
iptoban = ''
# instance API access token - you can create this in the "development" menu
# this token MUST have admin:read:accounts and admin:write:accounts access
token = ''
# url of the instance to access
apiurl = ''

mastodon = Mastodon(access_token=token, api_base_url=apiurl)
accts = mastodon.admin_accounts(ip=iptoban, status="active")
for acct in accts:
    mastodon.admin_account_moderate(acct['id'], action="suspend", text="Your account (and IP) are being suspended for mass spamming.")
    print("Banned user "+acct['username'])
