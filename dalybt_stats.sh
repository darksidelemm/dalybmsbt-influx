#!/bin/bash
#
# Daly Bluetooth BMS -> InfluxDB Collection Script
#
# Run with cron on whatever update rate you want
#

# Enter your BMS Bluetooth MAC address here.
export DALYBMS_MAC="B6:6B:09:02:07:93"
export DALYBMS_NAME="Rack LiFe Pack"


# InfluxDB Settings
export INFLUXDB_URL="http://localhost:8086"
export INFLUXDB_TOKEN=""
export INFLUXDB_ORG=""
export INFLUXDB_BUCKET=""
export INFLUXDB_MEASNAME="dalybms_power"

# Use a local venv if it exists
VENV_DIR=venv
if [ -d "$VENV_DIR" ]; then
    echo "Entering venv."
    source $VENV_DIR/bin/activate
fi

python3 dalybt_stats.py
