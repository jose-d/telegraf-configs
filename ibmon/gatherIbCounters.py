#!/usr/bin/env python3

import sys
import os
import re

BASE_PATH = "/sys/class/infiniband"
PORT_REGEXP = "^mlx5.*"
MEASUREMENT_NAME = "infiniband"

def _getLineFromFile(filepath: str) -> str:
    fd = open(filepath)
    line_string = fd.readline()
    fd.close()
    return line_string

def get_phys_state(portPath: str) -> int:
    phys_state_string = _getLineFromFile(f"{portPath}/phys_state")
    return int(phys_state_string.split(':')[0])

def get_rate(portPath: str) -> int:
    rate_string = _getLineFromFile(f"{portPath}/rate")
    return int(rate_string.split(' ')[0])

def get_state(portPath: str) -> int:
    state_string = _getLineFromFile(f"{portPath}/state")
    return int(state_string.split(':')[0])

def get_counters_list(portPath: str, suffix: str) -> list:
    return os.listdir(str(portPath)+'/'+str(suffix)) #fixme - os join or so..

def read_counter_value(counterPath: str) -> int:
    fd = open(counterPath)
    line_string = fd.readline()
    fd.close()
    return int(line_string)

def getMlx5DevicesList() -> list:
    """ get devices in BASE_PATH matching regexp mlx5 """
    directory_content = os.listdir(BASE_PATH)
    r = re.compile(PORT_REGEXP)
    return list(filter(r.match, directory_content))

def getPortList(devicePath:str) -> list:
    """ get port list for given device path """
    return os.listdir(str(devicePath)+'/ports')


if __name__ == "__main__":

    devices = getMlx5DevicesList()
    for device in devices:
        deviceFullPath = f"{BASE_PATH}/{device}"
        ports = getPortList(deviceFullPath)
        for port in ports:

            data = {}

            portFullPath = f"{deviceFullPath}/ports/{port}"

            # 1) get individual states:
            data['phys_state'] = get_phys_state(portFullPath)
            data['rate'] = get_rate(portFullPath)
            data['state'] = get_state(portFullPath)

            # 2) collect counter values

            prefixes = [ "counters", "hw_counters" ]

            for prefix in prefixes:
                counters = get_counters_list(portFullPath,prefix)
                for counter in counters:
                    counterFullPath = f"{portFullPath}/{prefix}/{counter}"
                    data[counter] = read_counter_value(counterFullPath)

            # produce influxdb line protocol line to stdout:
            prefix_string = f"{MEASUREMENT_NAME},device={device},port={port}"
            data_list = []
            for item in data:
                data_list.append(f"{item}={data[item]}i")

            data_string = ','.join(data_list)
            influx_line = f"{prefix_string} {data_string}"
            print(influx_line)
