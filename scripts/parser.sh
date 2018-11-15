#!/bin/bash
fname=$1
sed 's/\r$//' "$fname"    |\
grep -v -- "-->"          |\
grep -v "^$"              |\
grep -E -v "^[0-9]+$"     |\
sed 's/WEBVTT//'          |\
tr '\n' ' '               |\
tr -s ' '                 |\
tr -d '\t'                |\
sed 's/\\/\\\\/g'         |\
sed 's/"/\\"/g'
