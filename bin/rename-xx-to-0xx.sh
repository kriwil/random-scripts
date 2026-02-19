#!/usr/bin/env bash
# Rename files with 2-digit prefix to 3-digit prefix
# e.g. "42 abc.mp3" -> "042 abc.mp3"

for f in [0-9][0-9]\ *.mp3; do
	[ -e "$f" ] || continue
	new="0${f}"
	echo "Renaming: '$f' -> '$new'"
	mv -- "$f" "$new"
done

echo "Done."
