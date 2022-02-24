from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import pytz
import joblib
import os
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
        )


@app.get("/")
def index():
    return {"greeting": "Hello world"}

@app.get("/predict")
def predict(pickup_datetime, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, passenger_count):

    dico = {}

    # create a datetime object from the user provided datetime

    pickup_datetime = datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")

    # localize the user datetime with NYC timezone
    eastern = pytz.timezone("US/Eastern")
    localized_pickup_datetime = eastern.localize(pickup_datetime, is_dst=None)

    # localize the datetime to UTC
    utc_pickup_datetime = localized_pickup_datetime.astimezone(pytz.utc)

    formatted_pickup_datetime = utc_pickup_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")


    dico['key'] = 0
    dico['pickup_datetime'] = formatted_pickup_datetime
    dico['pickup_longitude'] = pickup_longitude
    dico['pickup_latitude'] = pickup_latitude
    dico['dropoff_longitude'] = dropoff_longitude
    dico['dropoff_latitude'] = dropoff_latitude
    dico['passenger_count'] = passenger_count

    df = pd.DataFrame(dico, index=[0], columns=dico.keys())


    model = joblib.load('model.joblib')

    dico_predict = {"fare": model.predict(df)[0]}

    return dico_predict
