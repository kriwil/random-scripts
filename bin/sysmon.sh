#!/bin/bash
# Script from http://www.webupd8.org/2011/05/how-to-display-network-upload-download.html#more
# Last Modified by Peter Curtis on 5th October 2011.

#-------------- settings: -----------------------------
netspeed=true
netspeedjoint=true
ram=true
cpu=true

#---------------- initialize ---------------------------
rm /tmp/.sysmon > /dev/null 2>&1
dstat --net --mem --cpu --output=/tmp/.sysmon 1 1 > /dev/null 2>&1

#----------- up/down speed -----------------------------
if [ $netspeed = true ]; then
#upspeed=$(echo $(cat /tmp/.sysmon | tail -1 | cut -d ',' -f2)/1024 | bc)
upspeed=$(echo $(cat /tmp/.sysmon | tail -1 | cut -d ',' -f2)/1 | bc)
upkbmb=$(if [ $upspeed -gt 1024 ]; then
up1=$(echo $(cat /tmp/.sysmon | tail -1 | cut -d ',' -f2)/1024 | bc -l)
echo $up1 | head -c 4
else
echo $upspeed | head -c 3
fi)
#
#downspeed=$(echo $(cat /tmp/.sysmon | tail -1 | cut -d ',' -f1)/1024 | bc)
downspeed=$(echo $(cat /tmp/.sysmon | tail -1 | cut -d ',' -f1)/1 | bc)
downkbmb=$(if [ $downspeed -gt 1024 ]; then
down1=$(echo $(cat /tmp/.sysmon | tail -1 | cut -d ',' -f1)/1024 | bc -l)
echo $down1 | head -c 4
else
echo $downspeed | head -c 3
fi)

#---------------- up/down speed unit --------------------
# upunit=$(if [ $upspeed -gt 1024 ]; then echo "MiB/s"; else echo "KiB/s"; fi)
# downunit=$(if [ $downspeed -gt 1024 ]; then echo "MiB/s"; else echo "KiB/s"; fi)
upunit=$(if [ $upspeed -gt 1024 ]; then echo "K"; else echo "B"; fi)
downunit=$(if [ $downspeed -gt 1024 ]; then echo "K"; else echo "B"; fi)
fi

#-------- up/down padding to keep constant width --------
uppad=$(if [ $upspeed -ge 0 -a $upspeed -lt 10 ]; then 
   echo ".00" ;
     else if [ $upspeed -ge 10 -a $upspeed -lt 100 ]; then 
        echo "0." ;
          else if [ $upspeed -ge 100 -a $upspeed -le 1024 ]; then 
            echo "." ;
          fi
     fi
fi)
downpad=$(if [ $downspeed -ge 0 -a $downspeed -lt 10 ]; then
   echo ".00" ;
     else if [ $downspeed -ge 10 -a $downspeed -lt 100 ]; then 
        echo "0." ;
          else if [ $downspeed -ge 100 -a $downspeed -le 1024 ]; then 
            echo "." ;
        fi
     fi
fi)

#------------------- CPU % used -------------------------
if [ $cpu = true ]; then
#cpufree=$(cat /tmp/.sysmon | tail -1 | cut -d ',' -f9)
cpufree=$(cat /tmp/.sysmon | tail -1 | cut -d ',' -f9 | cut -d '.' -f1)
#cpuused=$(echo 100-$cpufree | bc | sed -e 's/..*//')
cpuused=$(echo `printf "%02d" $((100-$cpufree))`)
fi

#------------------- RAM % used --------------------------
if [ $ram = true ]; then
memused=$(free -m | grep buffers/cache | tr -s ' ' | cut -d' ' -f 3)
memfree=$(free -m | grep buffers/cache | tr -s ' ' | cut -d' ' -f 4)
memtotal=$(echo $memused+$memfree | bc -l)
memusedpercent=$(echo 100-100*$memfree/$memtotal | bc)
fi

#------------------ The Indicator Sysmonitor actual output -
echo $(if [ $ram = true ]; then echo Mem: $memusedpercent% \|; fi) $(if [ $cpu = true ]; then echo CPU: $cpuused% \|; fi) $(if [ $netspeed = true ]; then echo ↑$upkbmb$uppad$upunit↓$downkbmb$downpad$downunit; fi)

