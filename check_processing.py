

### The intent of this script is to verify ongoing alta activity, its suppose to run over cron reading the old happili notification outputs and then if there is something major it will notify me over slack


from autorun_manual import verify_logfiles, slack_hook
import subprocess
import datetime
import os
import time

def get_past_slack_notifications(filepath):
    """Based on output filepath from vanessa"""
    return None


def check_taskid():
    """checks log files for errors, checks long timestamps, checks processor utilization
    tid - currenta running taskid
    TODO: Find a way to Check if all raw files are present
    """
    data = get_past_slack_notifications('')

    # TODO: Take last entry tid

    # temporarily get most recent tid by listing all

    cmd = 'ls -ltr /data/apertif'
    ret = subprocess.check_output(cmd, shell=True, universal_newlines=True)
    tid = int([i for i in ret.split('\n')[-2].split(' ') if i != ''][-1])
    try:
        verify_logfiles(tid, this_script=False)
    except Exception as e:
        slack_hook('Could not check log files with exception: '+str(e))
    print('Checked logfiles')

    check_long_timestamps()

    print('Checked timestamp')

    get_last_modified(tid)

    print('Checked modified')

    check_raw(tid)

    print('Checked all')

    if datetime.datetime.now().hour == 10 and datetime.datetime.now().minute<40:
	slack_hook('Module check')
    
    return


def get_last_modified(tid):
    """Checks last touched folder in /data/apertif"""
    path = ['/data/apertif/','/data2/apertif/','/data3/apertif/','/data4/apertif/']

    for i in path:
        if datetime.datetime.now()-datetime.datetime.strptime(time.ctime(os.path.getmtime(i+str(tid))),"%a %b %d %H:%M:%S %Y") < datetime.timedelta(minutes=60):
            slack_hook('Path: {} last changed more than 10 minutes ago'.format(i+str(tid)))
    return 



def check_long_timestamps():
    cmd = 'ls -ltr /home/moss/autocal/happili-0*/*log'
    ret = subprocess.check_output(cmd, shell=True, universal_newlines=True)
    last_line = [i for i in ret.split('\n')[-2].split(' ') if i != '']
    months = {'Jan':1,'Feb':2, 'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
    if last_line[-2].split(':')[1][0]=='0':minute=int(last_line[-2].split(':')[1][1])
    else: minute=int(last_line[-2].split(':')[1])
    if last_line[-2].split(':')[0][0]=='0':hour=int(last_line[-2].split(':')[0][1])
    else: hour=int(last_line[-2].split(':')[0])
    if datetime.datetime.now()-datetime.datetime(year=datetime.datetime.now().year,month=months[last_line[-4]], day=int(last_line[-3]),hour=hour, minute=minute) < datetime.timedelta(minutes=10):
        slack_hook('Last update in long logs more than 10 minutes ago')
    return


def check_raw(tid):
    path = ['/data/apertif/','/data2/apertif/','/data3/apertif/','/data4/apertif/']
    beamlist = []
    for j in range(0,10): 
        if len(os.listdir(path[0]+str(tid)+'/0'+str(j)+'/raw'))<3:
            beamlist.append(j)
    for j in range(10,20): 
        if len(os.listdir(path[1]+str(tid)+'/'+str(j)+'/raw'))<3:
            beamlist.append(j)
    for j in range(20,30): 
        if len(os.listdir(path[2]+str(tid)+'/'+str(j)+'/raw'))<3:
            beamlist.append(j)
    for j in range(30,40): 
        if len(os.listdir(path[3]+str(tid)+'/'+str(j)+'/raw'))<3:
            beamlist.append(j)

    if len(beamlist)>0:
        slack_hook('Not enough raw files in tid:{} and beams:{}'.format(tid, beamlist))
    print('Checked Raw, ', beamlist)

    return




if __name__=='__main__':
    with open('/home/semler/test_file_check.txt', 'wr') as f:
	f.write('trigerred')
    check_taskid()





