# telegraf-collectors

* Cpufreq-monitor
* Mathmon
* gpfs_stats_collector

## Cpufreq-monitor

Parses `/sys/devices/system/cpu/cpuXX/cpufreq/scaling_cur_freq` . Manual customization of script is needed to define NUMA node topology (aka cpu-ID vs socket-ID relations).


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

## Deprecated

### ibmon

Monitoring of Infiniband is now implemented in upstream Telegraf.
