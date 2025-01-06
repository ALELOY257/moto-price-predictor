
import requests
import json

url = "https://suzuki-motos-api-134691067108.us-east1.run.app/predict"
headers = {"Content-Type": "application/json"}

data = {
    "displacement": 645.2,
    "engine": "V2, four-stroke",
    "compression": 11.5,
    "bore": 81.5,
    "stroke": 62.2,
    "fuel_system": "Injection",
    "cooling": "Liquid",
    "power": 69.7,
    "torque": 69.0,
    "front_suspension": "Telescopic, coil spring, oil damped"
}

response = requests.post(url, headers=headers, json=data)

print(response.text)
