import os
import sys

import pandas as pd
from tqdm import tqdm

src_dir = os.path.join(os.getcwd(), "..", "..")

sys.path.append(os.path.abspath(src_dir))

from src.helpers.city_to_train_station import CityToTrainHelper
from src.utils.visualizer import Visualizer

print("============================================================")

visualizer = Visualizer()

dataset_name = "test3_train_station"
csv = pd.read_csv(f"../../../data/dataset/test/{dataset_name}.csv")

results = []

with tqdm(total=len(csv)) as pbar:
    for idx, row in csv.iterrows():
        inferences = visualizer.pipeline(row.sentence)
        evaluation = True

        for res in inferences:
            search_result = CityToTrainHelper.fuzzy_search(res["place"])
            closest_train_station = CityToTrainHelper.get_closest_train_station(search_result["name"])
            res["train_station"] = closest_train_station
            res["place"] = search_result["name"]

        content = {
            "sentence": row.sentence,
            "departure": row.departure,
            "arrival": row.arrival,
            "intermediary_1": row.get("intermediary_1"),
            "intermediary_2": row.get("intermediary_2"),
            "none": row.get("none"),
        }

        for res in inferences:
            if res["status"] == "departure" :
                content["infer_departure"] = res["place"]
                if row.get("departure") is None:
                    evaluation = False
                evaluation = res["place"] == row.departure if evaluation else False
                continue
        
            if res["status"] == "arrival" :
                content["infer_arrival"] = res["place"]
                if row.get("arrival") is None:
                    evaluation = False
                evaluation = res["place"] == row.arrival if evaluation  else False
                continue

            if res["status"] == 'intermediary':
                if content.get("infer_intermediary_1") is None:
                    content["infer_intermediary_1"] = res["place"]
                elif content.get("infer_intermediary_2") is None:
                    content["infer_intermediary_2"] = res["place"]
                else:
                    content["infer_intermediary_3"] = res["place"]
                    evaluation = False
                continue

            if res["status"] == "none" :
                content["infer_none"] = res["place"]
                if row.get("none") is None:
                    evaluation = False
                evaluation = res["place"] == row.none if evaluation else False
                continue

        if content.get("infer_intermediary_1"):
            all_intermediaries = [row.get("intermediary_1"), row.get("intermediary_2")]
            if content["infer_intermediary_1"] not in all_intermediaries:
                evaluation = False
        if content.get("infer_intermediary_2"):
            all_intermediaries = [row.get("intermediary_1"), row.get("intermediary_2")]
            if content["infer_intermediary_2"] not in all_intermediaries:
                evaluation = False

        if content.get("infer_departure") is None:
            evaluation = False
        if content.get("infer_arrival") is None:
            evaluation = False

        content["evaluation"] = evaluation

        results.append(content)

        pbar.update(1)

df = pd.DataFrame(results)
df.to_csv(f"../../processed/test_results/{dataset_name}_results.csv", index=False)