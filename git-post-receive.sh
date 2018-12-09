#!/usr/bin/env bash

# git-post-receive.sh
# Description: Checks if ref has been pushed then copies the dir to the deployment dir, removing some sensitive files in the deploy dir.
# Usage: move/link this script to hooks under post-recieve of a bare git repo
# Requires: git, bash
#
# dev notes:
# oof, this script hurts to look at.
# i wrote this as part of a web security course to help automate deployment of project updates to the webserver.
# i usually kept the server this script was running on firewalled HARD (read: to my IP only, and only when I'm using it),
# due in part to the nature of the web security labs being insecure,
# but also because i did hacks like this that probably leaked sensitive data more than once.
# still, it was fast, and got the job done.
# i only wish i would have refactored it when I was still using it. maybe someday.


while read fromref toref branch
do
  deploydir=/var/www/html
  if [[ $branch == *master ]]
  then
    echo "deploying commit $toref..."
    GIT_WORK_TREE=$deploydir git checkout -f master
    rm -r $deploydir/.git*
    rm -r $deploydir/*.sql
    rm -r $deploydir/*.md
  else
    echo "not a master push (on branch $branch); not deploying"
  fi
done
