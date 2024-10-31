import os
import sys
import json
import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt

# open csv file and read content
def read_csv_file(file_path, delimiter = ","):
    try:
        # Read the file into a DataFrame
        content = pd.read_csv(file_path, delimiter=delimiter)
        return content
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

content = read_csv_file("./timetables-1.csv", delimiter="\t")

# Remove the first row (if it is unnecessary, adjust as needed)
content = content.drop(0)

# Show the first few rows to verify the data structure
print(content.head())

# Create a hash map where the starting station is the key, and the value is another dict with destination and duration
trips = {}
all_destinations = set()  # Track all stations that appear as destinations

for index, row in content.iterrows():
    trajet = row['trajet']
    duree = row['duree']

    # Split the trip into starting and destination stations
    try:
        # Assuming the format is "Starting Station - Destination Station"
        stations = trajet.split(' - ')
        if len(stations) == 2:
            start_station = stations[0].strip()
            end_station = stations[1].strip()

            # Add to the all_destinations set
            all_destinations.add(end_station)

            # If the starting station is not in the dictionary, add it
            if start_station not in trips:
                trips[start_station] = {}

            # Add the destination and duration to the dictionary for the starting station
            trips[start_station][end_station] = duree
    except Exception as e:
        print(f"Error processing row {index}: {e}")

# Check for stations that are not connected to any others
# These stations would appear as destinations but not as starting points
unconnected_stations = all_destinations - set(trips.keys())

# Print out the resulting dictionary of trips
print("Trips dictionary:")
for start_station, destinations in trips.items():
    print(f"{start_station} : {destinations}")

# Print unconnected stations
if unconnected_stations:
    print("\nStations that are not connected to any other stations:")
    for station in unconnected_stations:
        print(station)
else:
    print("\nAll stations are connected to at least one other station.")
