import os
import sys

src_dir = os.path.join(os.getcwd(), "..", "..")

sys.path.append(os.path.abspath(src_dir))

from src.helpers.city_to_train_station import CityToTrainHelper
from src.utils.visualizer import Visualizer

print("============================================================")

visualizer = Visualizer()

# sentence = "Je veux passer par Bucy le Long. Je veux aller à Abergement le Petit depuis Viodos Abense de Bas en passant par Marseille, mais je veux éviter Chauny. Je voudrais aussi passer par Bourguignon sous Coucy."

city_1 = "Bucy le Long"
city_2 = "Abergement le Petit"
city_3 = "Viodos Abense de Bas"
city_4 = "Marseille"
city_5 = "Chauny"
city_6 = "Paris gare de lyon"

sentence = f"De {city_6} à {city_2}."

inferences = visualizer.pipeline(sentence)

for res in inferences:
    closest_train_station = CityToTrainHelper.get_closest_train_station(res["city"])
    res["train_station"] = closest_train_station["train_station"]
    res["city"] = closest_train_station["name"]

print(inferences)