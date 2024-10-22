import csv
import ast
import heapq
from collections import defaultdict, deque
from functools import lru_cache
import time
import psutil  
import matplotlib.pyplot as plt
from geopy.distance import geodesic
import json

PATHFINDER_DIR = '/workspaces/T-AIA-901_par_1/pathfinder_try/'
with open(PATHFINDER_DIR + 'output/stations_info.json', 'r') as json_file:
    station_data = json.load(json_file)

def convert_to_dict(connected_to_str):
    try:
        list_of_dicts = ast.literal_eval(connected_to_str)
        return {str(item['station']): float("{:.2f}".format(item['distance'])) for item in list_of_dicts}
    except (ValueError, SyntaxError):
        print(f"Error converting data: {connected_to_str}")
        return None

connected_stations = {}
with open(PATHFINDER_DIR + '/output/adjacency_list_stations_uic.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=',')
    for row in reader:
        code_uic = str(row['CODE_UIC'])
        connected_stations[code_uic] = convert_to_dict(row['connected_to'])

# Graph class
class Graph:
    def __init__(self):
        self.graph = defaultdict(dict)
    
    def add_edge(self, node1, node2, weight):
        self.graph[node1][node2] = weight
        self.graph[node2][node1] = weight
    
    def get_neighbors(self, node):
        return self.graph[node]
    
    def get_all_nodes(self):
        return self.graph.keys()

G = Graph()
for station, connections in connected_stations.items():
    for connected_station, distance in connections.items():
        G.add_edge(station, connected_station, distance)

# Pathfinder class


