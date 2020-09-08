#!/bin/bash

NODE="$1"

awk -v node="$NODE" '$0 ~ "Exception" { print node"\terror occurred" } \
    { if ( $1 == "null" ) { print node"\t" "node is offline" } \
    else if ( $1 == "Result:" ) { print node"\t" $0 } }'
