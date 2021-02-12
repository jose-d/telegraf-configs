# telegraf-collectors

Here are some custom collectors for Telegraf (https://www.influxdata.com/time-series-platform/telegraf), usually related to HPC environment..

* [Cpufreq-monitor](https://github.com/jose-d/telegraf-collectors/blob/master/README.md#cpufreq-monitor) - collects frequency of CPU cores
* [Mathmon](https://github.com/jose-d/telegraf-collectors/blob/master/README.md#mathmon) - collects usage stats of Mathematica licenses
* [gpfs_stats_collector](https://github.com/jose-d/telegraf-collectors/blob/master/README.md#gpfs_stats_collector) - collects GPFS filesystem stats
* ibmon - gathers state and counter values for Mellanox Infifiniband devices.


### ibmon

I revived this script as built-in Infiniband monitoring in Telegraf is broken for Mellanox, Intel ethernet and RHEL-ish-8 OS - https://github.com/influxdata/telegraf/issues/8135. Script parses content of `/sys/class/infiniband`, matches mlx5 devices and pushes data using influx line protocol.

![Grafana visualization of ibmon data](https://github.com/jose-d/telegraf-collectors/blob/master/.docu/Screenshot_2021-02-12%20node%20details%20-%20Grafana.png)


## Cpufreq-monitor

Parses `/sys/devices/system/cpu/cpuXX/cpufreq/scaling_cur_freq` .

### Cpufreq-monitor data in Grafana

![Grafana visualization of cpufreq-monitor data](
https://github.com/jose-d/telegraf-collectors/raw/master/.docu/Screenshot_2020-07-15%20node%20details%20-%20Grafana.png)

## Mathmon

Calls ```monitorlm``` binary[(link to Wolfram/Mathematica docu)](https://reference.wolfram.com/language/tutorial/MonitoringMathLM.html) to collect usage of Wolfram Mathematica licences.

### Mathmon data in Grafana

![Grafana visualisation of Mathmon data](
https://github.com/jose-d/telegraf-collectors/raw/master/.docu/Screenshot_2020-07-15%20Mathematica%20license%20usage%20-%20Grafana.png)

### mathmon configuration

Snippet for ```telegraf.conf```:

```
[[inputs.exec]]
   commands = [
     "/usr/local/sw/monitors/mathmon/give_stats.py"
   ]
   timeout = "5s"
   data_format = "influx"
```

* ```monitorlm_path``` - should point to your monitorlm binary, e.g. ```monitorlm_path= "/usr/local/sw/monitors/mathmon/monitorlm"```
* ```license_server``` - should contain IP or hostname of your Mathematica license server, e.g. ```license_server="192.0.2.1"```



## gpfs_stats_collector

Using ```mmpmon``` [(link to IBM docu)](https://www.ibm.com/support/knowledgecenter/en/STXKQY_5.0.1/com.ibm.spectrum.scale.v5r01.doc/bl1adv_mmpmonch.htm) periodically queries local GPFS statistics.

### Configuration

Snippet for ```telegraf.conf```:

```
[[inputs.exec]]
  command = "/usr/bin/sudo /usr/local/monitoring/gpfs_stats_collector/give_stats.py"
  timeout = "5s"
  data_format = "influx"
```

Needs also sudo rights, because GPFS.., so 

```telegraf ALL=NOPASSWD: /usr/local/monitoring/gpfs_stats_collector/give_stats.py```

should be included in ```/etc/sudoers.d/monitoring```.

Check ```mmpmon_path``` variable if really points to your **mmpmon** binary.
