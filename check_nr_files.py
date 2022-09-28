
from __future__ import print_function
import os
import subprocess

base_dir = '/data/apertif'
results = {}
for rootdir in os.listdir(base_dir):
    if os.path.isdir(os.path.join(base_dir,rootdir)):
	count = 0
	for subdir, dirs, files in os.walk(os.path.join(base_dir,rootdir)):
            for file in files:
	        count += 1
	results[rootdir] = count
	if count>10000:
	    print(subprocess.check_output(['du', '-sh', os.path.join(base_dir, rootdir)]))
	print(rootdir, ' : ',count)

results = sorted(results.items(), key=lambda x:x[1])
print('results')
for i in results:
    print(i[0], ' : ', i[1])
