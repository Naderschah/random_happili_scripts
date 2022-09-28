
# TODO: Ask Vanessa about this, also raffaella and betsy about time allocation

# See if we can link this into Vanessa`s send slack message script 
# Idea is to collect info about each taskid in case it fails, i.e. file sizes, storage available, 


# system cmds: df --- hardrive space, du -sh <ataskid> --- folder size, should be aronud 200GB (after apergest)
# In case folder is too large look at subfolders --- maybe automate deleting let see 

# Possibly load log file may be over the top

# For some we may be able to automate the script from kulkin TODO: get dir




# Below will be temporary note taking





# First image rm extra unneeded files

# Second image ignore

# rsync -amv /data/apertif/<YYMM>* /tank/apertif/
# copies files to tank from YY MM 
# After completed reomve from data so space is free for processing
# THen make symbolic links to tank storage : ln -s <Source> <Linkname>

# FOr jupyter notebook there is a link tank2 linked to tank   


# 6TB lasts about a week



# Most common issues
# Most Crash of ALTA
# When it happes pipeline cant receive or process
# If during receiving crashes silently check with htop or alike
#  ls -lt1 head to get most recent
# look into log by less taskid/log...
# If didnt work Traceback in GET_ALTA
# Go to slack aston alta operations report alta crashed... 
# Go clean taskid directory with folder
# Crash during ingest: After finish we have products that need to go to alta storage
# See in slack Apergest failed
# PRob alta crashed again
# in home of kulkin run_apergest.py
# DOes everything ./run_apergest <taskid>
# Safe to run
# -d makes it delete files localy need to delete anyway but only after ingestion
# Runs twice once without and once with

# If double calibrator issue usually processed manually or text vanessa

# Tos tart or stop pipeline:
# echo <ON/OFF> > /home/moss/autocal/STATUS
# Just a file saying if its on or off



# TODO: Alta flow
autocal
# Data gets send to alta then gets retrieved from alta with iget <taskid> all done automatically 
# Then processing is done and results are sent aback, whole process takes around 2TB per 10beams


# I am now in astron_user with gid 9000

# To clean raw we require sudo TODO: Discuss with Vanessa, she does this recursively

Logfiles:
/moss/autocal/happili-0x/
Should have autocal transfer 
/moss/apergest/happili-0x/
ingest_done_0x.txt holds ingest log of tid_beam

The kutkin and moss file only gets added to if ingest is completed

/data/apertif/run_apergest.py tid checks kutkin and moss file if already ingested

add to github chmod in autocal so i can delete

do less to check what is wrong in tid apercal.log

To check alta:

ils /altaZone/archive/apertif_main/visibilities_default/tid_AP_B0nn


After finissh run_apergest.py <taskid> in 20 something hours

# CHeck: /data/apertif/210718041/apercal.log


Check alta

for i in {0..9}; do echo $i; ils /altaZone/archive/apertif_main/visibilities_default/210612050_AP_B00$i; sleep 2;  done



If pipeline turns off echo off > ...
and do some manual processing until Vanessa reset the pipeline or whatever she does


# In case crash is suspected check long timestamps by doing 
ls -ltr /home/moss/autocal/happili-0*/*log
