#!/usr/bin/env python3
from typing import List

from bson import Regex
from fastapi import APIRouter, Body, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder
from model import *

router = APIRouter()


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


@router.get(
    "/", response_description="Get all airlines", response_model=List[Airline]
)
def list_airlines(request: Request, rating: float = 0):
    airlines = list(
        request.app.database["airlines"].find(
            {"average_rating": {"$gte": rating}}
        )
    )
    return airlines


@router.get(
    "/{id}",
    response_description="Get a single airline by id",
    response_model=Airline,
)
def find_airline(id: str, request: Request):
    if (
        airline := request.app.database["airlines"].find_one({"_id": id})
    ) is not None:
        return airline

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"airline with ID {id} not found",
    )


@router.put(
    "/{id}",
    response_description="Update a airline by id",
    response_model=Airline,
)
def update_airline(
    id: str, request: Request, airline: FlightUpdate = Body(...)
):
    flightUpdate = jsonable_encoder(flightUpdate)

    if not request.app.database["airlines"].find_one({"_id": id}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Flight with ID {id} not found",
        )

    request.app.database["airlines"].update_one(
        {"_id": id}, {"$set": flightUpdate}
    )
    flightUpdate = request.app.database["airlines"].find_one({"_id": id})

    if flightUpdate is not None:
        return flightUpdate
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Flight with ID {id} not found",
        )


@router.delete("/{id}", response_description="Delete a airline")
def delete_airline(id: str, request: Request, response: Response):
    delete_flight = request.app.database["airlines"].delete_one({"_id": id})

    if delete_flight.deleted_count:
        return {"message": f"Flight with ID {id} has been deleted"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Flight with ID {id} not found",
    )


@router.get("/automated-carts-recommendation", response_model=Airline)
def get_automated_carts_recommendation(request: Request, response: Response):
    recommendations = []
    for airport_data in request.app.database["airlines"].find():
        score = airport_data.get("some_metric", 0)
        recommendations.append(
            {"airport": airport_data["airport"], "benefit_score": score}
        )

    if recommendations:
        return recommendations
    else:
        raise HTTPException(
            status_code=404, detail="No recommendations available"
        )
