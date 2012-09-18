#!/bin/sh
ffmpeg -i $1 -acodec libfaac -aq 100 -vcodec libx264 -preset slow -crf 22 -threads 0 $2
