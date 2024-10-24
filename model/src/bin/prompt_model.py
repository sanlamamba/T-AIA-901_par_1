import os
import sys

src_dir = os.path.join(os.getcwd(), "..", "..")

sys.path.append(os.path.abspath(src_dir))

from src.helpers.city_to_train_station import VisualizerHelper
from src.utils.visualizer import Visualizer

print("============================================================")

visualizer = Visualizer()

# sentence = "Je veux passer par Bucy le Long. Je veux aller à Abergement le Petit depuis Viodos Abense de Bas en passant par Marseille, mais je veux éviter Chauny. Je voudrais aussi passer par Bourguignon sous Coucy."

city_1 = "Bucy le Long"
city_2 = "Abergement le Petit"
city_3 = "Viodos Abense de Bas"
city_4 = "Marseille"
city_5 = "Chauny"
city_6 = "Bourguignon sous Coucy"

sentence = f"Je souhaite aller de {city_1} à {city_2}."

inferences = visualizer.pipeline(sentence)

for res in inferences:
    train_station = VisualizerHelper.get_nearest_station(res["city"])
    res["Train station"] = train_station["LIBELLE"].values[0]

print(inferences)