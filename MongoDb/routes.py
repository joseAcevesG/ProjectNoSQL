#!/usr/bin/env python3
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from bson import Regex

from model import Airline, FlightUpdate, AirportRecommendation

router = APIRouter()

@router.post("/", response_description="Post a new airline", status_code=status.HTTP_201_CREATED, response_model=Airline)
def create_airline(request: Request, airline: Airline = Body(...)):
    airline = jsonable_encoder(airline)
    new_airline = request.app.database["airlines"].insert_one(airline)
    created_airline = request.app.database["airlines"].find_one(
        {"_id": new_airline.inserted_id}
    )

    return created_airline


@router.get("/", response_description="Get all airlines", response_model=List[Airline])
def list_airlines(request: Request, rating: float = 0):
    airlines = list(request.app.database["airlines"].find({"average_rating": {"$gte": rating}}))
    return airlines


@router.get("/{id}", response_description="Get a single airline by id", response_model=Airline)
def find_airline(id: str, request: Request):
    if (airline := request.app.database["airlines"].find_one({"_id": id})) is not None:
        return airline

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"airline with ID {id} not found")

@router.put("/{id}", response_description="Update a airline by id", response_model=Airline)
def update_airline(id: str, request: Request, airline: FlightUpdate = Body(...)):
    flightUpdate = jsonable_encoder(flightUpdate)

    if not request.app.database["airlines"].find_one({"_id": id}):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flight with ID {id} not found")
    
    request.app.database["airlines"].update_one({"_id": id}, {"$set": flightUpdate})
    flightUpdate = request.app.database["airlines"].find_one({"_id": id})

    if flightUpdate is not None:
        return flightUpdate
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flight with ID {id} not found")

@router.delete("/{id}", response_description="Delete a airline")
def delete_airline(id: str, request: Request, response: Response):
    delete_flight = request.app.database["airlines"].delete_one({"_id": id})

    if delete_flight.deleted_count:
        return {"message": f"Flight with ID {id} has been deleted"}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flight with ID {id} not found")

@router.get("/automated-carts-recommendation", response_model=AirportRecommendation)
def get_automated_carts_recommendation(request: Request, response: Response):
    recommendations = []
    for airport_data in request.app.database["airlines"].find():
        score = airport_data.get('some_metric', 0)
        recommendations.append({
            "airport": airport_data['airport'],
            "benefit_score": score
        })
    
    if recommendations:
        return recommendations
    else:
        raise HTTPException(status_code=404, detail="No recommendations available")
