#!/usr/bin/env bash

# nmwatch.sh
# Description: Check NetworkManager connections and automatically restart any
#  dead connections. Great for keeping VPNs and other interfaces up when
#  NetworkManager fails to do so.
# Usage: ./nmwatch.sh [connections-to-keep-alive]
# Requires: bash, nmcli, grep, awk, echo - most GNU/Linux/systemd systems should have these
#
# dev notes:
# funny story behind this one!
#
# as of the time of this writing, this script is deployed to a Raspberry Pi
# that captures my apartment's provided Wi-Fi network and relays it through the
# ethernet port to a Nintendo Switch dock nearby, relaying all traffic to and
# from that connection through a VPN, in what might be the greatest home
# network bodge I've ever done.
#
# all of this was set up because ISP-managed Wi-Fi hotspots are the only way to
# connect to the Internet here, and due to a combination of their NAT settings
# and Nintendo's insistence on using peer-to-peer architectures for online
# multiplayer games, many Nintendo games won't allow me to play online.
#
# this setup is the only way I can evade the NAT rules and make online
# connections while still keeping latency low enough to play the game.
#
# this script comes into play because the VPN occasionally dies (i think due to
# lack of activity) and I have to plug in a keyboard and restart the connection
# manually.
#
# i could have fixed this in a simpler way (namely a oneliner that greps `nmcli
# con show` for connection status and reconnects when a grep fails), but i took
# the opportunity to learn a bit of awk to also give myself a semi-real-time
# readout of the network connection status, so i could see if all the
# connections were on at a glance when something wasn't working right.


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
