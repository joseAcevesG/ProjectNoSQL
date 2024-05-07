#!/usr/bin/env python3
import csv

import requests

BASE_URL = "http://localhost:8000"


def main():
    # genders = ["male", "female", "unspecified", "undisclosed"]
    # genders_id = {}
    # for gender in genders:
    #     # Realizar la solicitud POST para crear un nuevo género
    #     response = requests.post(
    #         BASE_URL + "/airline/gender", json={"gender": gender}
    #     )
    #     # Verificar si la solicitud fue exitosa (código de estado 201)
    #     if response.status_code == 201:
    #         # Obtener el ID del nuevo género creado
    #         new_gender_id = response.json().get("_id")
    #         # Almacenar el ID en el diccionario genders_id
    #         genders_id[gender] = new_gender_id
    #     else:
    #         print(f"No se pudo crear el género '{gender}': {response.text}")
    # print("IDs de género obtenidos:", genders_id)

    # reason_for_travel = ["vacation_pleasure", "business_work", "back_home"]
    # reason_for_travel_id = {}
    # for reason in reason_for_travel:
    #     # Realizar la solicitud POST para crear una nueva razón de viaje
    #     response = requests.post(
    #         BASE_URL + "/airline/reason_for_travel", json={"reason": reason}
    #     )

    #     # Verificar si la solicitud fue exitosa (código de estado 201)
    #     if response.status_code == 201:
    #         # Obtener el ID de la nueva razón de viaje creada
    #         new_reason_id = response.json().get("_id")

    #         # Almacenar el ID en el diccionario reasons_for_travel_id
    #         reason_for_travel_id[reason] = new_reason_id
    #     else:
    #         print(
    #             f"No se pudo crear la razón de viaje '{reason}': {response.text}"
    #         )

    # print("IDs de razón de viaje obtenidos:", reason_for_travel_id)

    # accomodation_type = [
    #     "hotel",
    #     "short_term_homestay",
    #     "home",
    #     "friend_family",
    # ]
    # accomodation_type_id = {}
    # for accomodation in accomodation_type:
    #     # Realizar la solicitud POST para crear una nueva razón de viaje
    #     response = requests.post(
    #         BASE_URL + "/airline/accomodation_type",
    #         json={"accomodation": accomodation},
    #     )

    #     # Verificar si la solicitud fue exitosa (código de estado 201)
    #     if response.status_code == 201:
    #         # Obtener el ID de la nueva razón de viaje creada
    #         accomodation_type_id = response.json().get("_id")

    #         # Almacenar el ID en el diccionario reasons_for_travel_id
    #         accomodation_type_id[accomodation] = accomodation_type_id
    #     else:
    #         print(
    #             f"No se pudo crear la razón de viaje '{reason}': {response.text}"
    #         )

    # print("IDs de razón de viaje obtenidos:", accomodation_type_id)

    # transportation_type = [
    #     "airpot_cab",
    #     "car_rental",
    #     "mobility_as_a_service",
    #     "public_transportation",
    #     "pickup",
    #     "own_car",
    # ]
    # transportation_type_id = {}
    # for transportation in transportation_type:
    #     # Realizar la solicitud POST para crear un nuevo tipo de transporte
    #     response = requests.post(
    #         BASE_URL + "/airline/transportation_type",
    #         json={"transportation": transportation},
    #     )

    #     # Verificar si la solicitud fue exitosa (código de estado 201)
    #     if response.status_code == 201:
    #         # Obtener el ID del nuevo tipo de transporte creado
    #         new_transportation_id = response.json().get("_id")

    #         # Almacenar el ID en el diccionario transportation_type_id
    #         transportation_type_id[transportation] = new_transportation_id
    #     else:
    #         print(
    #             f"No se pudo crear el tipo de transporte '{transportation}': {response.text}"
    #         )

    # print("IDs de tipos de transporte obtenidos:", transportation_type_id)

    # ticket_type = ["economy", "business", "first_class"]
    # ticket_type_id = {}
    # for ticket in ticket_type:
    #     # Realizar la solicitud POST para crear un nuevo tipo de boleto
    #     response = requests.post(
    #         BASE_URL + "/airline/ticket_type", json={"ticket": ticket}
    #     )

    #     # Verificar si la solicitud fue exitosa (código de estado 201)
    #     if response.status_code == 201:
    #         # Obtener el ID del nuevo tipo de boleto creado
    #         new_ticket_id = response.json().get("_id")

    #         # Almacenar el ID en el diccionario ticket_type_id
    #         ticket_type_id[ticket] = new_ticket_id
    #     else:
    #         print(
    #             f"No se pudo crear el tipo de boleto '{ticket}': {response.text}"
    #         )

    # print("IDs de tipos de boleto obtenidos:", ticket_type_id)

    with open("flight_passengers.csv") as fd:
        flight_passengers_csv = csv.DictReader(fd)
        for row in flight_passengers_csv:
            # Mapping the CSV keys to the desired JSON keys and formatting values
            flight_data = {
                "airline": row["airline"],
                "from_": row["from"],
                "to": row["to"],
                "day": int(row["day"]),
                "month": int(row["month"]),
                "year": int(row["year"]),
                "duration": int(row["duration"]),
                "age": int(row["age"]),
                "gender": (
                    row["gender"].lower()
                    if row["gender"].lower() != "unspecified"
                    or row["gender"].lower() != "undisclosed"
                    else None
                ),
                "reason": row["reason"].replace("/", "_").lower(),
                "stay": row["stay"],
                "transit": row["transit"],
                "connection": row["connection"] == "True",
                "wait": int(row["wait"]),
                "ticket": row["ticket"],
                "checked_bags": int(row["checked_bags"]),
                "carry_on": row["carry_on"] == "True",
            }
            x = requests.post(BASE_URL + "/airline", json=flight_data)
            if not x.ok:
                print(f"Failed to post flight {x} - {flight_data}")


if __name__ == "__main__":
    main()
