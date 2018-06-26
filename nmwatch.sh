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
  # using the output of the command, pretty-print a simplified status with awk:
  # awk script is a little drawn out so it's commented accordingly
  echo "$conshow" | awk '
  # for every line after 1 (which serves as a header):
  FNR > 1 {
    # if the 4th argument is a -- (meaning NetworkManager has no device set for it):
    if ($4 == "--") {
      # print <device>: inactive.
      # \033[31m sets text to red, and \033[39m resets the color
      print $1": \033[31minactive\033[39m"
    }
    # if the 4th argument actually has a device:
    else {
      # print <device>: active.
      # \033[32m sets text to green, and \033[39m resets the color
      print $1": \033[32mactive\033[39m"
    }
  }';
  # get a list of inactive connections.
  # awkscript is roughly: for each line where the 4th column is --, print the first column
  inactive=$(echo "$conshow" | awk '$4 == "--" {print $1}')
  # for each connection that the script was told to watch:
  for con in $@
  do
    # if the connection is in the inactive list:
    # using grep here is a little janky; may be in need of refinement
    if ( echo "$inactive" | grep -w $con &>/dev/null ); then
      # bring the connection up
      echo -n "bringing $con up..."
      nmcli con up $con &>/dev/null && echo " success! "|| echo "error!"
    fi
  done
  sleep 5
done
