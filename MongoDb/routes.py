#!/usr/bin/env python3
import logging
from typing import List

from bson import Regex
from fastapi import APIRouter, Body, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder
from model import *

router = APIRouter()

log = logging.getLogger()
log.setLevel("INFO")
handler = logging.FileHandler("router.log")
handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
)
log.addHandler(handler)


@router.post(
    "/",
    response_description="Post a new airline",
    status_code=status.HTTP_201_CREATED,
    response_model=Airline,
)
def create_airline(request: Request, airline: Airline = Body(...)):
    airline = jsonable_encoder(airline)
    new_airline = request.app.database["airlines"].insert_one(airline)
    created_airline = request.app.database["airlines"].find_one(
        {"_id": new_airline.inserted_id}
    )

    return created_airline


@router.post(
    "/gender",
    response_description="Post a new gender",
    status_code=status.HTTP_201_CREATED,
    response_model=GenderOptions,
)
def create_gender(request: Request, gender: GenderOptions = Body(...)):
    gender = jsonable_encoder(gender)
    new_gender = request.app.database["gender_options"].insert_one(gender)
    created_gender = request.app.database["gender_options"].find_one(
        {"_id": new_gender.inserted_id}
    )

    return created_gender


@router.post(
    "/reason_for_travel",
    response_description="Post a new reason",
    status_code=status.HTTP_201_CREATED,
    response_model=ReasonForTravel,
)
def create_reason(request: Request, reason: ReasonForTravel = Body(...)):
    reason = jsonable_encoder(reason)
    new_reason = request.app.database["reason_for_travels"].insert_one(reason)
    created_reason = request.app.database["reason_for_travels"].find_one(
        {"_id": new_reason.inserted_id}
    )

    return created_reason


@router.post(
    "/accomodation_type",
    response_description="Post a new accomodation",
    status_code=status.HTTP_201_CREATED,
    response_model=AccomodationType,
)
def create_accomodation(
    request: Request, accomodation: AccomodationType = Body(...)
):
    accomodation = jsonable_encoder(accomodation)
    new_accomodation = request.app.database["accomodation_types"].insert_one(
        accomodation
    )
    created_accomodation = request.app.database["accomodation_types"].find_one(
        {"_id": new_accomodation.inserted_id}
    )

    return created_accomodation


@router.post(
    "/transportation_type",
    response_description="Post a new transportation",
    status_code=status.HTTP_201_CREATED,
    response_model=TransportationType,
)
def create_transportation(
    request: Request, transportation: TransportationType = Body(...)
):
    transportation = jsonable_encoder(transportation)
    new_transportation = request.app.database[
        "transportation_types"
    ].insert_one(transportation)
    created_transportation = request.app.database[
        "transportation_types"
    ].find_one({"_id": new_transportation.inserted_id})

    return created_transportation


@router.post(
    "/ticket_type",
    response_description="Post a new ticket",
    status_code=status.HTTP_201_CREATED,
    response_model=TicketType,
)
def create_ticket(request: Request, ticket: TicketType = Body(...)):
    ticket = jsonable_encoder(ticket)
    new_ticket = request.app.database["ticket_type"].insert_one(ticket)
    created_ticket = request.app.database["ticket_type"].find_one(
        {"_id": new_ticket.inserted_id}
    )

    return created_ticket
    delete_flight = request.app.database["airlines"].delete_one({"_id": id})

    if delete_flight.deleted_count:
        return {"message": f"Flight with ID {id} has been deleted"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Flight with ID {id} not found",
    )


@router.get("/automated-carts-recommendation", response_model=List[str])
def analyze_airport_benefits(request: Request):
    # Retrieve all documents (Assuming the dataset is not excessively large; otherwise, consider batching)
    documents = list(
        request.app.database["airlines"].aggregate(
            [
                {
                    "$match": {
                        "transit": {
                            "$in": [
                                "Mobility as a service",
                                "Airport cab",
                                "Public Transportation",
                            ]
                        }
                    }
                },
                {
                    "$group": {
                        "_id": {"from_": "$from_", "transit": "$transit"},
                        "count": {"$sum": 1},
                    }
                },
                {
                    "$group": {
                        "_id": "$_id.from_",
                        "transport_not_private": {"$sum": "$count"},
                    }
                },
                {
                    "$sort": {"transport_not_private": -1}
                },  # Ordena descendente por el conteo de transport_not_private
            ]
        )
    )

    return [doc.get("_id") for doc in documents]
