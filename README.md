# telegraf-collectors



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
