#!/usr/bin/env python3

import logging
import os

BASE_PATH = "/sys/devices/system/cpu"


def readScalingCurFreqFromCpu(i: int):
    """returns current core frequency in Hz as Grafana knows Hz"""
    cpu_id = f"cpu{i}"
    scalingCurFreqFilePath = os.path.join(
        BASE_PATH,
        cpu_id,
        "cpufreq", "scaling_cur_freq"
    )
    try:
        fd = open(scalingCurFreqFilePath, "r")
        freq_string = fd.readline()
        fd.close()
    except FileNotFoundError:
        logging.error(f"CPU doesn't provide {scalingCurFreqFilePath} API.")
        exit(1)

    return int(freq_string.strip())*1000


def getPhysicalPackageIdFromCpu(i: int):
    cpu_id = f"cpu{i}"
    physicalPackageIdFilePath = os.path.join(
        BASE_PATH,
        cpu_id,
        "topology", "physical_package_id"
    )
    fd = open(physicalPackageIdFilePath, "r")
    package_id_string = fd.readline()
    fd.close()
    return int(package_id_string.strip())


if __name__ == "__main__":

    fd_present = open(f"{BASE_PATH}/present", "r")
    fd_present_content = fd_present.readline()
    fd_present.close()
    cpu_min, cpu_max = str(fd_present_content).split('-')

    for i in range(int(cpu_min), int(cpu_max)+1):
        cpu_id = f"cpu{i}"
        freq = readScalingCurFreqFromCpu(i)
        socket = getPhysicalPackageIdFromCpu(i)
        print(f"cpufreq,cpu=cpu{i},socket={socket} scaling_cur_freq={freq}")
