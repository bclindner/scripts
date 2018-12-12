#!/usr/bin/env bash

# create-and-push.sh:
# Description: Creates a GitHub repository using their REST API and then pushes the repository in the current directory to it.
# Usage: ./create-and-push.sh [username]/[reponame]
# Requires: bash, cut, curl, git
# dev notes: having to go through GitHub's web interface to make repos before pushing annoyed me, so I made this!
# in a pinch, though, when my work just needs to be saved, I still generally just push to a service like GitLab that has push-to-create abilities.
USERNAME=$(echo $1 | cut -f1 -d"/")
REPONAME=$(echo $1 | cut -f2 -d"/")

if [[ -n $USERNAME ]] && [[ -n $REPONAME ]]; then
  curl -X POST \
    -H "Accept: application/vnd.github.v3+json" \
    -d "{\"name\":\"$REPONAME\"}" \
    -u $USERNAME \
    https://api.github.com/user/repos
  git remote add origin https://github.com/$1
  git push -u origin master
fi
