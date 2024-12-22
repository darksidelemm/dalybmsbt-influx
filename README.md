# Daly BT BMS to InfluxDB Collector
Pull power statistics from a BLE-connected Daly BMS and push it into InfluxDB.

Notes:
* The library this uses (dalybt) has a partly broken Daly bluetooth implementation. I've attempted to work around some of the bugs.
* Cell voltages can't be read at the moment.
* I'm only reading the first temperature sensor.

## Setup
```
python3 -m venv venv
pip install -r requirements.txt
```

Edit dalybt_stats.sh and update env vars with appropriate settings.

Setup crontab to run dalybt_stats.sh as required.

## InfluxDB Data Point

Data is added in the following format:
```
{'fields': {'capacity_ah': 87.84,
            'current': 0.0,
            'highest_cell_voltage': 3.469,
            'lowest_cell_voltage': 3.445,
            'soc_percent': 97.6,
            'temp': 21,
            'total_voltage': 13.8},
 'measurement': 'dalybms_power',
 'tags': {'name': 'Rack LiFe Pack'}}
 ```