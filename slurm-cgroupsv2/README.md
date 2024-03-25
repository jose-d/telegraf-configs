# cgroupsv2 plugin for slurm(d)

captures data from compute node cgroups fs


## example output

```
[root@n1 telegraf.d]# telegraf --test --config ./inputs.cgroups.conf 
2024-03-25T10:55:11Z I! Loading config: ./inputs.cgroups.conf
2024-03-25T10:55:11Z I! Starting Telegraf 1.29.2 brought to you by InfluxData the makers of InfluxDB
2024-03-25T10:55:11Z I! Available plugins: 241 inputs, 9 aggregators, 30 processors, 24 parsers, 60 outputs, 6 secret-stores
2024-03-25T10:55:11Z I! Loaded inputs: cgroup (2x)
2024-03-25T10:55:11Z I! Loaded aggregators: 
2024-03-25T10:55:11Z I! Loaded processors: starlark
2024-03-25T10:55:11Z I! Loaded secretstores: 
2024-03-25T10:55:11Z W! Outputs are not used in testing mode!
2024-03-25T10:55:11Z I! Tags enabled: host=n1.koios.lan
> cgroup,host=n1.koios.lan,nodeWide=True,path=/sys/fs/cgroup/system.slice/slurmstepd.scope/ memory.current=36442583040i,memory.swap.current=0i 1711364112000000000
> cgroup,host=n1.koios.lan,job_id=7216637,nodeWide=False,path=/sys/fs/cgroup/system.slice/slurmstepd.scope/job_7216637 memory.current=2387808256i,memory.current_percent=4.744148763020833,memory.high=50331648000i,memory.low=0i,memory.max=50331648000i,memory.min=0i,memory.swap.current=0i 1711364112000000000
> cgroup,host=n1.koios.lan,job_id=7216638,nodeWide=False,path=/sys/fs/cgroup/system.slice/slurmstepd.scope/job_7216638 memory.current=9912692736i,memory.current_percent=19.6947509765625,memory.high=50331648000i,memory.low=0i,memory.max=50331648000i,memory.min=0i,memory.swap.current=0i 1711364112000000000
> cgroup,host=n1.koios.lan,job_id=7216639,nodeWide=False,path=/sys/fs/cgroup/system.slice/slurmstepd.scope/job_7216639 memory.current=2441224192i,memory.current_percent=4.850276692708333,memory.high=50331648000i,memory.low=0i,memory.max=50331648000i,memory.min=0i,memory.swap.current=0i 1711364112000000000
> cgroup,host=n1.koios.lan,job_id=7216640,nodeWide=False,path=/sys/fs/cgroup/system.slice/slurmstepd.scope/job_7216640 memory.current=2356973568i,memory.current_percent=4.6828857421875005,memory.high=50331648000i,memory.low=0i,memory.max=50331648000i,memory.min=0i,memory.swap.current=0i 1711364112000000000
> cgroup,host=n1.koios.lan,job_id=7216641,nodeWide=False,path=/sys/fs/cgroup/system.slice/slurmstepd.scope/job_7216641 memory.current=3521867776i,memory.current_percent=6.997322591145834,memory.high=50331648000i,memory.low=0i,memory.max=50331648000i,memory.min=0i,memory.swap.current=0i 1711364112000000000
> cgroup,host=n1.koios.lan,job_id=7216642,nodeWide=False,path=/sys/fs/cgroup/system.slice/slurmstepd.scope/job_7216642 memory.current=9513897984i,memory.current_percent=18.9024169921875,memory.high=50331648000i,memory.low=0i,memory.max=50331648000i,memory.min=0i,memory.swap.current=0i 1711364112000000000
> cgroup,host=n1.koios.lan,job_id=7216643,nodeWide=False,path=/sys/fs/cgroup/system.slice/slurmstepd.scope/job_7216643 memory.current=2342936576i,memory.current_percent=4.654996744791666,memory.high=50331648000i,memory.low=0i,memory.max=50331648000i,memory.min=0i,memory.swap.current=0i 1711364112000000000
> cgroup,host=n1.koios.lan,job_id=7216644,nodeWide=False,path=/sys/fs/cgroup/system.slice/slurmstepd.scope/job_7216644 memory.current=2404700160i,memory.current_percent=4.7777099609375,memory.high=50331648000i,memory.low=0i,memory.max=50331648000i,memory.min=0i,memory.swap.current=0i 1711364112000000000
[root@n1 telegraf.d]#
```