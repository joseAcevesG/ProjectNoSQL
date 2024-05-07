#!/usr/bin/env python3
import csv
import os

CQL_FILE = "data.cql"
# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Update the CSV_FILE path
CSV_FILE = os.path.join(current_dir, "annual_conc_by_monitor_2023.csv")
# CSV_FILE = os.path.join(current_dir, "temp.csv")


def cql_stmt_generator():
    # Define la sentencia de inserción con todos los campos necesarios
    air_quality_stmt = (
        "INSERT INTO air_quality_data (state_code, county_code, city_name, latitude, longitude, year, parameter_name, arithmetic_mean, "
        "arithmetic_standard_deviation, first_max_value, second_max_value, third_max_value, fourth_max_value, first_max_datetime, "
        "second_max_datetime, third_max_datetime, fourth_max_datetime, pollutant_standard) "
        "VALUES ('{}', '{}', '{}', {}, {}, {}, '{}', {}, {}, {}, {}, {}, {}, '{}', '{}', '{}', '{}', '{}');"
    )

    # Abre los archivos CSV y CQL para leer y escribir respectivamente
    with open(CSV_FILE, newline="") as csvfile, open(CQL_FILE, "w") as cqlfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Prepara y escribe la declaración CQL para cada fila
            cqlfile.write(
                air_quality_stmt.format(
                    row["State Code"],
                    row["County Code"],
                    row["City Name"],
                    float(row["Latitude"]),
                    float(row["Longitude"]),
                    int(row["Year"]),
                    row["Parameter Name"],
                    float(row["Arithmetic Mean"]) if row["Arithmetic Mean"] else "NULL",
                    (
                        float(row["Arithmetic Standard Dev"])
                        if row["Arithmetic Standard Dev"]
                        else "NULL"
                    ),
                    float(row["1st Max Value"]) if row["1st Max Value"] else "NULL",
                    float(row["2nd Max Value"]) if row["2nd Max Value"] else "NULL",
                    float(row["3rd Max Value"]) if row["3rd Max Value"] else "NULL",
                    float(row["4th Max Value"]) if row["4th Max Value"] else "NULL",
                    row["1st Max DateTime"] if row["1st Max DateTime"] else "NULL",
                    row["2nd Max DateTime"] if row["2nd Max DateTime"] else "NULL",
                    row["3rd Max DateTime"] if row["3rd Max DateTime"] else "NULL",
                    row["4th Max DateTime"] if row["4th Max DateTime"] else "NULL",
                    row["Pollutant Standard"],
                )
            )
            cqlfile.write("\n")


def main():
    cql_stmt_generator()


if __name__ == "__main__":
    main()
