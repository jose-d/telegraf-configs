#!/usr/bin/python

import os
import subprocess
import sys
import threading

mmpmon_path = '/usr/lpp/mmfs/bin/mmpmon'


# --
# classes

class Command:

    # good old class I use to execute commands in OS shell.

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

        return self.rc, self.stdout, self.stderr


# --
# functions


def dump_data(data):
    site_prefix = str("gpfs,cluster=" + str(data['cluster']) + ",filesystem=" + str(data['filesystem']))
    for metric in metrics:
        print(str(site_prefix) + " " + str(metric) + "=" + str(data[metric]))


# --
# metric config

metrics = ["disks", "bytes_read", "bytes_written", "opens", "closes", "reads", "writes", "readdir", "inode_updates"]

nvdict = {}

nvdict['cluster:'] = 'cluster'
nvdict['filesystem:'] = 'filesystem'
nvdict['disks:'] = 'disks'
nvdict['bytes read:'] = 'bytes_read'
nvdict['bytes written:'] = 'bytes_written'
nvdict['opens:'] = 'opens'
nvdict['closes:'] = 'closes'
nvdict['reads:'] = 'reads'
nvdict['writes:'] = 'writes'
nvdict['readdir:'] = 'readdir'
nvdict['inode updates:'] = 'inode_updates'

# --
# main

if __name__ == "__main__":

    script_path = os.path.dirname(os.path.realpath(__file__))
    arguments = '-i ' + str(script_path) + '/commandFile'
    cmd_string = str(mmpmon_path) + ' ' + str(arguments)

    cmd = Command(cmd_string)

    rc, stdout, stderr = cmd.run(5)

    if rc != 0:
        print('Something went wrong when calling ' + str(mmpmon_path) + ' ' + str(arguments))
        sys.exit(1)

    for line in stdout.splitlines():
        if "mmpmon node" in str(line):
            if 'data' in locals():
                dump_data(data)
            data = {}
            node_name = str(line).split()[4]
            data['name'] = node_name
            data['measurement'] = 'gpfs'

        if "timestamp:" in str(line):
            data['timestamp'] = str(line).split(':')[1].strip().split('/')[0]

        for metric in nvdict:
            if metric in str(line):
                data[nvdict[metric]] = str(line).split(':')[1].strip()

    if 'data' in locals():
        dump_data(data)
