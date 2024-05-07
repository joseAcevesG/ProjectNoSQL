#!/usr/bin/env python3

import logging

log = logging.getLogger()

CREATE_KEYSPACE = """
        CREATE KEYSPACE IF NOT EXISTS {}
        WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': {} }}
"""

CREATE_AIR_QUALITY_TABLE = """
    CREATE TABLE IF NOT EXISTS air_quality_data (
        state_code TEXT,
        county_code TEXT,
        city_name TEXT,
        latitude DOUBLE,
        longitude DOUBLE,
        year INT,
        parameter_name TEXT,
        arithmetic_mean DOUBLE,
        arithmetic_standard_deviation DOUBLE,
        first_max_value DOUBLE,
        second_max_value DOUBLE,
        third_max_value DOUBLE,
        fourth_max_value DOUBLE,
        first_max_datetime TIMESTAMP,
        second_max_datetime TIMESTAMP,
        third_max_datetime TIMESTAMP,
        fourth_max_datetime TIMESTAMP,
        Pollutant_standard TEXT,
        PRIMARY KEY ((state_code, county_code, city_name), year, parameter_name, first_max_datetime)
    )
"""

SELECT_AIR_QUALITY_DATA = """
    SELECT state_code, county_code, city_name, latitude, longitude, year, parameter_name, arithmetic_mean, arithmetic_standard_deviation, first_max_value, second_max_value, third_max_value, fourth_max_value, first_max_datetime, second_max_datetime, third_max_datetime, fourth_max_datetime, pollutant_standard
    FROM air_quality_data
    WHERE state_code = ?
    AND county_code = ?
    AND city_name = ?
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


def evaluate_air_quality(arithmetic_mean, max_values, pollutant_standard):
    # Definir los umbrales de calidad del aire para el ozono según la EPA
    # Estos valores son ejemplos y deben ser verificados y ajustados según las regulaciones locales
    thresholds = {
        "Ozone 8-hour 2015": 0.070,  # partes por millón
        "Ozone 1-hour 1979": 0.120,  # partes por millón
    }

    quality = "Good"
    standard_limit = thresholds.get(pollutant_standard, None)

    if standard_limit is None:
        return "No standard limit available for this pollutant."

    # Evaluar la media aritmética
    if arithmetic_mean > standard_limit:
        quality = "Unhealthy"

    # Evaluar los valores máximos
    for value in max_values:
        if value > standard_limit:
            quality = "Unhealthy"
            break

    return f"The air quality for {pollutant_standard} is {quality} based on an arithmetic mean of {arithmetic_mean} and maximum values of {max_values}."


def get_air_quality_data(
    session, state_code, county_code, city_name, year, parameter_name
):
    log.info(
        f"Retrieving air quality data for {city_name}, {county_code}, {state_code} in {year} regarding {parameter_name}"
    )
    stmt = session.prepare(SELECT_AIR_QUALITY_DATA)

    # Ejecutamos la consulta con los parámetros necesarios
    rows = session.execute(
        stmt, [state_code, county_code, city_name, year, parameter_name]
    )

    # Imprimimos los resultados obtenidos
    for row in rows:
        print(
            evaluate_air_quality(
                row.arithmetic_mean,
                [
                    row.first_max_value,
                    row.second_max_value,
                    row.third_max_value,
                    row.fourth_max_value,
                ],
                row.pollutant_standard,
            )
        )
