#!/bin/bash

dire='./stock'

for file in $( ls $dire ) 
do
    full=$dire'/'$file

    if [ -h "$full" ] ; then
        echo "symlink, skip"
    elif [ $full == "convertgray.sh" ] ; then
        echo "the script, skip"
    else
        echo "processing $full"
        inkscape $full --verb=org.inkscape.color.grayscale --verb=FileSave --verb=FileClose
    fi
done
