# cspell: ignore pydgraph homestay iterrows isna nquads uids orderasc
import json
from collections import Counter

import pandas as pd
import pydgraph


def set_schema(client):
    schema = """
    type Airline {
    name
    operates
}

type Flight {
    day
    month
    year
    duration
    ticket
     transit
    connection
    wait
    departs_from
    arrives_at
}

type Airport {
    name
}

type Passenger {
    age
    gender
    books
    travels_for
    carries
}

type Trip {
    reason
    stay
}

type Luggage {
    checked_bags
    carry_on
}

name: string @index(exact) .
age: int @index(int) .
gender: string @index(exact) .
day: int .
month: string @index(exact).
year: int @index(int) .
duration: int .
ticket: string @index(exact) .
reason: string @index(exact) .
stay: string @index(exact).
transit: string @index(exact) .
connection: bool .
wait: int .
checked_bags: int .
carry_on: bool .

operates: [uid] @reverse .
departs_from: uid @reverse .
arrives_at: uid @reverse .
books: [uid] @reverse .
travels_for: [uid] @reverse .
carries: [uid] @reverse .
    """
    return client.alter(pydgraph.Operation(schema=schema))


def prepare_mutation(file_path):
    df = pd.read_csv(file_path)

    airlines = set(df["airline"])
    airports = set(df["from"]).union(set(df["to"]))

    airline_mutations = [
        f'_:airline_{airline.replace(" ", "_")} <type> "Airline" .\n_:airline_{airline.replace(" ", "_")} <name> "{airline}" .'
        for airline in airlines
    ]
    airport_mutations = [
        f'_:airport_{airport.replace(" ", "_")} <type> "Airport" .\n_:airport_{airport.replace(" ", "_")} <name> "{airport}" .'
        for airport in airports
    ]

    reasons = ["On vacation/Pleasure", "Business/Work", "Back home"]
    stays = ["Hotel", "Short-term homestay", "Home", "Friend/Family"]
    trip_combinations = []
    for reason in reasons:
        if reason == "Back home":
            trip_combinations.append((reason, "Home"))
        else:
            for stay in stays:
                trip_combinations.append((reason, stay))
    trip_mutations = [
        f'_:trip_{reason.replace(" ", "_").replace("/", "")}_{stay.replace(" ", "_").replace("/", "")} <type> "Trip" .\n_:trip_{reason.replace(" ", "_").replace("/", "")}_{stay.replace(" ", "_").replace("/", "")} <reason> "{reason}" .\n_:trip_{reason.replace(" ", "_").replace("/", "")}_{stay.replace(" ", "_").replace("/", "")} <stay> "{stay}" .'
        for reason, stay in trip_combinations
    ]

    flight_mutations = []
    for index, row in df.iterrows():
        trip_node = f'trip_{row["reason"].replace(" ", "_").replace("/", "")}_{row["stay"].replace(" ", "_").replace("/", "")}'
        flight_mutations.append(
            f"""_:flight{index} <type> "Flight" .
_:flight{index} <day> "{row['day']}" .
_:flight{index} <month> "{row['month']}" .
_:flight{index} <year> "{row['year']}" .
_:flight{index} <duration> "{row['duration']}" .
_:flight{index} <ticket> "{row['ticket']}" .
_:airline_{row['airline'].replace(" ", "_")} <operates> _:flight{index} .
_:flight{index} <departs_from> _:airport_{row['from'].replace(" ", "_")} .
_:flight{index} <arrives_at> _:airport_{row['to'].replace(" ", "_")} .
_:flight{index} <connection> "{('true' if row['connection'] else 'false')}" .
_:flight{index} <transit> "{row['transit'] if not pd.isna(row['transit']) else ''}" .
_:flight{index} <wait> "{row['wait']}" .
_:passenger{index} <type> "Passenger" .
_:passenger{index} <age> "{row['age']}" .
_:passenger{index} <gender> "{row['gender']}" .
_:passenger{index} <books> _:flight{index} .
_:passenger{index} <travels_for> _:{trip_node} .
_:luggage{index} <type> "Luggage" .
_:luggage{index} <checked_bags> "{row['checked_bags']}" .
_:luggage{index} <carry_on> "{('true' if row['carry_on'] else 'false')}" .
_:passenger{index} <carries> _:luggage{index} .
_:transit{index} <type> "Transit" .
"""
        )
    all_mutations = "\n".join(
        airline_mutations + airport_mutations + trip_mutations + flight_mutations
    )
    return all_mutations


def create_data(client):
    mutations = prepare_mutation("flight_passengers.csv")

    txn = client.txn()
    try:
        response = txn.mutate(set_nquads=mutations)

        commit_response = txn.commit()
        print(f"Commit Response: {commit_response}")
        print(f"UIDs: {response.uids}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        txn.discard()


def extract_month_transit(data):
    months = [item["month"] for item in data["all"][0]["~arrives_at"]]
    month_count = Counter(months)
    sorted_months = sorted(month_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_months


""" {
  peak_months(func: eq(name, "GDL")){
    ~arrives_at @filter(eq(transit, "Mobility as a service")){
        month
	    }
    }
} """


def bests_month_transit(client, name):
    query = """
    query search_peak_months($a: string) {
        all(func: eq(name, $a)) {
            uid
            name
            ~arrives_at @filter(eq(transit, "Mobility as a service")) {
                month
            }
            place_in {
                uid
                name
                location
            }
            ~organizes {
                uid
                name
            }
        }
    }
    """
    variables = {"$a": name}
    res = client.txn(read_only=True).query(query, variables=variables)
    ppl = json.loads(res.json)
    return extract_month_transit(ppl)


def extract_month_reason(data):

    filtered_data = [
        entry for entry in data["all"][0]["~arrives_at"] if "~books" in entry
    ]
    months = [item["month"] for item in filtered_data]
    month_count = Counter(months)
    sorted_months = sorted(month_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_months


""" {
  peak_travel_reasons(func: eq(name, "GDL")){
    ~arrives_at {
    	month
    	~books{
    		travels_for @filter(eq(reason, "On vacation/Pleasure")and (eq(stay, "Short-term homestay") or eq(stay, "Hotel"))){
          reason
          stay
        }
      }
  	}
  }
} """


def best_month_reason(client, name):
    query = """
    query search_peak_travel_reasons($a: string) {
        all(func: eq(name, $a)) {
            uid
            name
            ~arrives_at {
                month
                ~books{
                    travels_for @filter(eq(reason, "On vacation/Pleasure") and (eq(stay, "Short-term homestay") or eq(stay, "Hotel"))) {
                        reason
                        stay
                    }
                }
            }
        }
    }
    """
    variables = {"$a": name}
    res = client.txn(read_only=True).query(query, variables=variables)
    ppl = json.loads(res.json)
    return extract_month_reason(ppl)


def find_common_best_month(list1, list2):
    dict1 = dict(list1)
    dict2 = dict(list2)

    common_months = set(dict1.keys()) & set(dict2.keys())
    combined_frequencies = {month: dict1[month] + dict2[month] for month in common_months}

    best_month = max(combined_frequencies, key=combined_frequencies.get, default=None)

    return best_month


def process_data(client, name):
    months_transit = bests_month_transit(client, name)
    months_reason = best_month_reason(client, name)
    print(f"the best moth for putting advertisement for {name} is ", end="")
    match find_common_best_month(months_transit, months_reason):
        case "1":
            print("January")
        case "2":
            print("February")
        case "3":
            print("March")
        case "4":
            print("April")
        case "5":
            print("May")
        case "6":
            print("June")
        case "7":
            print("July")
        case "8":
            print("August")
        case "9":
            print("September")
        case "10":
            print("October")
        case "11":
            print("November")
        case "12":
            print("December")

def drop_all(client):
    return client.alter(pydgraph.Operation(drop_all=True))


if __name__ == "__main__":
    # Run the main function
    file_path = "flight_passengers.csv"
    mutations = prepare_mutation(file_path)
    print(mutations)
