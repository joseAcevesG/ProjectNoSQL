#!/usr/bin/env python3
import os

import model
import pydgraph

DGRAPH_URI = os.getenv("DGRAPH_URI", "localhost:9080")


def print_menu():
    mm_options = {
        1: "Create data",
        2: "Search event",
        3: "Search person",
        4: "Count events",
        5: "Search events ordered by date",
        6: "Delete event",
        7: "Drop All",
        8: "Exit",
    }
    for key in mm_options.keys():
        print(key, "--", mm_options[key])


def create_client_stub():
    return pydgraph.DgraphClientStub(DGRAPH_URI)


def create_client(client_stub):
    return pydgraph.DgraphClient(client_stub)


def close_client_stub(client_stub):
    client_stub.close()


def main():
    # Init Client Stub and Dgraph Client
    client_stub = create_client_stub()
    client = create_client(client_stub)

    # Create schema
    model.set_schema(client)

    """options: 
    search_event
    search_person
    count_events
    search_events_ordered_by_date"""

    while True:
        print_menu()
        option = int(input("Enter your choice: "))
        if option == 1:
            model.create_data(client)
        if option == 2:
            event = input("Event: ")
            model.search_event(client, event)
        if option == 3:
            age = input("Age: ")
            model.search_person(client, age)
        if option == 4:
            model.count_events(client)
        if option == 5:
            pagination = input("Number of events: ")
            model.search_events_ordered_by_date(client, pagination)
        if option == 6:
            event = input("Event: ")
            model.delete_event(client, event)
        if option == 7:
            model.drop_all(client)
        if option == 8:
            model.drop_all(client)
            close_client_stub(client_stub)
            exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error: {}".format(e))


""" this laboratory help me to understand how to dgraph with python, 
also how to create a schema, insert data, query data, delete data and drop all data.
this is going to be handy for the projects that need to use dgraph as a database."""
