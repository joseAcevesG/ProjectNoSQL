#!/usr/bin/env python3
# cspell: ignore levelname keyspace
import logging
import os
import random
from datetime import datetime

import model

from cassandra.cluster import Cluster

# Set logger
log = logging.getLogger()
log.setLevel("INFO")
handler = logging.FileHandler("air_quality_analysis.log")
handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
)
log.addHandler(handler)

# Read env vars related to Cassandra App
CLUSTER_IPS = os.getenv("CASSANDRA_CLUSTER_IPS", "localhost")
KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "air_quality")
REPLICATION_FACTOR = os.getenv("CASSANDRA_REPLICATION_FACTOR", "1")


def print_menu():
    mm_options = {
        1: "Show all data",
        2: "Exit",
    }
    for key in mm_options.keys():
        print(key, "--", mm_options[key])


def update_data_entry(session):
    entry_id = input("**** Enter data entry ID to update: ")
    new_value = float(input("**** Enter new arithmetic mean value: "))
    model.update_data_entry(session, entry_id, new_value)
    log.info(f"Data entry {entry_id} updated to {new_value}")


def main():
    log.info("Connecting to Cluster")
    cluster = Cluster(CLUSTER_IPS.split(","))
    session = cluster.connect()

    model.create_keyspace(session, KEYSPACE, REPLICATION_FACTOR)
    session.set_keyspace(KEYSPACE)

    model.create_schema(session)

    while True:
        print_menu()
        option = int(input("Enter your choice: "))
        print()
        if option == 1:
            stateCode = input("Enter state code: ")
            countyCode = input("Enter county code: ")
            parameterName = input("Enter parameter name: ")
            year = int(input("Enter year: "))
            model.get_air_quality_data(
                session, stateCode, countyCode, parameterName, year
            )

        elif option == 2:
            exit(0)

        print()
        input("Press Enter to continue...\n")


if __name__ == "__main__":
    main()
