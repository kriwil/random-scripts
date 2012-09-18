for img in *.JPG; do echo "$img"; mogrify -resize 1024x768 "$img"; done
