#!/usr/bin/python

import threading
import subprocess
import json


mmpmon='/usr/lpp/mmfs/bin/mmpmon'
arguments='-i /usr/local/monitoring/gpfs_stats_collector/commandFile'

# --
# classes etc

class Command:
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None
        self.stdout = None
        self.stderr = None
        self.rc = None

    def run(self, timeout):
        def target():
            self.process = subprocess.Popen(self.cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.stdout, self.stderr = self.process.communicate()
            self.rc = self.process.wait()

        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            print('Command.run(): timeout: terminating process')
            self.process.terminate()
            thread.join()
            self.rc = 999

        return (self.rc, self.stdout, self.stderr)

def dump_data(data):
  site_prefix = str("gpfs,cluster=" + str(data['cluster']) + ",filesystem=" + str(data['filesystem']))
  
  metrics = ["disks","bytes_read","bytes_written","opens","closes","reads","writes","readdir","inode_updates"]
  for metric in metrics:
    print str(site_prefix)+" " + str(metric) + "=" + str(data[metric])


# lookup table:
nvdict = {}

nvdict['cluster:']='cluster'
nvdict['filesystem:']='filesystem'
nvdict['disks:']='disks'
nvdict['bytes read:']='bytes_read'
nvdict['bytes written:']='bytes_written'
nvdict['opens:']='opens'
nvdict['closes:']='closes'
nvdict['reads:']='reads'
nvdict['writes:']='writes'
nvdict['readdir:']='readdir'
nvdict['inode updates:']='inode_updates'

if __name__ == "__main__":

    cmd = Command(str(mmpmon)+' '+str(arguments))
    rc,stdout,stderr = cmd.run(5)

    if rc != 0:
        print('Something went wrong when calling ' + str(mmpmon)+' '+str(arguments))
        sys.exit(1)

    everything=[]

    for line in stdout.splitlines():
	if "mmpmon node" in str(line):
            if 'data' in locals():
                dump_data(data)
            data={}
            node_name = str(line).split()[4]
            data['name']=node_name
            data['measurement']='gpfs'

        if "timestamp:" in str(line):
            data['timestamp']=str(line).split(':')[1].strip().split('/')[0]

        for metric in nvdict:
            if metric in str(line):
                data[nvdict[metric]]=str(line).split(':')[1].strip()

    if 'data' in locals(): dump_data(data)



