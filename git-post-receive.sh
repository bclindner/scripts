#!/usr/bin/env bash
# post-receive

# hacky post-receive script.
# checks if ref has been pushed then copies the dir to the deployment dir, removing some sensitive files in the deploy dir.
# probably shouldn't use this in any serious production due to the insecure nature of rms, but it works for class, so w/e

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
