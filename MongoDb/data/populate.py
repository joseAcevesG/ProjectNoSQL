#!/usr/bin/env python3
import csv
import requests

BASE_URL = "http://localhost:8000"

def main():
    with open("flight_passengers.csv") as fd:
        flight_passengers_csv = csv.DictReader(fd)
        for flight in flight_passengers_csv:
            del flight["flightID"]
            flight["airline"] = flight["airline"].split("/")
            x = requests.post(BASE_URL+"/flight", json=flight)
            if not x.ok:
                print(f"Failed to post flight {x} - {flight}")

if __name__ == "__main__":
    main()