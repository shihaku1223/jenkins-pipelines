#!/bin/bash
DEST=$1
val=$(mount -l | awk -v "dest=$DEST" '{ if ($1 == dest) { print "TRUE" } }')

if [ "$val" == "TRUE" ]; then
  exit 0
else
	exit 1
fi
