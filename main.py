import os
from dotenv import load_dotenv
import requests
from datetime import datetime
import json

now = datetime.now()


load_dotenv('api_keys.env')
nutritionix_app_id = os.environ.get('NUTRITIONIX_APP_ID')
nutritionix_api_key = os.environ.get('NUTRITIONIX_API_KEY')
nutritionix_main_endpoint = "https://trackapi.nutritionix.com"
nutritionix_natural_nutrients_endpoint = "/v2/natural/nutrients"
nutritionix_search_instant_endpoint = "/v2/search/instant"
nutritionix_natural_exercise_endpoint = "/v2/natural/exercise"
nutritionix_headers = {
    "x-app-id": nutritionix_app_id,
    "x-app-key": nutritionix_api_key,
    "Content-Type": "application/json"
}
query = input("How did you workout?")
nutritionix_api_parameters = {
    "query": query,
    "gender": "male",
    "weight_kg": 95.00,
    "height_cm": 185.00,
    "age": 44
}

response = requests.post(url=nutritionix_main_endpoint+nutritionix_natural_exercise_endpoint,
                         json=nutritionix_api_parameters,
                         headers=nutritionix_headers)
response.raise_for_status()
workouts_full = json.loads(response.text)
# print(workouts_full)

sheety_bearer_token = os.environ.get('SHEETY_BEARER_TOKEN')
sheety_api_endpoint = os.environ.get("SHEETY_API_ENDPOINT")
workouts = []
sheety_headers = {
    "Content-Type": "application/json",
    "Authorization": sheety_bearer_token,
}

for workout in workouts_full['exercises']:
    workout_data = {
            "date": now.strftime("%d/%m/%Y"),
            "time": now.strftime("%H:%M:%S"),
            "exercise": workout["user_input"].title(),
            "duration": workout["duration_min"],
            "calories": workout["nf_calories"]
        }
    sheety_parameters = {
        "workout": workout_data
        }
    print('sheety parameters:', sheety_parameters)
    print(sheety_headers)
    sheety_response = requests.post(url=sheety_api_endpoint, json=sheety_parameters, headers=sheety_headers)
    sheety_response.raise_for_status()


