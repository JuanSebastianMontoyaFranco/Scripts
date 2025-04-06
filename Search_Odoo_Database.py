import requests
import json

url = "https://octopusforce.odoo.com/web/database/list"

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers)
response.raise_for_status()

db_list = response.json().get("result", [])
print("Databases disponibles:", db_list)
