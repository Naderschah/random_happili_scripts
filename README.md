## Explanation of Random scripts written while working for APERTIF

# check_files.py 

This script checks file sizes in the tid provided as a cmd line argument on the current machine
It uses a standard range to verify things are on the ~100 GB scale 
It also checks if the files have been ingested

-- Rarely used tuned out to be less usefull than initially imagined

# check_nr_files.py

As the name suggests checks the number of files in a tid provided as a cmd line argument if there is more than 10000 files it runs du -sh to verify file size

-- This was also less usefull than imagined

# check_processing.py

Never finished, this was supposed to be an automated way of checking the state of apercal, however a redirect of the slack messages was needed and an open ssh connection to the other nodes to make this efficient, fragments of this may be useful however was also abandoned

# notes.py

Initially some script, ended up being a random collection of notes: may be useful may not be

# slack_behavior

Describes how slack messages are sent and in what step of automated (apercal) processing, very useful for debugging and was actually written for that purpose

# collect_logsheets.sh

Takes tid as cmd line arguemnt, change path inside script to your home dir. Creates a file containing all error messages of a tid, usually quite lengthy, very good for quick verification and to see the scale of the issue

# run_apergest_foreign.py

Modified version of run_apergest to allow ingest of happili non native beam numbers
For this script to work the source code of apergest needs to be changed to allow forwarding of the intended happili node, make sure to change the intended happili node to the one to be ingested when running

# simlink_non_links.sh 

Checks for regex pattern (i.e. YYMMDD* will select all tids of year month day) in data and tank will present list of tids to be moved and simlinked and if its already on tank if so check which directory is larger (more complete) and merge delete whatever is appropriate for the specific case. Anyway if ypu enter Y on the option it will rsync the files remove the directory from data and simlink the directory back to data. More of a quality of life script than anything else

