#!/bin/sh -x
for f in *.MP4; do
    `which ffmpeg` -i "$f" "$f.mp3"
    echo "$f converted"
done

for f in *.mp4; do
    `which ffmpeg` -i "$f" "$f.mp3"
    echo "$f converted"
done
