#!/usr/bin/env python3

import sys
import os

BASE_PATH = "/sys/devices/system/cpu"


def byteArrayToString(bytearray) -> str:
    return str(bytearray.decode('utf8')).strip()


def readScalingCurFreqFromCpu(i:int):
    """returns current core frequency in Hz as Grafana knows Hz"""
    cpu_id = f"cpu{i}"
    scalingCurFreqFilePath = f"{BASE_PATH}/{cpu_id}/cpufreq/scaling_cur_freq"
    fd = open(scalingCurFreqFilePath,"r")
    freq_string = fd.readline()
    fd.close()
    return int(freq_string.strip())*1000

def getPhysicalPackageIdFromCpu(i:int):
    cpu_id = f"cpu{i}"
    physicalPackageIdFilePath = f"{BASE_PATH}/{cpu_id}/topology/physical_package_id"
    fd = open(physicalPackageIdFilePath,"r")
    package_id_string = fd.readline()
    fd.close()
    return int(package_id_string.strip())

if __name__ == "__main__":

    f_possible=open(f"{BASE_PATH}/possible","r")
    f_possible_content = f_possible.readline()
    f_possible.close()
    cpu_min,cpu_max = str(f_possible_content).split('-')

    for i in range(int(cpu_min),int(cpu_max)+1):
        cpu_id = f"cpu{i}"
        freq = readScalingCurFreqFromCpu(i)
        socket = getPhysicalPackageIdFromCpu(i)
        print(f"cpufreq,cpu=cpu{i},socket={socket} scaling_cur_freq={freq}")
