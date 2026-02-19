#/bin/sh

speed="0.7"

mkdir "speed-${speed}x"

for f in *.mp3
  do ffmpeg -i "$f" -filter:a "atempo=${speed}" "./speed-${speed}x/$f"
done