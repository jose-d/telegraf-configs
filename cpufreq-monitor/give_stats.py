#!/usr/bin/env python3

import sys
import os
import re

# hardware-speficic:
# - can be collected using this command:
# numactl --hardware | grep cpus | sed 's/node /node_/g' | sed 's/ cpus: /_cpus=["/g' | sed 's/ /","/g' | sed 's/$/" ]/g'

node_0_cpus = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
               "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47"]
node_1_cpus = ["16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
               "31", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63"]


def byteArrayToString(bytearray) -> str:
    return str(bytearray.decode('utf8')).strip()


if __name__ == "__main__":
    # we collect values like this: /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq - there are values in kHz

    base_path = "/sys/devices/system/cpu"
    cpu_dir_raw_list = os.listdir(base_path)
    cpu_id_list = []

    # simple filter to get just cpu* paths..
    for cpuid in cpu_dir_raw_list:
        if "cpu" not in cpuid:
            continue
        if "idle" in cpuid:
            continue
        cpu_id_list.append(cpuid)

    file_open_flags = os.O_RDONLY
    for cpuid in cpu_id_list:
        cpu_n = cpuid.replace('cpu', '')

        if str(cpu_n) in node_0_cpus:
            socket = "0"
        if str(cpu_n) in node_1_cpus:
            socket = "1"

        scaling_cur_freq_file_path = os.path.normpath(
            "{base_path}/{cpu_path}/cpufreq/scaling_cur_freq".format(base_path=base_path, cpu_path=cpuid))
        fd = os.open(scaling_cur_freq_file_path, file_open_flags)

        # 10bytes is enough to get laarge freqs :)
        scaling_cur_freq_khz = byteArrayToString(os.read(fd, 10))
        os.close(fd)

        # in Grafana aren't kHZ defined so we need to convert to Hz
        scaling_cur_freq_hz = int(scaling_cur_freq_khz)*1000

        # print the values in the influx line protocol (https://docs.influxdata.com/influxdb/v1.8/write_protocols/line_protocol_tutorial/)
        print("cpufreq,cpu={cpu},socket={socket} scaling_cur_freq={scaling_cur_freq}".format(
            cpu=cpuid, socket=socket, scaling_cur_freq=scaling_cur_freq_hz))
