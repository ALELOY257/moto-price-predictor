from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os
import json
dictionary = {}
# pag a scrapear

for i in range(5):
    print(f"Scraping page {i}")
    url = f"https://suzuki.com.co/motocicletas/lista?page={i}" 
    response = requests.get(url)
    html_content = response.content

    # parse
    soup = BeautifulSoup(html_content, "html.parser")

    # divs que contienen la info
    parent_divs = soup.find_all("div", class_="col-md-3 col-sm-6 col-xs-6 moto-info")
    price_div = soup.find_all("p", class_="precio")

    # h4 del parent div
    h4_values = []
    for div in parent_divs:
        h4_elements = div.find_all("h4")
        for h4 in h4_elements:
            h4_values.append(h4.get_text(strip=True))

    for i in range(len(h4_values)):
        dictionary[h4_values[i]] = price_div[i].get_text(strip=True)

# Output the results

formatted_prices = {
    key.replace('FI', '').replace('ABS', '').replace('EURO 3', '').strip(): int(value.replace('AGOTADO', '0').replace("$", "").replace("IVA Incluido", "").replace(",", "").strip())
    for key, value in dictionary.items()
}

print(formatted_prices)

# Llamada a la api
responses = []
load_dotenv()
api_key = os.getenv('NINJA_KEY')
for key in formatted_prices.keys():
    make = "Suzuki"
    model = key
    endpoint = f'https://api.api-ninjas.com/v1/motorcycles?make={make}&model={model}'
    headers = {
        'X-Api-Key': api_key
        }
    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200 and response.json() != []:
        response_data = response.json()
        for entry in response_data:
            entry['price'] = formatted_prices[key]
        responses.append(response_data)
    else:
        print(f'Error: {response.status_code}')

with open('suzuki_colombia.json', 'w') as json_file:
    json.dump(responses, json_file, indent=4)


