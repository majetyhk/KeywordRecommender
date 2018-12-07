#!/bin/bash
fname=$1
cat "$fname" | sed 's/\r$//' |\
grep -v -- "-->" |\
grep -v "^$" |\
grep -E -v "^[0-9]+$" |\
sed 's/WEBVTT//' |\
tr -s ' ' |\
tr -d '\t' |\
sed 's/\\/\\\\/g' |\
sed 's/"/\\"/g'
