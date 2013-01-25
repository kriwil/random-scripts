#!/bin/sh
thedate=`date +%Y%m%d`
datepart=`echo $thedate | cut -b -7`
rsync -czvP -e "ssh -i $HOME/Personal/usgd/usgd_new.pem" ubuntu@pat.usgreendata.com:~/backups/usgd_main.$datepart* $HOME/Dropbox/USGD\ Database/
