#!/bin/sh
ffmpeg -i $1 -pass 1 -vcodec libx264 -preset fast -b 512k -threads 0 -f mp4 -an -y /dev/null && ffmpeg -i $1 -pass 2 -acodec libfaac -ab 128k -ac 2 -vcodec libx264 -preset fast -b 512k -threads 0 $2
