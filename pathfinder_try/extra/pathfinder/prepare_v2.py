import pandas as pd
import json
from geopy.distance import geodesic
from joblib import Parallel, delayed
from tqdm import tqdm
import folium
import colorsys  

BASE_DIR = './data/'
PATHFINDER_DIR = './pathfinder/'
gare_df = pd.read_csv(BASE_DIR + 'liste-des-gares.csv', delimiter=';')
ligne_df = pd.read_csv(BASE_DIR + 'formes-des-lignes-du-rfn.csv', delimiter=';')

include_geo_shape = False 

prepared_df = gare_df[['CODE_UIC', 'LIBELLE', 'CODE_LIGNE', 'Geo Shape']].copy()
prepared_df['connected_to'] = None

def calculate_connected_stations(index, row, gare_df, ligne_df, include_geo_shape):
    try:
        current_station_code = row['CODE_UIC']
        current_line_code = row['CODE_LIGNE']
    
        current_station_coords = row['Geo Shape']
        if isinstance(current_station_coords, str):
            current_station_coords = json.loads(current_station_coords)
            # Check if it's a LineString or Point
            if current_station_coords['type'] == 'LineString':
                current_station_coords = current_station_coords['coordinates'][0]  # First point for simplicity
            elif current_station_coords['type'] == 'Point':
                current_station_coords = current_station_coords['coordinates']
        
        concerned_lines = ligne_df[ligne_df['CODE_LIGNE'] == current_line_code]
    
        connected_stations = gare_df[gare_df['CODE_LIGNE'].isin(concerned_lines['CODE_LIGNE'])]
        
        connected_info = []
        for _, connected_row in connected_stations.iterrows():
            if connected_row['CODE_UIC'] == current_station_code:
                continue  # Skip if it's the same station
            
            connected_station_coords = connected_row['Geo Shape']
            if isinstance(connected_station_coords, str):
                connected_station_coords = json.loads(connected_station_coords)
                if connected_station_coords['type'] == 'LineString':
                    # Iterate over all points in the LineString and find the closest point
                    closest_point = min(connected_station_coords['coordinates'], 
                                        key=lambda point: geodesic((current_station_coords[1], current_station_coords[0]), (point[1], point[0])).kilometers)
                    connected_station_coords = closest_point
                elif connected_station_coords['type'] == 'Point':
                    connected_station_coords = connected_station_coords['coordinates']
            
            coord_1 = (current_station_coords[1], current_station_coords[0])
            coord_2 = (connected_station_coords[1], connected_station_coords[0])
            distance = geodesic(coord_1, coord_2).kilometers
            
            # Append connected station info as tuples (LIBELLE, distance)
            connected_info.append((connected_row['LIBELLE'], distance))
    
        return index, connected_info
    except Exception as e:
        print(f"Error processing station {row['CODE_UIC']}: {e}")
        return index, None

results = Parallel(n_jobs=-1)(
    delayed(calculate_connected_stations)(index, row, gare_df, ligne_df, include_geo_shape) 
    for index, row in tqdm(prepared_df.iterrows(), total=len(prepared_df))
)

for index, connected_info in results:
    if connected_info is not None:
        prepared_df.at[index, 'connected_to'] = connected_info

def convert_to_dict_format(station_data):
    return [{'station': conn[0], 'distance': conn[1]} for conn in station_data]

prepared_df['connected_to'] = prepared_df['connected_to'].apply(convert_to_dict_format)

prepared_df.to_csv(PATHFINDER_DIR + "output/" 'adjacency_list_stations_uic.csv', index=False)

print("Data preparation complete.")
