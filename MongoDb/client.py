#!/usr/bin/env python3
import argparse
import logging
import os
import requests
from model import FlightUpdate


# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('airlines.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars related to API connection
AIRLINE_API_URL = os.getenv("AIRLINE_API_URL", "http://localhost:8000")



def print_airline(airline):
    for k in airline.keys():
        print(f"{k}: {airline[k]}")
    print("="*50)

def list_airlines(rating):
    suffix = "/airline"
    endpoint = AIRLINE_API_URL + suffix
    params = {
        "rating": rating
    }
    response = requests.get(endpoint, params=params)
    if response.ok:
        json_resp = response.json()
        for airline in json_resp:
            print_airline(airline)
    else:
        print(f"Error: {response}")


def get_airline_by_id(id):
    suffix = f"/airline/{id}"
    endpoint = AIRLINE_API_URL + suffix
    response = requests.get(endpoint)
    if response.ok:
        json_resp = response.json()
        print_airline(json_resp)
    else:
        print(f"Error: {response}")


def update_airline(id):
    suffix = f"/airline/{id}"
    endpoint = AIRLINE_API_URL + suffix
    response = requests.get(endpoint)

    if response.ok:
        json_resp = response.json()
        for i in json_resp.keys():
            if i == "_id":
                continue
            elif i == "airlines":
                print(f"Current airlines: {json_resp[i]}, press enter button to keep the current value")
                print("Write the new airlines separated by spaces")
                print(f"update {i} (current: {json_resp[i]}): ", end="")
                new_author = input()
                if new_author:
                    json_resp[i] = new_author.split(" ")
            else:
                print(f"current {i}: {json_resp[i]}, press enter button to keep the current value")
                print(f"update {i} (current: {json_resp[i]}): ", end="")
                new_value = input()
                if new_value:
                    json_resp[i] = new_value
        updateBook = FlightUpdate(**json_resp)    
        response = requests.put(endpoint, json=updateBook.dump())

    else:
        print(f"Error: {response}")


def delete_airline(id):
    suffix = f"/airline/{id}"
    endpoint = AIRLINE_API_URL + suffix
    response = requests.delete(endpoint)
    if response.ok:
        json_resp = response.json()
        print(json_resp)
    else:
        print(f"Error: {response}")

def recommend_automated_carts():
    suffix = "airline/automated-carts-recommendation"
    endpoint = AIRLINE_API_URL + suffix
    try:
        response = requests.get(endpoint)
        if response.ok:
            json_resp = response.json()
            print("Recommended Airports for Automated Carts:")
            for item in json_resp:
                print(f"Airport: {item['airport']}, Benefit Score: {item['benefit_score']}")
        else:
            print(f"Error: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Failed to fetch recommendations: {str(e)}")

def main():
    log.info(f"Welcome to airlines catalog. App requests to: {AIRLINE_API_URL}")

    parser = argparse.ArgumentParser()

    list_of_actions = ["search", "get", "update", "delete"]
    parser.add_argument("action", choices=list_of_actions,
            help="Action to be user for the airlines library")
    parser.add_argument("-i", "--id",
            help="Provide a airline ID which related to the airline action", default=None)
    parser.add_argument("-r", "--rating",
            help="Search parameter to look for airlines with average rating equal or above the param (0 to 5)", default=None)
    parser.add_argument(
        "-l",
        "--limit",
        help="Limit the number of airlines to be shown",
        default=None,
        type=int,
    )

    args = parser.parse_args()

    if args.id and not args.action in ["get", "update", "delete"]:
        log.error(f"Can't use arg id with action {args.action}")
        exit(1)

    if args.rating and args.action != "search":
        log.error(f"Rating arg can only be used with search action")
        exit(1)

    if args.action == "update" and not args.id:
        log.error(f"Update action requires an id")
        print(f"Update action requires an id")
        exit(1)

    if args.action == "delete" and not args.id:
        log.error(f"Delete action requires an id")
        print(f"Delete action requires an id")
        exit(1)

    if args.action == "search":
        list_airlines(args.rating)
    elif args.action == "get" and args.id:
        get_airline_by_id(args.id)
    elif args.action == "update":
        update_airline(args.id)
    elif args.action == "delete":
        delete_airline(args.id)
    elif args.action == "recommend":
        recommend_automated_carts()

if __name__ == "__main__":
    main()