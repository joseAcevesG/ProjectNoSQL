# cspell: ignore pydgraph DGRAPH
import os

import model
import pydgraph

DGRAPH_URI = os.getenv("DGRAPH_URI", "localhost:9080")


def print_menu():
    mm_options = {
        1: "Create data",
        2: "peek best month for a airport",
        3: "Drop All",
        4: "Exit",
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
        elif option == 2:
            airport = input("Enter the airport: ")
            model.process_data(client, airport)
        elif option == 3:
            model.drop_all(client)
        if option == 4:
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
