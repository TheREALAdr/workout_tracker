# ------------------------- IMPORTS ------------------------- #

import os
from datetime import datetime

import requests

# ------------------------ CONSTANTS ------------------------ #

NUTRITIONIX_APP_ID = os.environ["NUTRITIONIX_APP_ID"]
NUTRITIONIX_APP_KEY = os.environ["NUTRITIONIX_APP_KEY"]
SHEETY_AUTH = (os.environ["SHEETY_USERNAME"], os.environ["SHEETY_PASSWORD"])
SHEETY_ENDPOINT = os.environ["SHEETY_ENDPOINT"]

GENDER = "MALE"
WEIGHT_KG = 54
HEIGHT_CM = 167
AGE = 13

DATE = datetime.now().strftime("%m/%d/%Y")
HOUR_NOW = int(datetime.now().strftime("%H"))
AM_PM = "PM"

if HOUR_NOW < 5:
    HOUR_NOW = (HOUR_NOW + 12) - 5
elif HOUR_NOW == 5:
    HOUR_NOW = 12
    AM_PM = "AM"
else:
    HOUR_NOW = HOUR_NOW - 17
    if HOUR_NOW <= 0:
        HOUR_NOW += 12
        if HOUR_NOW != 12:
            AM_PM = "AM"
        
TIME = datetime.now().strftime(f"{HOUR_NOW}:%M {AM_PM}")


# -------------------- NUTRITIONIX DATA --------------------- #

nutritionix_headers = {
    'x-app-id': NUTRITIONIX_APP_ID,
    'x-app-key': NUTRITIONIX_APP_KEY,
}

nutritionix_parameters = {
    'query': input("Tell me what exercise/s you did today: "),
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

exercise_response = requests.post(
    url="https://trackapi.nutritionix.com/v2/natural/exercise",
    json=nutritionix_parameters,
    headers=nutritionix_headers,
)
exercise_response.raise_for_status()
exercise_data = exercise_response.json()
exercises = exercise_data['exercises']

# ---------------- ADDING DATA TO SHEETY ------------------ #
for exercise in exercises:
    workout_data = {
        "workout": {
            'date': DATE,
            'time': TIME,
            'exercise': exercise['name'].title(),
            'duration(mins)': exercise['duration_min'],
            'calories': exercise['nf_calories']
        }
    }
    sheety_post_response = requests.post(
        url=SHEETY_ENDPOINT,
        json=workout_data,
        auth=SHEETY_AUTH
    )
    print(sheety_post_response)
