#!/usr/bin/python

import sys
import os
import re
from shared import Command

monitorlm_path= "/home/jose/temp/monitorlm"
license_server="localhost"  #or fill in the proper host where mathematica LM is running

if __name__ == "__main__":

    script_path = os.path.dirname(os.path.realpath(__file__))

    arguments = " " + str(license_server) + " -template " + str(script_path) + "/template -format text"

    cmd_string = str(monitorlm_path) + ' ' + str(arguments)

    cmd = Command(cmd_string)
    rc, stdout, stderr = cmd.run(5)

    if rc != 0:
        print('Something went wrong when calling ' + str(monitorlm_path) + ' ' + str(arguments))
        sys.exit(1)

    expr = re.compile(r'(\s)*(\d)+(\s)+(\w)+')

    server_fqdn = ""
    data = {}

    for line in str(stdout).splitlines():

        if "SERVER_FQDN" in line:
            # we have FQDN, let's parse it
            server_fqdn = line.strip().split(' ')[0].strip()

        if re.match(expr, line):
            # its some value - key pair, add it into "data" dictionary
            try:
                value = str(line.strip().split(' ')[0].strip()).lower()
                key = str(line.strip().split(' ')[1].strip()).lower()
            except:
                continue
            else:
                data[key]=value

    site_prefix = str("mathematica,server=" + str(server_fqdn))

    for item in data:
        print(str(site_prefix) + " " + str(item) + "=" + str(data[item]))
