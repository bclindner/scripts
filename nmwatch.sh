#!/bin/bash

# nmwatch.sh - check NetworkManager connections and automatically restart any dead connections. great for keeping VPNs and other interfaces up when NetworkManager fails to do so.
# usage: ./nmwatch.sh [connections-to-keep-alive]



# this program needs to loop infinitely
while true
do
  # get the output of "nmcli con show".
  conshow=$(nmcli con show)
  # clear the screen now instead of before the command, because nmcli
  # takes a lot of time to execute and will leave the screen blank
  # until it's done otherwise.
  clear
  # pretty-print a simplified status with awk.
  # the awk script broken down:
  # FNR > 1 {                                 # for every line after 1 (which serves as a header):
  # if ($4 == "--")                           # if the 4th argument is a -- (meaning NetworkManager has no device set for it):
  #   print $1": \033[31minactive\033[39m";   # print <device>: inactive. \033[31m sets text to red, and \033[39m resets the color
  # else                                      # if the 4th argument actually has a device:
  #   print $1": \033[32mactive\033[39m"      # print <device>: active. \033[32m sets text to green, and \033[39m resets the color
  # }
  echo "$conshow" | awk 'FNR > 1 {if ($4 == "--") print $1": \033[31minactive\033[39m"; else print $1": \033[32mactive\033[39m"}' &
  # get a list of inactive connections.
  # awkscript is roughly: for each line where the 4th column is --, print the first column
  inactive=$(echo "$conshow" | awk '$4 == "--" {print $1}')
  # for each connection that the script was told to watch:
  for con in $@
  do
    # if the connection is in the inactive list:
    if ( echo "$inactive" | grep $con &>/dev/null ); then
      # bring the connection up
      echo -n "bringing $con up..."
      nmcli con up $con &>/dev/null && echo " success! "|| echo "error!"
    fi
  done
  sleep 5
done
