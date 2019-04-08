#!/bin/bash

awk '$0 ~ "download url:" \
  { print $0; split($3, a, "/"); \
    print a[6] "," a[7] "," a[8]; \
    system("test -d plugins/"a[6]"/"a[7] "|| mkdir -p plugins/"a[6]"/"a[7]"; wget "$3 " -O  plugins/"a[6]"/"a[7]"/"a[8]) \
  }'
