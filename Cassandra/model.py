#!/usr/bin/env python3

import logging

import pandas as pd

log = logging.getLogger()

CREATE_KEYSPACE = """
        CREATE KEYSPACE IF NOT EXISTS {}
        WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': {} }}
"""
# INSERT INTO air_quality_data (state_code, county_code, city_name, latitude, longitude, year, parameter_name, units_of_measure, arithmetic_mean, max_value, max_datetime) VALUES ('01', '003', 'Fairhope', 30.497478, -87.880258, '2023', 'PM2.5 - Local Conditions', 'Micrograms/cubic meter (LC)', 7.662048, 18.9, '2023-06-29 00:00');


CREATE_AIR_QUALITY_TABLE = """
    CREATE TABLE IF NOT EXISTS air_quality_data (
        state_code TEXT,
        county_code TEXT,
        city_name TEXT,
        latitude DOUBLE,
        longitude DOUBLE,
        year INT,
        parameter_name TEXT,
        units_of_measure TEXT,
        arithmetic_mean DOUBLE,
        max_value DOUBLE,
        max_datetime TIMESTAMP,
        PRIMARY KEY ((state_code), county_code, year, parameter_name, max_datetime)
    )
"""

SELECT_AIR_QUALITY_DATA = """
    SELECT state_code, county_code, city_name, latitude, longitude, year, parameter_name, units_of_measure, arithmetic_mean, max_value, max_datetime
    FROM air_quality_data
    WHERE state_code = ?
    AND county_code = ?
    AND year = ?
    AND parameter_name = ?
"""


def create_keyspace(session, keyspace, replication_factor):
    log.info(
        f"Creating keyspace: {keyspace} with replication factor {replication_factor}"
    )
    session.execute(CREATE_KEYSPACE.format(keyspace, replication_factor))


def create_schema(session):
    log.info("Creating model schema")
    session.execute(CREATE_AIR_QUALITY_TABLE)


def get_air_quality_data(session, state_code, county_code, parameter_name, year):
    logging.info(
        f"Retrieving air quality data for state: {state_code}, county: {county_code}, parameter: {parameter_name}, year: {year}"
    )
    stmt = session.prepare(
        "SELECT * FROM air_quality_data WHERE state_code=? AND county_code=? AND year=? AND parameter_name=?"
    )
    rows = session.execute(
        stmt,
        [state_code, county_code, year, parameter_name],
    )

    for row in rows:
        print(f"=== Air Quality Data ===")
        print(f"- State Code: {row.state_code}")
        print(f"- County Code: {row.county_code}")
        print(f"- Latitude: {row.latitude}")
        print(f"- Longitude: {row.longitude}")
        print(f"- Parameter Name: {row.parameter_name}")
        print(f"- Year: {row.year}")
        print(f"- Units of Measure: {row.units_of_measure}")
        print(f"- Arithmetic Mean: {row.arithmetic_mean}")
        print(f"- Max Value: {row.max_value}")
        print(f"- Max DateTime: {row.max_datetime}")


"""     for row in rows:
        print(f"=== Air Quality Data ===")
        print(f"- State Code: {row.state_code}")
        print(f"- County Code: {row.county_code}")
        print(f"- Latitude: {row.latitude}")
        print(f"- Longitude: {row.longitude}")
        print(f"- Parameter Name: {row.parameter_name}")
        print(f"- Year: {row.year}")
        print(f"- Units of Measure: {row.units_of_measure}")
        print(f"- Arithmetic Mean: {row.arithmetic_mean}")
        print(f"- Max Value: {row.max_value}")
        print(f"- Max DateTime: {row.max_datetime}") """
