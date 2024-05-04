# cspell: ignore pydgraph dgraph tomasa uids ITESO
import datetime
import json
from io import StringIO

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
    transits_through
}

type Trip {
    reason
    stay
}

type Luggage {
    checked_bags
    carry_on
}

type Transit {
    transit
    connection
    wait
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
stay: string .
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
transits_through: [uid] @reverse .

    """
    return client.alter(pydgraph.Operation(schema=schema))


def prepare_dgraph_mutation(file_path):
    # Leemos los datos desde el archivo CSV
    # df = pd.read_csv(file_path)

    # temp
    string_data = """airline,from,to,day,month,year,duration,age,gender,reason,stay,transit,connection,wait,ticket,checked_bags,carry_on
American Airlines,LAX,SJC,9,5,2015,872,58,male,Business/Work,Friend/Family,Mobility as a service,False,0,First Class,1,True
Alaska,LAX,PDX,13,9,2022,660,48,undisclosed,Back Home,Home,Mobility as a service,False,0,Economy,0,False
Delta Airlines,LAX,JFK,24,4,2019,601,22,male,On vacation/Pleasure,Short-term homestay,,True,289,Economy,1,True
Volaris,GDL,JFK,11,12,2014,427,11,undisclosed,On vacation/Pleasure,Home,Public Transportation,False,0,First Class,0,False
Volaris,LAX,PDX,2,12,2017,458,86,unspecified,On vacation/Pleasure,Hotel,,True,201,Economy,3,False
Aeromexico,LAX,JFK,6,6,2014,933,19,undisclosed,Business/Work,Short-term homestay,,True,333,Business,0,False
Alaska,JFK,LAX,25,6,2017,34,67,undisclosed,Back Home,Home,Mobility as a service,False,0,First Class,2,True
Alaska,JFK,PDX,22,8,2017,981,35,undisclosed,On vacation/Pleasure,Hotel,,True,168,Business,3,True
Aeromexico,LAX,PDX,26,10,2017,469,76,undisclosed,Back Home,Home,Public Transportation,False,0,Economy,3,False
Volaris,JFK,GDL,18,5,2016,119,61,male,On vacation/Pleasure,Friend/Family,Mobility as a service,False,0,Business,3,False
"""
    data = StringIO(string_data)

    # Leemos los datos usando pandas
    df = pd.read_csv(data)

    # Identificamos aerolíneas y aeropuertos únicos
    airlines = set(df["airline"])
    airports = set(df["from"]).union(set(df["to"]))

    # Preparamos las mutaciones para aerolíneas y aeropuertos
    airline_mutations = [
        f'_:airline_{airline.replace(" ", "_")} <type> "Airline" .\n_:airline_{airline.replace(" ", "_")} <name> "{airline}" .'
        for airline in airlines
    ]
    airport_mutations = [
        f'_:airport_{airport.replace(" ", "_")} <type> "Airport" .\n_:airport_{airport.replace(" ", "_")} <name> "{airport}" .'
        for airport in airports
    ]

    # Crear nodos Trip estáticos
    reasons = ["On vacation/Pleasure", "Business/Work", "Back home"]
    stays = ["Hotel", "Short-term homestay", "Home", "Friend/Family"]
    trip_combinations = []
    for reason in reasons:
        if reason == "Back home":
            # Solo agregar combinación con "Home" para "Back home"
            trip_combinations.append((reason, "Home"))
        else:
            # Todas las combinaciones para otras razones
            for stay in stays:
                trip_combinations.append((reason, stay))
    trip_mutations = [
        f'_:trip_{reason.replace(" ", "_").replace("/", "")}_{stay.replace(" ", "_").replace("/", "")} <type> "Trip" .\n_:trip_{reason.replace(" ", "_").replace("/", "")}_{stay.replace(" ", "_").replace("/", "")} <reason> "{reason}" .\n_:trip_{reason.replace(" ", "_").replace("/", "")}_{stay.replace(" ", "_").replace("/", "")} <stay> "{stay}" .'
        for reason, stay in trip_combinations
    ]

    # Preparar mutaciones para vuelos, pasajeros, equipaje y tránsito
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
_:transit{index} <transit> "{row['transit'] if not pd.isna(row['transit']) else ''}" .
_:transit{index} <connection> "{('true' if row['connection'] else 'false')}" .
_:transit{index} <wait> "{row['wait']}" .
_:passenger{index} <transits_through> _:transit{index} .
"""
        )
    all_mutations = "\n".join(
        airline_mutations + airport_mutations + trip_mutations + flight_mutations
    )
    return all_mutations


def create_data(client):
    mutations = prepare_dgraph_mutation("flight_passengers.csv")

    # Creamos una nueva transacción
    txn = client.txn()
    try:
        # Usamos las mutaciones preparadas
        response = txn.mutate(set_nquads=mutations)

        # Confirmamos la transacción
        commit_response = txn.commit()
        print(f"Commit Response: {commit_response}")
        print(f"UIDs: {response.uids}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        txn.discard()


def delete_event(client, name):
    # Create a new transaction.
    txn = client.txn()
    try:
        query1 = """query search_event($a: string) {
            all(func: eq(name, $a)) {
               uid
            }
        }"""
        variables1 = {"$a": name}
        res1 = client.txn(read_only=True).query(query1, variables=variables1)
        ppl1 = json.loads(res1.json)
        for event in ppl1["all"]:
            print("UID: " + event["uid"])
            txn.mutate(del_obj=event)
            print(f"{name} deleted")
        commit_response = txn.commit()
        print(commit_response)
    finally:
        txn.discard()


def search_event(client, name):
    query = """
    query search_event($a: string) {
        all(func: eq(name, $a)) {
            uid
            name
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

    # Print results.
    print(f"Number of people named {name}: {len(ppl['all'])}")
    print(f"Data associated with {name}:\n{json.dumps(ppl, indent=2)}")


def search_person(client, age):
    query = """query search_person($a: int) {
        all(func: gt(age, $a), orderasc: age) {
        uid
        name
        age
        }
    }"""

    variables = {"$a": age}
    res = client.txn(read_only=True).query(query, variables=variables)
    ppl = json.loads(res.json)

    # Print results.
    print(f"Number of people older than {age}: {len(ppl['all'])}")
    print(f"Data associated with people older than {age}:\n{json.dumps(ppl, indent=2)}")


def count_events(client):
    query = """query count_events {
        all(func: type(Organizations)) {
        uid
        name
        number_of_events: count(organizes)
        }
    }"""

    res = client.txn(read_only=True).query(query)
    ppl = json.loads(res.json)

    # Print results.
    print(f"Number of organizations: {len(ppl['all'])}")
    print(f"Data associated with organizations:\n{json.dumps(ppl, indent=2)}")


def search_events_ordered_by_date(client, pagination):
    query = f"""query search_events_ordered_by_date {{
        all(func: type(Event), orderasc: date, first: {pagination}) {{
        uid
        name
        date
        }}
    }}"""

    res = client.txn(read_only=True).query(query)
    ppl = json.loads(res.json)

    # Print results.
    print(f"Number of events: {len(ppl['all'])}")
    print(f"Data associated with events:\n{json.dumps(ppl, indent=2)}")


def drop_all(client):
    return client.alter(pydgraph.Operation(drop_all=True))


if __name__ == "__main__":
    # Run the main function
    file_path = "flight_passengers.csv"
    mutations = prepare_dgraph_mutation(file_path)
    print(mutations)
