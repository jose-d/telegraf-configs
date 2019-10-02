#!/usr/bin/env python3

import sys
import os
import re
from shared import Command

perfquery_path= "/usr/sbin/perfquery"

if __name__ == "__main__":

    arguments = "-x"	# to show extended mellanox counters
    cmd_string = 'sudo ' + str(perfquery_path) + ' ' + str(arguments)	# we need root rights to access counters

    cmd = Command(cmd_string)
    rc, stdout, stderr = cmd.run(5)

    if rc != 0:
        print('Something went wrong when calling ' + str(perfquery_path) + ' ' + str(arguments))
        sys.exit(1)

    without_dots = stdout.replace(".", "")

    data = {}

    for line in str(without_dots).splitlines():
        try:
            key = str(line.strip().split(':')[0].strip()).lower()
            value = int(str(line.strip().split(':')[1].strip()).lower())	#this int() overtyping ensures no trash values :)
        except:
            continue
        else:
            data[key]=value

    for item in data:
        print(str("perfquery_data") + " " + str(item) + "=" + str(data[item]))
