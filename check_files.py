# Script to check file sizes of past observations and if they are ingested

import sys
import os
import subprocess
import datetime as dt
import re


def check_data(period):
    """Gets tids within period  and returns them as dict
    period - days to check for
    """
    months = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
    # To check if dir has a numeric name or not
    regex = '^[0-9]+$'
    # Until when to check
    date = dt.date.today()-dt.timedelta(days=period)
    # check which naming applies to data dirs
    data_dir = {'data':[], 'data2':[], 'data3':[], 'data4':[]}
    for i in data_dir:
        res = subprocess.run(['ls','-lt1', '/{}/apertif'.format(i)],capture_output=True).stdout.decode('utf-8')
        #Split along newlines and make list of lists
        res = str(res).split('\n')[1:-1:]
        res = [[k.strip(' ') for k in j.split(' ') if k.strip(' ')!=''] for j in res if 'tank' not in j]
        # With the below we can find the last index of res within the date range
        for k in range(len(res)):
            month = res[k][-4]
            day = res[k][-3]
            if dt.date(dt.date.today().year, months[month],int(day)) < date:
                break
            else:
                pass
        # k-1 since it stops on the item where the above condition does not hold
        data_dir[i] = [res[z][-1] for z in range(k-1) if re.search(regex, res[z][-1])]
    return data_dir


if __name__=="__main__":
    if len(sys.argv)>1:
        period = sys.argv[1]
    else:
        period = 2
    if period == '-h':
        print('add a number to specify how many days back this should check, default is 2')

    try:
        period = int(period)
    except:
        print('invalid period')
        sys.exit(0)

    hostname = subprocess.run(['hostname'],capture_output=True).stdout.strip(b'\n').decode('utf-8')

    if hostname != 'happili-01':
        print('Can only run on happili-01 your on ', str(hostname))
        sys.exit(0)

    print('Checking local files for past {} days'.format(period))

    #              Check if all data dirs contain the same taskids
    print('Check if taskids in all happili machines')
    data_dir=check_data(period)
    lengths = [len(data_dir[i]) for i in data_dir] 
    if not all(elem == lengths[0] for elem in lengths): 
        print('\033[1;31m Number of taskids accross happili machines not equivalent\033[0m')
        tid_dict = {}
        for i in data_dir:
            for j in data_dir[i]:
                if j in tid_dict.keys():
                    tid_dict[j].append(i)
                else:
                    tid_dict[j] = [i]
        for key in tid_dict:
            print('tid ', key, ' on directories: ', tid_dict[key])

    #               Check file sizes
    # First we change the data_dir into a dict of dicts
    print('Checking file sizes')
    data_dir = {key:{tid:1 for tid in data_dir[key]} for key in data_dir}
    for key in data_dir:
        for tid in data_dir[key]:
            data_dir[key][tid] = os.path.getsize(os.path.join('/'+key, 'apertif', tid))
            if 100*10**9 > data_dir[key][tid] > 130*10**9:
                print('In {} tid {} directory appears to be too large/small with {} GB'.format(key, tid, data_dir[key][tid]/10**9))
    
    #               Check if beams ingested based on lists
    print('Checking if all beams ingested according to log files')
    for key in data_dir:
        # Get happili nr
        if key[-1] == 'a': nr=1
        else: nr = int(key[-1])
        local = '/home/kutkin/apergest/happili-0{}/ingest_done_0{}.txt'.format(nr, nr)
        moss = '/home/moss/apergest/happili-0{}/ingest_done_0{}.txt'.format(nr,nr)
        
        #Load files for happili machine
        ingested = []
        with open(local,'r') as file:
            for line in file:
                if line[0] !='#' and line[0]!='t':
                    ingested.append(line)
        with open(moss,'r') as file:
            for line in file:
                if line[0] !='#' and line[0]!='t':
                    ingested.append(line)

        # Check if all beams for taskid in files
        for tid in data_dir[key]:
            check = ['{}_B0{}{}'.format(tid, nr-1, i) for i in range(0,10)]
            for i in check:
                if i not in ingested:
                    print('Beam {} not ingested'.format(i))
