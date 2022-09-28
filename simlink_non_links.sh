#!/bin/bash

# This script is intended to symlink all files of pattern (with wildcards *) entered as the first argument after the script
# It checks in order: if tank has enough space, if rsync was succesfull,  and move them to their respective tank (this runs machine specific)


# First list files so that user can verify
echo "Moving:"
echo "Will move:"
for f in /data/apertif/$1; 
   do 
      if ! [[ -L "$f" ]]; then 
	base=$(basename "$i")
        # Check that tank doesnt have something here
	if ! [[ -L "/tank/apertif/$base" ]]; then
		var="--- This tid also exists on tank"
	fi;
	echo $f $var
      fi; 
   done

read -p "Can these be moved and linked? (Y/n): " move_on
# Check condition
if [ "$move_on" == "Y" ]; then 
# Do actual moving
   for i in /data/apertif/$1;
   do
       if ! [[ -L "$i" ]]; then
           echo "Moving $i"
	   # Check space
	   tank_space=$(df -Pk /tank | sed 1d | grep -v used | awk '{ print $4 "\t" }')
 	   dir_size=$(du -s $i | awk '{print $1}')
	   if [ $dir_size -lt $tank_space ]; then 
	      part1=$(dirname "$i") # Get directory path
	      part2=$(basename "$i") # Get directory name
	      # Check exit code
              if rsync -amv "/data/apertif/$part2" "/tank/apertif/"; then
	   	   rm -r "/data/apertif/$part2"
          	   if ! ln -s "/tank/apertif/$part2" "/data/apertif/"; then
			echo "Simlink was not successfull!"
			echo "Note that the directory has been already moved and removed from data"
			read -p "Double check directory then hit anything to continue iteration" _
	           fi
              else
		   echo "Rsync failed for $i"
		   read -p "Double check directory, if you enter f the script force continue, else this will be skipped: " force_continue
	           if [ $force_continue=="f" ]; then
			rm -r "/data/apertif/$part2"
                        if ! ln -s "/tank/apertif/$part2" "/data/apertif/"; then
                           echo "Simlink was not successfull!"
                           echo "Note that the directory has been already moved and removed from data"
                           read -p "Double check directory then hit anything to continue iteration" _
                        fi;
                   fi;
              fi; echo "Finished $i"
           else
		echo "Not Enough Space on Tank!"	
	   fi;
       fi;
   done
else
   echo "Terminating"
fi
