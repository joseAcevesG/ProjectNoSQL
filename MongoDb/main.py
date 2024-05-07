#!/usr/bin/env python3
import os

from fastapi import FastAPI
from pymongo import MongoClient
from pymongo.errors import OperationFailure
from routes import router as airline_router

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGODB_DB_NAME", "iteso")

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(MONGODB_URI)
    app.database = app.mongodb_client[DB_NAME]

    try:
        app.database["airlines"].create_index([("transit", 1)])
        print("Índice único en el campo 'transportation' creado exitosamente.")
    except OperationFailure as e:
        print(
            f"No se pudo crear el índice único en el campo 'transportation': {e}"
        )
        print(
            f"Connected to MongoDB at: {MONGODB_URI} \n\t Database: {DB_NAME}"
        )

    try:
        app.database["airlines"].create_index([("airline", 1)])
        print("Índice único en el campo 'ticket' creado exitosamente.")
    except OperationFailure as e:
        print(f"No se pudo crear el índice único en el campo 'ticket': {e}")
        print(
            f"Connected to MongoDB at: {MONGODB_URI} \n\t Database: {DB_NAME}"
        )
    print(f"Connected to MongoDB at: {MONGODB_URI} \n\t Database: {DB_NAME}")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    print("Bye bye...!!")


app.include_router(airline_router, tags=["airlines"], prefix="/airline")
