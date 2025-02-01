import pandas as pd
import json

BASE_DIR = '/workspaces/T-AIA-901_par_1/data/'
PATHFINDER_DIR = '/workspaces/T-AIA-901_par_1/pathfinder_try/'

# Load the station data
gare_df = pd.read_csv(BASE_DIR + 'liste-des-gares.csv', delimiter=';')

# Initialize an empty dictionary to hold the processed station data
station_dict = {}

# Function to process the Geo Shape and extract coordinates
def extract_coordinates(geo_shape):
    try:
        if isinstance(geo_shape, str):
            geo_shape_json = json.loads(geo_shape)
            if geo_shape_json['type'] == 'Point':
                return geo_shape_json['coordinates']  # Return the coordinates of the point
            elif geo_shape_json['type'] == 'LineString':
                return geo_shape_json['coordinates'][0]  # Use the first coordinate of the LineString
    except Exception as e:
        print(f"Error processing Geo Shape: {e}")
        return None

# Loop through the DataFrame and build the dictionary
for _, row in gare_df.iterrows():
    code_uic = row['CODE_UIC']
    libelle = row['LIBELLE']
    geo_shape = row['Geo Shape']
    
    coordinates = extract_coordinates(geo_shape)
    
    if coordinates:
        station_dict[code_uic] = {
            'libelle': libelle,
            'coordinates': coordinates
        }

# Save the resulting dictionary to a JSON file for easy access
with open(PATHFINDER_DIR + 'output/stations_info.json', 'w') as json_file:
    json.dump(station_dict, json_file, indent=4)

print("Station information saved successfully.")
