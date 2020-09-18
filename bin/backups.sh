#!/bin/sh
rsync -av --delete /Volumes/OSXDATA/Pictures $1
rsync -av --delete /Volumes/OSXDATA/Archives $1
