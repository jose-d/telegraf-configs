# telegraf-collectors

## cpufreq-monitor

Parses /sys/devices/system/cpu/cpuXX/cpufreq/scaling_cur_freq . Manual customization script is needed to define NUMA node topology (aka cpu-ID vs socket-ID relations).



## ibmon

Parses output of ```perfquery``` (provided by ```infiniband-diags``` RPM, [(manpage)](https://linux.die.net/man/8/perfquery)).

### Configuration

Snippet for ```telegraf.conf```

```
[[inputs.exec]]
   commands = [
     "/usr/local/sw/monitors/ibmon/give_stats.py"
   ]
   timeout = "5s"
   data_format = "influx"
```

Snippet for ```sudoers.d/monitoring```

```
telegraf ALL=NOPASSWD:  /usr/sbin/perfquery *
```

* ```perfquery_path= "/usr/sbin/perfquery"``` - should point to perfquery binary



## mathmon

Calls ```monitorlm``` binary[(link to Wolfram/Mathematica docu)](https://reference.wolfram.com/language/tutorial/MonitoringMathLM.html) to collect usage of Wolfram Mathematica licences.

### Configuration

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
