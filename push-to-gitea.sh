#!/usr/bin/env bash

# push-to-gitea.sh:
# Description: Creates a Gitea repository using their REST API and pushes the repository in the current directory to it.
# Usage: Set the necessary variables below, then run "./push-to-gitea.sh.sh [reponame]" inside a repo
# Requires: bash, curl, git
# dev notes: similar to push-to-github.sh. makes for very easy push-to-create!
username=
reponame=$username/$1
branchname=gitea
gitea_token=
server=
if [[ -n $username ]] && [[ -n $gitea_token ]] && [[ -n $server ]]; then
  curl --fail -X POST "$server/api/v1/user/repos" \
  -H "accept: application/json" \
  -H "Authorization: token $gitea_token" \
  -H "Content-Type: application/json" \
  -d "{ \"name\": \"$reponame\", \"private\": false}"
  cd $reponame
  git remote add $branchname https://$server/$reponame.git
  git push $branchname
fi
