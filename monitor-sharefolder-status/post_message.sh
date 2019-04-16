#!/bin/bash
MSG="$@"
curl -X POST -H "Content-Type: application/json" --data {\"text\":\""$MSG"\"} \
  http://10.156.2.89:8008/rocketchat/ipf3/hooks/4pygkDgX87KdZuSZT/MkFfN3mZ8SimaRyy9yAxj9XaaWANyoRuekwSLXxhEZTyyaTL
