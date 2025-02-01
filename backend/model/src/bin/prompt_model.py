# import os
# import sys

# src_dir = os.path.join(os.getcwd(), "..", "..")

# sys.path.append(os.path.abspath(src_dir))

# from src.helpers.city_to_train_station import CityToTrainHelper
# from src.utils.visualizer import Visualizer

# print("============================================================")

# visualizer = Visualizer()

# sentence = "Je souhaite aller de Paris à Marseille en passant par Lyon."

# inferences = visualizer.pipeline(sentence)

# for res in inferences:
#     search_result = CityToTrainHelper.fuzzy_search(res["place"])
#     closest_train_station = CityToTrainHelper.get_closest_train_station(search_result["name"])
#     res["train_station"] = closest_train_station
#     res["place"] = search_result["name"]

# print(inferences)