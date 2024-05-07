#!/usr/bin/env python3
import csv
import uuid

CQL_FILE = "data.cql"
# CSV_FILE = r"C:\Users\chava\OneDrive\Escritorio\NoSQL\ProjectNoSQL\annual_conc_by_monitor_2023.csv"  # Two directories up from the script location
CSV_FILE = r"C:\Users\chava\OneDrive\Escritorio\NoSQL\ProjectNoSQL\Cassandra\tools\temp.csv"  # Two directories up from the script location


def cql_stmt_generator():
    air_quality_stmt = "INSERT INTO air_quality_data (state_code, county_code, city_name, latitude, longitude, year, parameter_name, units_of_measure, arithmetic_mean, max_value, max_datetime) VALUES ('{}', '{}', '{}', {}, {}, {}, '{}', '{}', {}, {}, '{}');"

    with open(CSV_FILE, newline="") as csvfile, open(CQL_FILE, "w") as cqlfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            state_code = row["State Code"]
            county_code = row["County Code"]
            city_name = row["City Name"]
            latitude = row["Latitude"]
            longitude = row["Longitude"]
            year = row["Year"]
            parameter_name = row["Parameter Name"]
            units_of_measure = row["Units of Measure"]
            arithmetic_mean = row["Arithmetic Mean"]
            max_value = row["1st Max Value"]
            max_datetime = row["1st Max DateTime"]

            cqlfile.write(
                air_quality_stmt.format(
                    state_code,
                    county_code,
                    city_name,
                    latitude,
                    longitude,
                    year,
                    parameter_name,
                    units_of_measure,
                    arithmetic_mean,
                    max_value,
                    max_datetime,
                )
            )
            cqlfile.write("\n")


def main():
    cql_stmt_generator()


if __name__ == "__main__":
    main()
