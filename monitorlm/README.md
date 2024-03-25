# Wolfram Mathematica monitorlm Telegraf config

this config calls `monitorlm` and using `monitorlm_template.yml` collects quantitative data about used mathematica licenses at Wolfram license server.


## example of output

```
[root@license telegraf.d]# telegraf --test --config ./inputs.mathlm.conf 
2024-03-25T11:11:02Z I! Loading config: ./inputs.mathlm.conf
2024-03-25T11:11:02Z I! Starting Telegraf 1.29.2 brought to you by InfluxData the makers of InfluxDB
2024-03-25T11:11:02Z I! Available plugins: 241 inputs, 9 aggregators, 30 processors, 24 parsers, 60 outputs, 6 secret-stores
2024-03-25T11:11:02Z I! Loaded inputs: disk exec
2024-03-25T11:11:02Z I! Loaded aggregators: 
2024-03-25T11:11:02Z I! Loaded processors: rename
2024-03-25T11:11:02Z I! Loaded secretstores: 
2024-03-25T11:11:02Z W! Outputs are not used in testing mode!
2024-03-25T11:11:02Z I! Tags enabled: host=license.phoebe.lan
> monitorlm,host=license.phoebe.lan,source=monitorlm ca_fe_authorized=0,ca_fe_available=0,ca_fe_out=0,ca_ke_authorized=0,ca_ke_available=0,ca_ke_out=0,ca_sub_fe_authorized=0,ca_sub_fe_available=0,ca_sub_fe_out=0,ca_sub_ke_authorized=0,ca_sub_ke_available=0,ca_sub_ke_out=0,cb_fe_authorized=13,cb_fe_available=10,cb_fe_out=3,cb_ke_authorized=13,cb_ke_available=12,cb_ke_out=1,cb_sub_fe_authorized=104,cb_sub_fe_available=104,cb_sub_fe_out=0,cb_sub_ke_authorized=104,cb_sub_ke_available=104,cb_sub_ke_out=0,total_fe_authorized=13,total_fe_available=10,total_fe_out=3,total_ke_authorized=13,total_ke_available=12,total_ke_out=1,total_sub_fe_authorized=104,total_sub_fe_available=104,total_sub_fe_out=0,total_sub_ke_authorized=104,total_sub_ke_available=104,total_sub_ke_out=0 1711365062000000000
[root@license telegraf.d]#
```