#!/usr/bin/env python3
import argparse
import logging
import os

import requests
from model import FlightUpdate

# Set logger
log = logging.getLogger()
log.setLevel("INFO")
handler = logging.FileHandler("airlines.log")
handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
)
log.addHandler(handler)

# Read env vars related to API connection
AIRLINE_API_URL = os.getenv("AIRLINE_API_URL", "http://localhost:8000")


def analyze_airport_benefits():
    suffix = "/airline/automated-carts-recommendation"
    endpoint = AIRLINE_API_URL + suffix
    try:
        response = requests.get(endpoint)
        if response.ok:
            json_resp = response.json()
            print("Recommended Airports for Automated Carts:")
            for i in range(len(json_resp)):
                print(f"Airport {i+1} - {json_resp[i]}: ")
        else:
            print(f"Error: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Failed to fetch recommendations: {str(e)}")


def print_menu():
    mm_options = {
        1: "analyze airport benefits",
        2: "Exit",
    }
    for key in mm_options.keys():
        print(key, "--", mm_options[key])


def main():
    log.info(
        f"Welcome to airlines catalog. App requests to: {AIRLINE_API_URL}"
    )
    while True:
        print_menu()
        option = int(input("Enter your choice: "))
        print()
        if option == 1:
            analyze_airport_benefits()

        elif option == 2:
            exit(0)

        print()
        input("Press Enter to continue...\n")


if __name__ == "__main__":
    main()
