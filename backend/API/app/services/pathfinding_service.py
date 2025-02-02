import os
import csv
import ast
import heapq
import json
import time
import psutil
from abc import ABC, abstractmethod
from collections import defaultdict, deque
from geopy.distance import geodesic
from config import config
import uuid
import folium
from folium import plugins

DATA_DIR = os.path.join(config["basedir"], "app", "models", "pathfinding")

with open(os.path.join(DATA_DIR, "stations_info.json"), "r") as json_file:
    station_data = json.load(json_file)

station_name_to_code = {}
for code, data in station_data.items():
    name = data["libelle"].strip().lower()
    station_name_to_code[name] = code


def convert_to_dict(connected_to_str):
    try:
        list_of_dicts = ast.literal_eval(connected_to_str)
        return {
            str(item["station"]): float("{:.2f}".format(item["distance"]))
            for item in list_of_dicts
        }
    except (ValueError, SyntaxError):
        print(f"Error converting data: {connected_to_str}")
        return None


connected_stations = {}
with open(
    os.path.join(DATA_DIR, "adjacency_list_stations_uic.csv"), "r", encoding="utf-8"
) as file:
    reader = csv.DictReader(file, delimiter=",")
    for row in reader:
        code_uic = str(row["CODE_UIC"])
        connections = convert_to_dict(row["connected_to"])
        if connections:
            connected_stations[code_uic] = connections


class Graph:
    def __init__(self):
        self.graph = defaultdict(dict)

    def add_edge(self, node1, node2, weight):
        self.graph[node1][node2] = weight
        self.graph[node2][node1] = weight

    def get_neighbors(self, node):
        return self.graph.get(node, {})

    def get_all_nodes(self):
        return self.graph.keys()


G = Graph()
for station, connections in connected_stations.items():
    for connected_station, distance in connections.items():
        G.add_edge(station, connected_station, distance)


class Pathfinder(ABC):
    def __init__(self, graph):
        self.graph = graph

    @abstractmethod
    def find_route(self, start, intermediates, goal):
        """
        Public method that receives start + intermediates + goal,
        splits them into sub-routes, aggregates results, and builds one combined map.
        """
        pass

    def compose_stops(self, start, intermediates, goal):
        """
        Combines start, intermediates, and goal into a single list of station codes.
        """
        return [start] + intermediates + [goal]

    def heuristic(self, node1, node2):
        node1_coords = station_data[node1]["coordinates"]
        node2_coords = station_data[node2]["coordinates"]
        return geodesic(node1_coords, node2_coords).kilometers

    def path_code_to_object(self, path):
        """
        Converts a list of station codes to human-readable station names.
        """
        return [station_data[station]["libelle"] for station in path]

    def reconstruct_path(self, came_from, current):
        """
        Reconstructs the path from the start node to the goal node.
        """
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.insert(0, current)
        return total_path

    def serialize_result(
        self,
        came_from,
        current_node,
        goal,
        distance,
        total_memory,
        start_time,
        end_time,
        tries,
    ):
        """
        Creates an HTML map (via Folium) for a single sub-route and returns a dict
        with path details including both station names and raw station codes.
        (This is used internally by the _find_single_route methods.)
        """
        total_time = end_time - start_time
        average_node_time = total_time / tries if tries > 0 else 0
        memory_usage_mb = total_memory / (1024**2)

        path_codes = self.reconstruct_path(came_from, current_node)
        path_names = self.path_code_to_object(path_codes)
        path_coords = [
            station_data[station]["coordinates"][::-1] for station in path_codes
        ]

        # Generate a map for the sub-route (for internal use only)
        folium_map = self.generate_folium_map(
            path_coords, path_names, path_codes, user_intermediates=None
        )
        unique_id = uuid.uuid4()
        map_filename = f"map_{unique_id}.html"
        map_directory = os.path.join(config["basedir"], "app", "static", "maps")
        if not os.path.exists(map_directory):
            os.makedirs(map_directory)
        map_filepath = os.path.join(map_directory, map_filename)
        folium_map.save(map_filepath)
        map_url = f"/static/maps/{map_filename}"

        return {
            "path": path_names,
            "path_codes": path_codes,
            "distance": distance,
            "tries": tries,
            "time": total_time,
            "path_length": len(path_codes),
            "memory_usage": round(memory_usage_mb, 6),
            "explored_nodes": tries,
            "average_node_time": average_node_time,
            "map_url": map_url,
        }

    def generate_folium_map(
        self, path_coords, path_names, path_codes=None, user_intermediates=None
    ):
        """
        Generates a Folium map for a route.
        Optionally, if path_codes is provided along with user_intermediates (a dict mapping station code
        to intermediate index), then markers for those user-specified intermediate stops are colored blue
        and their tooltip shows their intermediate index.
        Otherwise:
          - Start marker is green.
          - End marker is red.
          - Other markers are orange.
        """
        avg_lat = sum(coord[0] for coord in path_coords) / len(path_coords)
        avg_lon = sum(coord[1] for coord in path_coords) / len(path_coords)
        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=6)
        plugins.AntPath(
            locations=path_coords,
            color="#3388ff",
            weight=5,
            opacity=0.7,
            delay=2000,
            dash_array=[10, 20],
        ).add_to(m)

        start_color = "#28a745"  # green
        end_color = "#dc3545"  # red
        default_color = "#ffc107"  # orange for computed intermediate nodes
        user_int_color = "#0000FF"  # blue for user-specified intermediate stops

        for idx, (coord, name) in enumerate(zip(path_coords, path_names)):
            # Determine marker color and extra label based on position and user-specified intermediate stops.
            if idx == 0:
                color = start_color
                tooltip_text = f"Start: {name}"
            elif idx == len(path_coords) - 1:
                color = end_color
                tooltip_text = f"Goal: {name}"
            elif (
                user_intermediates
                and path_codes
                and (path_codes[idx] in user_intermediates)
            ):
                color = user_int_color
                # Show intermediate index from user specification.
                intermediate_index = user_intermediates.get(path_codes[idx], "?")
                tooltip_text = f"Intermediate {intermediate_index}: {name}"
            else:
                color = default_color
                tooltip_text = f"{idx + 1}. {name}"

            html = f"""
            <div style="font-family: Arial; font-size: 14px;">
                <h4 style="margin-bottom:5px;">Station Information</h4>
                <b>Name:</b> {name}<br>
                <b>Stop:</b> {idx + 1} of {len(path_coords)}<br>
                <b>Coordinates:</b> {coord[0]:.5f}, {coord[1]:.5f}
            </div>
            """
            popup = folium.Popup(html, max_width=300)
            tooltip = folium.Tooltip(tooltip_text)
            folium.CircleMarker(
                location=coord,
                radius=8,
                popup=popup,
                tooltip=tooltip,
                color="black",
                weight=1,
                fill=True,
                fill_color=color,
                fill_opacity=0.9,
            ).add_to(m)

        folium.LayerControl().add_to(m)
        plugins.Fullscreen(position="topright").add_to(m)
        plugins.MiniMap(toggle_display=True).add_to(m)
        plugins.MousePosition().add_to(m)
        plugins.MeasureControl().add_to(m)
        return m


# ---------------------- A* Algorithm ----------------------
class AStar(Pathfinder):
    def find_route(self, start, intermediates, goal):
        """
        Aggregates sub-route results for A* over the entire route and creates one combined map.
        """
        stops = self.compose_stops(start, intermediates, goal)
        aggregated_codes = []
        total_distance = 0.0
        total_tries = 0
        total_time = 0.0
        peak_memory_usage = 0.0

        # For highlighting user-specified intermediate stops, build a dict mapping
        # each intermediate station code to its index (starting at 1).
        user_intermediates = {}
        for idx, code in enumerate(intermediates, start=1):
            user_intermediates[code] = idx

        for i in range(len(stops) - 1):
            seg_start = stops[i]
            seg_goal = stops[i + 1]
            segment_result = self._find_single_route(seg_start, seg_goal)
            if "error" in segment_result:
                return segment_result

            seg_codes = segment_result["path_codes"]
            if i == 0:
                aggregated_codes.extend(seg_codes)
            else:
                aggregated_codes.extend(seg_codes[1:])

            total_distance += segment_result["distance"]
            total_tries += segment_result["tries"]
            total_time += segment_result["time"]
            peak_memory_usage = max(peak_memory_usage, segment_result["memory_usage"])

        average_node_time = total_time / total_tries if total_tries > 0 else 0.0
        aggregated_names = self.path_code_to_object(aggregated_codes)
        aggregated_coords = [
            station_data[code]["coordinates"][::-1] for code in aggregated_codes
        ]

        # Generate one combined map, passing the aggregated raw codes and the user_intermediates dict.
        folium_map = self.generate_folium_map(
            aggregated_coords, aggregated_names, aggregated_codes, user_intermediates
        )
        unique_id = uuid.uuid4()
        map_filename = f"map_{unique_id}.html"
        map_directory = os.path.join(config["basedir"], "app", "static", "maps")
        if not os.path.exists(map_directory):
            os.makedirs(map_directory)
        map_filepath = os.path.join(map_directory, map_filename)
        folium_map.save(map_filepath)
        combined_map_url = f"/static/maps/{map_filename}"

        return {
            "path": aggregated_names,
            "path_codes": aggregated_codes,
            "distance": total_distance,
            "tries": total_tries,
            "time": total_time,
            "path_length": len(aggregated_codes),
            "memory_usage": round(peak_memory_usage, 6),
            "explored_nodes": total_tries,
            "average_node_time": average_node_time,
            "map_url": combined_map_url,
        }

    def _find_single_route(self, start, goal):
        process = psutil.Process()
        start_memory = process.memory_info().rss
        peak_memory = start_memory
        start_time = time.time()
        open_set = [(0, start)]
        came_from = {}
        g_score = defaultdict(lambda: float("inf"))
        f_score = defaultdict(lambda: float("inf"))
        tries = 0
        g_score[start] = 0
        f_score[start] = self.heuristic(start, goal)

        while open_set:
            tries += 1
            current_f, current_node = heapq.heappop(open_set)
            current_mem = process.memory_info().rss
            peak_memory = max(peak_memory, current_mem)

            if current_node == goal:
                end_time = time.time()
                total_memory = peak_memory - start_memory
                path_codes = self.reconstruct_path(came_from, current_node)
                path_names = self.path_code_to_object(path_codes)
                total_time = end_time - start_time
                average_node_time = total_time / tries if tries > 0 else 0
                memory_usage_mb = total_memory / (1024**2)
                return {
                    "path": path_names,
                    "path_codes": path_codes,
                    "distance": g_score[goal],
                    "tries": tries,
                    "time": total_time,
                    "path_length": len(path_codes),
                    "memory_usage": round(memory_usage_mb, 6),
                    "explored_nodes": tries,
                    "average_node_time": average_node_time,
                }

            for neighbor, distance in self.graph.get_neighbors(current_node).items():
                tentative_g_score = g_score[current_node] + distance
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(
                        neighbor, goal
                    )
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return {"error": "No path found"}


# ---------------------- Dijkstra Algorithm ----------------------
class Dijkstra(Pathfinder):
    def find_route(self, start, intermediates, goal):
        stops = self.compose_stops(start, intermediates, goal)
        aggregated_codes = []
        total_distance = 0.0
        total_tries = 0
        total_time = 0.0
        peak_memory_usage = 0.0
        user_intermediates = {}
        for idx, code in enumerate(intermediates, start=1):
            user_intermediates[code] = idx

        for i in range(len(stops) - 1):
            seg_start = stops[i]
            seg_goal = stops[i + 1]
            segment_result = self._find_single_route(seg_start, seg_goal)
            if "error" in segment_result:
                return segment_result

            seg_codes = segment_result["path_codes"]
            if i == 0:
                aggregated_codes.extend(seg_codes)
            else:
                aggregated_codes.extend(seg_codes[1:])
            total_distance += segment_result["distance"]
            total_tries += segment_result["tries"]
            total_time += segment_result["time"]
            peak_memory_usage = max(peak_memory_usage, segment_result["memory_usage"])

        avg_node_time = total_time / total_tries if total_tries else 0
        aggregated_names = self.path_code_to_object(aggregated_codes)
        aggregated_coords = [
            station_data[code]["coordinates"][::-1] for code in aggregated_codes
        ]
        folium_map = self.generate_folium_map(
            aggregated_coords, aggregated_names, aggregated_codes, user_intermediates
        )
        unique_id = uuid.uuid4()
        map_filename = f"map_{unique_id}.html"
        map_directory = os.path.join(config["basedir"], "app", "static", "maps")
        if not os.path.exists(map_directory):
            os.makedirs(map_directory)
        map_filepath = os.path.join(map_directory, map_filename)
        folium_map.save(map_filepath)
        combined_map_url = f"/static/maps/{map_filename}"

        return {
            "path": aggregated_names,
            "path_codes": aggregated_codes,
            "distance": total_distance,
            "tries": total_tries,
            "time": total_time,
            "path_length": len(aggregated_codes),
            "memory_usage": round(peak_memory_usage, 6),
            "explored_nodes": total_tries,
            "average_node_time": avg_node_time,
            "map_url": combined_map_url,
        }

    def _find_single_route(self, start, goal):
        process = psutil.Process()
        start_memory = process.memory_info().rss
        peak_memory = start_memory
        start_time = time.time()
        pq = [(0, start)]
        distances = defaultdict(lambda: float("inf"))
        distances[start] = 0
        came_from = {}
        tries = 0

        while pq:
            tries += 1
            current_distance, current_node = heapq.heappop(pq)
            current_mem = process.memory_info().rss
            peak_memory = max(peak_memory, current_mem)

            if current_node == goal:
                end_time = time.time()
                total_memory = peak_memory - start_memory
                return self.serialize_result(
                    came_from,
                    current_node,
                    goal,
                    distances[goal],
                    total_memory,
                    start_time,
                    end_time,
                    tries,
                )

            for neighbor, distance in self.graph.get_neighbors(current_node).items():
                tentative_distance = distances[current_node] + distance
                if tentative_distance < distances[neighbor]:
                    distances[neighbor] = tentative_distance
                    came_from[neighbor] = current_node
                    heapq.heappush(pq, (tentative_distance, neighbor))

        return {"error": "No path found"}


# ---------------------- BFS Algorithm ----------------------
class BFS(Pathfinder):
    def find_route(self, start, intermediates, goal):
        stops = self.compose_stops(start, intermediates, goal)
        aggregated_codes = []
        total_distance = 0.0  # BFS uses -1 per segment by default.
        total_tries = 0
        total_time = 0.0
        peak_memory_usage = 0.0
        user_intermediates = {}
        for idx, code in enumerate(intermediates, start=1):
            user_intermediates[code] = idx

        for i in range(len(stops) - 1):
            seg_start = stops[i]
            seg_goal = stops[i + 1]
            segment_result = self._find_single_route(seg_start, seg_goal)
            if "error" in segment_result:
                return segment_result
            seg_codes = segment_result["path_codes"]
            if i == 0:
                aggregated_codes.extend(seg_codes)
            else:
                aggregated_codes.extend(seg_codes[1:])
            total_distance += segment_result["distance"]
            total_tries += segment_result["tries"]
            total_time += segment_result["time"]
            peak_memory_usage = max(peak_memory_usage, segment_result["memory_usage"])

        avg_node_time = total_time / total_tries if total_tries else 0
        aggregated_names = self.path_code_to_object(aggregated_codes)
        aggregated_coords = [
            station_data[code]["coordinates"][::-1] for code in aggregated_codes
        ]
        folium_map = self.generate_folium_map(
            aggregated_coords, aggregated_names, aggregated_codes, user_intermediates
        )
        unique_id = uuid.uuid4()
        map_filename = f"map_{unique_id}.html"
        map_directory = os.path.join(config["basedir"], "app", "static", "maps")
        if not os.path.exists(map_directory):
            os.makedirs(map_directory)
        map_filepath = os.path.join(map_directory, map_filename)
        folium_map.save(map_filepath)
        combined_map_url = f"/static/maps/{map_filename}"

        return {
            "path": aggregated_names,
            "path_codes": aggregated_codes,
            "distance": total_distance,
            "tries": total_tries,
            "time": total_time,
            "path_length": len(aggregated_codes),
            "memory_usage": round(peak_memory_usage, 6),
            "explored_nodes": total_tries,
            "average_node_time": avg_node_time,
            "map_url": combined_map_url,
        }

    def _find_single_route(self, start, goal):
        process = psutil.Process()
        start_memory = process.memory_info().rss
        peak_memory = start_memory
        start_time = time.time()
        queue = deque([start])
        came_from = {}
        visited = set()
        tries = 0
        visited.add(start)

        while queue:
            tries += 1
            current_node = queue.popleft()
            current_mem = process.memory_info().rss
            peak_memory = max(peak_memory, current_mem)

            if current_node == goal:
                end_time = time.time()
                total_memory = peak_memory - start_memory
                return self.serialize_result(
                    came_from,
                    current_node,
                    goal,
                    -1,
                    total_memory,
                    start_time,
                    end_time,
                    tries,
                )

            for neighbor in self.graph.get_neighbors(current_node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current_node
                    queue.append(neighbor)

        return {"error": "No path found"}


# ---------------------- DFS Algorithm ----------------------
class DFS(Pathfinder):
    def find_route(self, start, intermediates, goal):
        stops = self.compose_stops(start, intermediates, goal)
        aggregated_codes = []
        total_distance = 0.0  # DFS uses -1 as default.
        total_tries = 0
        total_time = 0.0
        peak_memory_usage = 0.0
        user_intermediates = {}
        for idx, code in enumerate(intermediates, start=1):
            user_intermediates[code] = idx

        for i in range(len(stops) - 1):
            seg_start = stops[i]
            seg_goal = stops[i + 1]
            segment_result = self._find_single_route(seg_start, seg_goal)
            if "error" in segment_result:
                return segment_result
            seg_codes = segment_result["path_codes"]
            if i == 0:
                aggregated_codes.extend(seg_codes)
            else:
                aggregated_codes.extend(seg_codes[1:])
            total_distance += segment_result["distance"]
            total_tries += segment_result["tries"]
            total_time += segment_result["time"]
            peak_memory_usage = max(peak_memory_usage, segment_result["memory_usage"])

        avg_node_time = total_time / total_tries if total_tries else 0
        aggregated_names = self.path_code_to_object(aggregated_codes)
        aggregated_coords = [
            station_data[code]["coordinates"][::-1] for code in aggregated_codes
        ]
        folium_map = self.generate_folium_map(
            aggregated_coords, aggregated_names, aggregated_codes, user_intermediates
        )
        unique_id = uuid.uuid4()
        map_filename = f"map_{unique_id}.html"
        map_directory = os.path.join(config["basedir"], "app", "static", "maps")
        if not os.path.exists(map_directory):
            os.makedirs(map_directory)
        map_filepath = os.path.join(map_directory, map_filename)
        folium_map.save(map_filepath)
        combined_map_url = f"/static/maps/{map_filename}"

        return {
            "path": aggregated_names,
            "path_codes": aggregated_codes,
            "distance": total_distance,
            "tries": total_tries,
            "time": total_time,
            "path_length": len(aggregated_codes),
            "memory_usage": round(peak_memory_usage, 6),
            "explored_nodes": total_tries,
            "average_node_time": avg_node_time,
            "map_url": combined_map_url,
        }

    def _find_single_route(self, start, goal):
        process = psutil.Process()
        start_memory = process.memory_info().rss
        peak_memory = start_memory
        start_time = time.time()
        stack = [start]
        came_from = {}
        visited = set()
        tries = 0

        while stack:
            tries += 1
            current_node = stack.pop()
            current_mem = process.memory_info().rss
            peak_memory = max(peak_memory, current_mem)

            if current_node == goal:
                end_time = time.time()
                total_memory = peak_memory - start_memory
                return self.serialize_result(
                    came_from,
                    current_node,
                    goal,
                    -1,
                    total_memory,
                    start_time,
                    end_time,
                    tries,
                )

            if current_node not in visited:
                visited.add(current_node)
                for neighbor in self.graph.get_neighbors(current_node):
                    if neighbor not in visited:
                        came_from[neighbor] = current_node
                        stack.append(neighbor)

        return {"error": "No path found"}


# ---------------------- Bellman-Ford Algorithm ----------------------
class BellmanFord(Pathfinder):
    def find_route(self, start, intermediates, goal):
        stops = self.compose_stops(start, intermediates, goal)
        aggregated_codes = []
        total_distance = 0.0
        total_tries = 0
        total_time = 0.0
        peak_memory_usage = 0.0
        user_intermediates = {}
        for idx, code in enumerate(intermediates, start=1):
            user_intermediates[code] = idx

        for i in range(len(stops) - 1):
            seg_start = stops[i]
            seg_goal = stops[i + 1]
            segment_result = self._find_single_route(seg_start, seg_goal)
            if "error" in segment_result:
                return segment_result
            seg_codes = segment_result["path_codes"]
            if i == 0:
                aggregated_codes.extend(seg_codes)
            else:
                aggregated_codes.extend(seg_codes[1:])
            total_distance += segment_result["distance"]
            total_tries += segment_result["tries"]
            total_time += segment_result["time"]
            peak_memory_usage = max(peak_memory_usage, segment_result["memory_usage"])

        avg_node_time = total_time / total_tries if total_tries else 0
        aggregated_names = self.path_code_to_object(aggregated_codes)
        aggregated_coords = [
            station_data[code]["coordinates"][::-1] for code in aggregated_codes
        ]
        folium_map = self.generate_folium_map(
            aggregated_coords, aggregated_names, aggregated_codes, user_intermediates
        )
        unique_id = uuid.uuid4()
        map_filename = f"map_{unique_id}.html"
        map_directory = os.path.join(config["basedir"], "app", "static", "maps")
        if not os.path.exists(map_directory):
            os.makedirs(map_directory)
        map_filepath = os.path.join(map_directory, map_filename)
        folium_map.save(map_filepath)
        combined_map_url = f"/static/maps/{map_filename}"

        return {
            "path": aggregated_names,
            "path_codes": aggregated_codes,
            "distance": total_distance,
            "tries": total_tries,
            "time": total_time,
            "path_length": len(aggregated_codes),
            "memory_usage": round(peak_memory_usage, 6),
            "explored_nodes": total_tries,
            "average_node_time": avg_node_time,
            "map_url": combined_map_url,
        }

    def _find_single_route(self, start, goal):
        process = psutil.Process()
        start_memory = process.memory_info().rss
        peak_memory = start_memory
        start_time = time.time()
        distances = defaultdict(lambda: float("inf"))
        distances[start] = 0
        came_from = {}
        tries = 0
        nodes = list(self.graph.get_all_nodes())

        for _ in range(len(nodes) - 1):
            tries += 1
            for u in nodes:
                for v, weight in self.graph.get_neighbors(u).items():
                    if distances[u] + weight < distances[v]:
                        distances[v] = distances[u] + weight
                        came_from[v] = u
            current_mem = process.memory_info().rss
            peak_memory = max(peak_memory, current_mem)

        for u in nodes:
            for v, weight in self.graph.get_neighbors(u).items():
                if distances[u] + weight < distances[v]:
                    return {"error": "Graph contains a negative-weight cycle"}

        if distances[goal] == float("inf"):
            return {"error": "No path found"}

        end_time = time.time()
        total_memory = peak_memory - start_memory
        return self.serialize_result(
            came_from,
            goal,
            goal,
            distances[goal],
            total_memory,
            start_time,
            end_time,
            tries,
        )


# ---------------------- Uniform Cost Search Algorithm ----------------------
class UniformCostSearch(Pathfinder):
    def find_route(self, start, intermediates, goal):
        stops = self.compose_stops(start, intermediates, goal)
        aggregated_codes = []
        total_distance = 0.0
        total_tries = 0
        total_time = 0.0
        peak_memory_usage = 0.0
        user_intermediates = {}
        for idx, code in enumerate(intermediates, start=1):
            user_intermediates[code] = idx

        for i in range(len(stops) - 1):
            seg_start = stops[i]
            seg_goal = stops[i + 1]
            segment_result = self._find_single_route(seg_start, seg_goal)
            if "error" in segment_result:
                return segment_result
            seg_codes = segment_result["path_codes"]
            if i == 0:
                aggregated_codes.extend(seg_codes)
            else:
                aggregated_codes.extend(seg_codes[1:])
            total_distance += segment_result["distance"]
            total_tries += segment_result["tries"]
            total_time += segment_result["time"]
            peak_memory_usage = max(peak_memory_usage, segment_result["memory_usage"])

        avg_node_time = total_time / total_tries if total_tries else 0
        aggregated_names = self.path_code_to_object(aggregated_codes)
        aggregated_coords = [
            station_data[code]["coordinates"][::-1] for code in aggregated_codes
        ]
        folium_map = self.generate_folium_map(
            aggregated_coords, aggregated_names, aggregated_codes, user_intermediates
        )
        unique_id = uuid.uuid4()
        map_filename = f"map_{unique_id}.html"
        map_directory = os.path.join(config["basedir"], "app", "static", "maps")
        if not os.path.exists(map_directory):
            os.makedirs(map_directory)
        map_filepath = os.path.join(map_directory, map_filename)
        folium_map.save(map_filepath)
        combined_map_url = f"/static/maps/{map_filename}"

        return {
            "path": aggregated_names,
            "path_codes": aggregated_codes,
            "distance": total_distance,
            "tries": total_tries,
            "time": total_time,
            "path_length": len(aggregated_codes),
            "memory_usage": round(peak_memory_usage, 6),
            "explored_nodes": total_tries,
            "average_node_time": avg_node_time,
            "map_url": combined_map_url,
        }

    def _find_single_route(self, start, goal):
        process = psutil.Process()
        start_memory = process.memory_info().rss
        peak_memory = start_memory
        start_time = time.time()
        frontier = [(0, start)]
        came_from = {}
        cost_so_far = {start: 0}
        tries = 0

        while frontier:
            tries += 1
            current_cost, current_node = heapq.heappop(frontier)
            current_mem = process.memory_info().rss
            peak_memory = max(peak_memory, current_mem)

            if current_node == goal:
                end_time = time.time()
                total_memory = peak_memory - start_memory
                return self.serialize_result(
                    came_from,
                    current_node,
                    goal,
                    cost_so_far[goal],
                    total_memory,
                    start_time,
                    end_time,
                    tries,
                )

            for neighbor, weight in self.graph.get_neighbors(current_node).items():
                new_cost = cost_so_far[current_node] + weight
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(frontier, (new_cost, neighbor))
                    came_from[neighbor] = current_node

        return {"error": "No path found"}


# ---------------------- Bidirectional A* Algorithm ----------------------
class BidirectionalAStar(Pathfinder):
    def find_route(self, start, intermediates, goal):
        stops = self.compose_stops(start, intermediates, goal)
        aggregated_codes = []
        total_distance = 0.0
        total_tries = 0
        total_time = 0.0
        peak_memory_usage = 0.0
        user_intermediates = {}
        for idx, code in enumerate(intermediates, start=1):
            user_intermediates[code] = idx

        for i in range(len(stops) - 1):
            seg_start = stops[i]
            seg_goal = stops[i + 1]
            segment_result = self._find_single_bidirectional_route(seg_start, seg_goal)
            if "error" in segment_result:
                return segment_result
            seg_codes = segment_result["path_codes"]
            if i == 0:
                aggregated_codes.extend(seg_codes)
            else:
                aggregated_codes.extend(seg_codes[1:])
            total_distance += segment_result["distance"]
            total_tries += segment_result["tries"]
            total_time += segment_result["time"]
            peak_memory_usage = max(peak_memory_usage, segment_result["memory_usage"])

        avg_node_time = total_time / total_tries if total_tries else 0
        aggregated_names = self.path_code_to_object(aggregated_codes)
        aggregated_coords = [
            station_data[code]["coordinates"][::-1] for code in aggregated_codes
        ]
        folium_map = self.generate_folium_map(
            aggregated_coords, aggregated_names, aggregated_codes, user_intermediates
        )
        unique_id = uuid.uuid4()
        map_filename = f"map_{unique_id}.html"
        map_directory = os.path.join(config["basedir"], "app", "static", "maps")
        if not os.path.exists(map_directory):
            os.makedirs(map_directory)
        map_filepath = os.path.join(map_directory, map_filename)
        folium_map.save(map_filepath)
        combined_map_url = f"/static/maps/{map_filename}"

        return {
            "path": aggregated_names,
            "path_codes": aggregated_codes,
            "distance": total_distance,
            "tries": total_tries,
            "time": total_time,
            "path_length": len(aggregated_codes),
            "memory_usage": round(peak_memory_usage, 6),
            "explored_nodes": total_tries,
            "average_node_time": avg_node_time,
            "map_url": combined_map_url,
        }

    def _find_single_bidirectional_route(self, start, goal):
        process = psutil.Process()
        start_memory = process.memory_info().rss
        peak_memory = start_memory
        start_time = time.time()
        open_set_fwd = [(0, start)]
        open_set_bwd = [(0, goal)]
        came_from_fwd = {}
        came_from_bwd = {}
        g_score_fwd = defaultdict(lambda: float("inf"))
        g_score_bwd = defaultdict(lambda: float("inf"))
        g_score_fwd[start] = 0
        g_score_bwd[goal] = 0
        visited_fwd = set()
        visited_bwd = set()
        tries = 0

        while open_set_fwd and open_set_bwd:
            tries += 1
            _, current_fwd = heapq.heappop(open_set_fwd)
            visited_fwd.add(current_fwd)
            current_mem = process.memory_info().rss
            peak_memory = max(peak_memory, current_mem)

            if current_fwd in visited_bwd:
                meeting_node = current_fwd
                end_time = time.time()
                total_memory = peak_memory - start_memory
                return self._reconstruct_bidirectional_path(
                    came_from_fwd,
                    came_from_bwd,
                    meeting_node,
                    g_score_fwd[current_fwd] + g_score_bwd[current_fwd],
                    total_memory,
                    start_time,
                    end_time,
                    tries,
                )

            for neighbor, weight in self.graph.get_neighbors(current_fwd).items():
                tentative_g_score = g_score_fwd[current_fwd] + weight
                if tentative_g_score < g_score_fwd[neighbor]:
                    came_from_fwd[neighbor] = current_fwd
                    g_score_fwd[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set_fwd, (f_score, neighbor))

            if open_set_bwd:
                _, current_bwd = heapq.heappop(open_set_bwd)
                visited_bwd.add(current_bwd)
                current_mem = process.memory_info().rss
                peak_memory = max(peak_memory, current_mem)

                if current_bwd in visited_fwd:
                    meeting_node = current_bwd
                    end_time = time.time()
                    total_memory = peak_memory - start_memory
                    return self._reconstruct_bidirectional_path(
                        came_from_fwd,
                        came_from_bwd,
                        meeting_node,
                        g_score_fwd[current_bwd] + g_score_bwd[current_bwd],
                        total_memory,
                        start_time,
                        end_time,
                        tries,
                    )

                for neighbor, weight in self.graph.get_neighbors(current_bwd).items():
                    tentative_g_score = g_score_bwd[current_bwd] + weight
                    if tentative_g_score < g_score_bwd[neighbor]:
                        came_from_bwd[neighbor] = current_bwd
                        g_score_bwd[neighbor] = tentative_g_score
                        f_score = tentative_g_score + self.heuristic(neighbor, start)
                        heapq.heappush(open_set_bwd, (f_score, neighbor))

        return {"error": "No path found"}

    def _reconstruct_bidirectional_path(
        self,
        came_from_fwd,
        came_from_bwd,
        meeting_node,
        total_distance,
        total_memory,
        start_time,
        end_time,
        tries,
    ):
        path_fwd = []
        current = meeting_node
        while current in came_from_fwd:
            path_fwd.append(current)
            current = came_from_fwd[current]
        path_fwd.append(current)
        path_fwd = path_fwd[::-1]

        path_bwd = []
        current = meeting_node
        while current in came_from_bwd:
            current = came_from_bwd[current]
            path_bwd.append(current)

        full_path = path_fwd + path_bwd
        total_time = end_time - start_time
        average_node_time = total_time / tries if tries > 0 else 0
        memory_usage_mb = total_memory / (1024**2)
        path_names = self.path_code_to_object(full_path)

        return {
            "path": path_names,
            "path_codes": full_path,
            "distance": total_distance,
            "tries": tries,
            "time": total_time,
            "path_length": len(full_path),
            "memory_usage": round(memory_usage_mb, 6),
            "explored_nodes": tries,
            "average_node_time": average_node_time,
        }


def find_path(start_name, end_name, intermediates=None, algorithm="AStar"):
    """
    Find the optimal path from start to end using the specified algorithm,
    optionally including intermediate stations. The aggregator logic returns
    a single combined map covering the entire route.
    """
    try:
        if intermediates is None:
            intermediates = []

        start_name = start_name.strip().lower()
        end_name = end_name.strip().lower()
        intermediates = [st.strip().lower() for st in intermediates]

        start_code = station_name_to_code.get(start_name)
        end_code = station_name_to_code.get(end_name)
        intermediate_codes = [station_name_to_code.get(name) for name in intermediates]

        if not start_code:
            return {"error": f"Start station '{start_name}' not found."}
        if not end_code:
            return {"error": f"End station '{end_name}' not found."}
        for i, code in enumerate(intermediate_codes):
            if code is None:
                return {
                    "error": f"Intermediate station '{intermediates[i]}' not found."
                }

        switch = {
            "AStar": AStar,
            "Dijkstra": Dijkstra,
            "BFS": BFS,
            "DFS": DFS,
            "BellmanFord": BellmanFord,
            "UCS": UniformCostSearch,
            "BidirectionalAStar": BidirectionalAStar,
        }

        PathfinderClass = switch.get(algorithm)
        if PathfinderClass is None:
            return {"error": f"Unsupported algorithm '{algorithm}'"}

        pathfinder = PathfinderClass(G)
        print(
            f"Finding path from {start_code} to {end_code} using {pathfinder.__class__.__name__}\nwith intermediates: {intermediate_codes}"
        )
        result = pathfinder.find_route(start_code, intermediate_codes, end_code)
        return result
    except Exception as e:
        return {"error": str(e)}
