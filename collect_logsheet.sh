#!/bin/bash


# The purpose of this script is to collect all Error messages from a tids logs form each file and then see if any are out of the ordinary
# The tid must be passed as a cmd line argument


tid=$1
file="/home/semler/error_log_$1.txt"

error_msgs=""

for j in "" "2" "3" "4"
do 
  for i in /data$j/apertif/$tid/*
  do
      if [[ "$i" == *"log"*  ]]; then
  	 error_msgs+="$i\n"
         error_msgs+=$(cat "$i" | grep ERROR)
         error_msgs+="\n\n"
      fi
  done 
done

echo -e "$error_msgs" >>  "$file"

echo "Sent all errors to file: /home/semler/error_log_$1.txt"

