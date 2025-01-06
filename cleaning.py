import json

# Load the JSON data from the file
with open('suzuki_colombia.json', 'r') as json_file:
    data = json.load(json_file)

# Function to get the latest year entry from a list of dictionaries
def get_latest_year_entry(entries):
    latest_entry = max(entries, key=lambda x: int(x['year']))
    return latest_entry

# Filter the data to keep only the latest year entries
filtered_data = [get_latest_year_entry(entry_list) for entry_list in data]

# Save the filtered data back to the JSON file
with open('suzuki_colombia_filtered.json', 'w') as json_file:
    json.dump(filtered_data, json_file, indent=4)

print("Filtered data saved to suzuki_colombia_filtered.json")