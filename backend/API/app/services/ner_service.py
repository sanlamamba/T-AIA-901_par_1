from model.src.helpers.city_to_train_station import CityToTrainHelper
from model.src.utils.visualizer import Visualizer


def extract_entities(text):
    """
    Extract named entities from the given text.
    Placeholder implementation; replace with actual NER logic.
    """

    visualizer = Visualizer()
    inferences = visualizer.pipeline(text)

    for res in inferences:
        search_result = CityToTrainHelper.fuzzy_search(res["place"])
        closest_train_station = CityToTrainHelper.get_closest_train_station(
            search_result["name"]
        )
        res["train_station"] = closest_train_station
        res["place"] = search_result["name"]

    response = []

    for item in inferences:
        new_item = {}
        for key, value in item.items():
            if key == "status" and value == "departure":
                new_item["status"] = "start"
            elif key == "status" and value == "arrival":
                new_item["status"] = "end"
            elif key == "status" and value == "intermediary":
                new_item["status"] = "intermediate"
            elif key == "train_station":
                new_item["station"] = value
        response.append(new_item)

    return response
