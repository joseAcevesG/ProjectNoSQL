#!/usr/bin/env python3
import uuid
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class Airline(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    airline: str = Field(...)
    from_: str = Field(...)
    to: str = Field(...)
    day: int = Field(...)
    month: int = Field(...)
    year: int = Field(...)
    duration: int = Field(...)
    age: int = Field(...)
    gender: str = Field(...)
    reason: str = Field(...)
    stay: str = Field(...)
    transit: str = Field(...)
    connection: bool = Field(...)
    wait: int = Field(...)
    ticket: str = Field(...)
    checked_bags: int = Field(...)
    carry_on: bool = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "123e4567-e89b-12d3-a456-426614174000",
                "airline": "Aeromexico",
                "from_": "GDL",
                "to": "JFK",
                "day": 15,
                "month": 6,
                "year": 2024,
                "duration": 7,
                "age": 29,
                "gender": "female",
                "reason": "business",
                "stay": "home",
                "transit": "airport_cab",
                "connection": False,
                "wait": 30,
                "ticket": "business",
                "checked_bags": 1,
                "carry_on": True,
            }
        }


class GenderOptions(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    gender: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "123e4567-e89b-12d3-a456-426614174000",
                "gender": "male",
            }
        }


class ReasonForTravel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    reason: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "123e4567-e89b-12d3-a456-426614174000",
                "reason": "back_home",
            }
        }


class AccomodationType(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    accomodation: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "123e4567-e89b-12d3-a456-426614174000",
                "accomodation": "home",
            }
        }


class TransportationType(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    transportation: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "123e4567-e89b-12d3-a456-426614174000",
                "transportation": "own_car",
            }
        }


class TicketType(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    ticket: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "123e4567-e89b-12d3-a456-426614174000",
                "ticket": "economy",
            }
        }


class FlightUpdate(BaseModel):
    airline: Optional[str]
    from_: Optional[str]
    to: Optional[str]
    day: Optional[int]
    month: Optional[int]
    year: Optional[int]
    duration: Optional[int]
    age: Optional[int]
    gender: Optional[str]
    reason: Optional[str]
    stay: Optional[str]
    transit: Optional[str]
    connection: Optional[bool]
    wait: Optional[int]
    ticket: Optional[str]
    checked_bags: Optional[int]
    carry_on: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "_id": "123e4567-e89b-12d3-a456-426614174000",
                "airline": "Aeromexico",
                "from_": "GDL",
                "to": "JFK",
                "day": 15,
                "month": 6,
                "year": 2024,
                "duration": 7,
                "age": 29,
                "gender": "Female",
                "reason": "Business",
                "stay": "Home",
                "transit": "Airport cab",
                "connection": False,
                "wait": 30,
                "ticket": "Business",
                "checked_bags": 1,
                "carry_on": True,
            }
        }
