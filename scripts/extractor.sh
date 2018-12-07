#!/bin/bash


if [ $# -eq 0 ]; then
    echo "No arguments supplied supplied. Usage: ./scrtpt.sh video-id"
    exit 0
fi

mkdir -p "$HOME/subtitles/"
mkdir -p "$HOME/text/"
mkdir -p "$HOME/subtitles/tmp/"
cp "$HOME/Keyword_Recommender/scripts/parser.sh" "$HOME/subtitles/."
#method 1, extract subtitles uploaded by provider - example - uuatZO76MgQ
youtube-dl --write-sub --sub-lang en --skip-download https://www.youtube.com/watch?v="$1" -o "$HOME/subtitles/$1"


#if [ ! -f /"$PWD"/"$1*" ]; then
if ls "$HOME/subtitles/$1"* 1> /dev/null 2>&1; then
    echo "downloaded from provider uploaded SRT, and extracting it"
    sh "$HOME/Keyword_Recommender/scripts"/parser.sh "$HOME/subtitles/$1".en.vtt > "$HOME/text/$1".txt
    exit 0

else
    echo "Fall back - Download automatic subtitles form youtube"
    # method 2, extrac automatic subtitles   example - 8f3ijY0MJBk
    youtube-dl --write-auto-sub --skip-download https://www.youtube.com/watch?v="$1" -o "$HOME/subtitles/tmp/$1"
fi

if ls "$HOME/subtitles/tmp/$1"* 1> /dev/null 2>&1; then
    echo "parse the auto downloaded str files"
    sed -e 's/<[^>]*>//g' "$HOME/subtitles/tmp/$1.en.vtt" > "$HOME/subtitles/$1.en.vtt" 
    sh "$HOME/Keyword_Recommender/scripts"/parser.sh "$HOME/subtitles/$1".en.vtt > "$HOME/text/$1".txt
else
    echo "Fall back - mp3 download and convert text from there"
    #youtube-dl --extract-audio --audio-format mp3 https://www.youtube.com/watch?v="$1" -o "$1.mp3"

    #ffmpeg -i "$1".mp3 -ar 16000 -ac 1 "$1".wav
    #pocketsphinx_continuous -infile "$1".wav 2> pocketsphinx.log > $1.txt &
fi
# method 2, extrac automatic subtitles
#youtube-dl --write-auto-sub --skip-download https://www.youtube.com/watch?v="$1" -o "$1"
