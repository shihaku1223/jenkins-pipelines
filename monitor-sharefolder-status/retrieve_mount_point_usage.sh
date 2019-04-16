#!/bin/bash

DEST=$1
THRES=$2

df -t cifs -BM | awk -v "dest=$DEST" -v "thres=$THRES" \
  '{ if( $1 == dest){ \
        gsub("M","",$4); \
        if( strtonum($4) <= strtonum(thres) ) { \
          print "Warning! " $1 " Used:" $3 " Available:" $4  "M Use%:" $5
        } \
    } \
  }'
