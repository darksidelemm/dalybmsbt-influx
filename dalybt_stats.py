#!/usr/bin/python3
import asyncio
import argparse
import sys
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from pprint import pprint
from dalybt import DalyBMSConnection


async def main():

    # Collect Environment Variables
    DALYBMS_MAC = os.environ.get("DALYBMS_MAC")
    DALYBMS_NAME = os.environ.get("DALYBMS_NAME")
    INFLUXDB_URL = os.environ.get("INFLUXDB_URL")
    INFLUXDB_TOKEN = os.environ.get("INFLUXDB_TOKEN")
    INFLUXDB_ORG = os.environ.get("INFLUXDB_ORG")
    INFLUXDB_BUCKET = os.environ.get("INFLUXDB_BUCKET")
    INFLUXDB_MEASNAME = os.environ.get("INFLUXDB_MEASNAME")


    print(f"Daly BMS MAC Address: \t{DALYBMS_MAC}")
    print(f"Daly BMS Name: \t{DALYBMS_NAME}")

    print(f"InfluxDB URL: \t{INFLUXDB_URL}")
    print(f"InfluxDB Token: \t{INFLUXDB_TOKEN}")
    print(f"InfluxDB Org: \t{INFLUXDB_ORG}")
    print(f"InfluxDB Bucket: \t{INFLUXDB_BUCKET}")
    print(f"InfluxDB Measurement Name: \t{INFLUXDB_MEASNAME}")

    # Try Connecting and polling for data
    con = DalyBMSConnection(mac_address=DALYBMS_MAC)
    await con.connect()
    #await con.update_status()
    await con.update_soc()
    await con.update_temps()
    # Not functioning right now...
    #await con.update_cell_voltages()
    await con.update_cell_voltage_range()
    await con.update_mosfet()
    #await con.update_bal()
    #await con.update_errors()
    await con.bt_bms.disconnect()


    print(con.data)

    # {'status': {'cells': 4, 'temperature_sensors': 1, 'charger_running': False, 'load_running': False, 'states': {'DI1': False}, 'cycles': 3}, 
    # 'cell_v_range': {'highest_voltage': 3.468, 'highest_cell': 2, 'lowest_voltage': 3.444, 'lowest_cell': 3}, 
    # 'soc': {'total_voltage': 13.8, 'current': 0.0, 'soc_percent': 97.6}, 
    # 'mosfet': {'mode': 'stationary', 'charging_mosfet': True, 'discharging_mosfet': True, 'capacity_ah': 87.84}}

    fields = {
        'capacity_ah': con.data['mosfet']['capacity_ah'],
        'soc_percent': con.data['soc']['soc_percent'],
        'total_voltage': con.data['soc']['total_voltage'],
        'current': con.data['soc']['current'],
        'temp': con.data['temps'],
        'highest_cell_voltage': con.data['cell_v_range']['highest_voltage'],
        'lowest_cell_voltage': con.data['cell_v_range']['lowest_voltage'],
    }

    meas_point = {
        "measurement": INFLUXDB_MEASNAME,
        "tags": {"name": DALYBMS_NAME},
        "fields": fields
    }
    pprint(meas_point)

    # Push into InfluxDB
    write_client = influxdb_client.InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    write_api = write_client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=meas_point)

    print("Done!")

asyncio.run(main())