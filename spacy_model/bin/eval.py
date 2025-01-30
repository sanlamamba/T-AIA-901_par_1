import os
import sys

src_dir = os.path.join(os.getcwd())
sys.path.append(os.path.abspath(src_dir))

import pandas as pd
from config.constants import OUTPUT_MODEL_DIR
from helpers.process_text import process_text
from tqdm import tqdm

if __name__ == "__main__":

    data_type = ["city", "train_station"]
    selected_type = data_type[0]
    version = "3"
    
    dataset_name = f"test{version}_{selected_type}"
    csv = pd.read_csv(f"../data/dataset/test/{dataset_name}.csv")

    results = []

    with tqdm(total=len(csv)) as pbar:
        for idx, row in csv.iterrows():
            evaluation = True

            content = {
                "sentence": row.sentence,
                "departure": row.departure,
                "arrival": row.arrival,
                "intermediary_1": row.get("intermediary_1"),
                "intermediary_2": row.get("intermediary_2"),
                "none": row.get("none"),
            }

            inferences = process_text(row.sentence, OUTPUT_MODEL_DIR)

            for res in inferences:
                if res["status"] == "start" :
                    content["infer_departure"] = res["station"]
                    if row.get("departure") is None:
                        evaluation = False
                    evaluation = res["station"] == row.departure if evaluation else False
                    continue
            
                if res["status"] == "end" :
                    content["infer_arrival"] = res["station"]
                    if row.get("arrival") is None:
                        evaluation = False
                    evaluation = res["station"] == row.arrival if evaluation  else False
                    continue

                if res["status"] == 'intermediary':
                    if content.get("infer_intermediary_1") is None:
                        content["infer_intermediary_1"] = res["station"]
                    elif content.get("infer_intermediary_2") is None:
                        content["infer_intermediary_2"] = res["station"]
                    else:
                        content["infer_intermediary_3"] = res["station"]
                        evaluation = False
                    continue

                if res["status"] == "none" :
                    content["infer_none"] = res["station"]
                    if row.get("none") is None:
                        evaluation = False
                    evaluation = res["station"] == row.none if evaluation else False
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
    df.to_csv(f"../model/processed/test_results/spacy/{dataset_name}_results.csv", index=False)