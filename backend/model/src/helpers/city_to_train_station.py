import numpy as np
import pandas as pd
from rapidfuzz import process


class CityToTrainHelper:
    # train_station_df = pd.read_csv('../data/liste-des-gares.csv', sep=';')
    # cities_df = pd.read_csv('../data/cities.csv')
    # all_names_df = pd.read_csv('../data/cities_and_train_stations.csv')
    cities_df = pd.read_csv('./data/cities.csv')
    all_names_df = pd.read_csv('./data/cities_and_train_stations.csv')

    def __haversine_vectorized(lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
        c = 2 * np.arcsin(np.sqrt(a))

        r = 6371

        distance = c * r
        return distance

    # @classmethod
    # def calculate_nearest_station(cls, city_name):
    #     train_station_df = pd.read_csv('../../../data/liste-des-gares.csv', sep=';')
    #     city = cls.cities_df.loc[cls.cities_df["label"] == city_name]

    #     if city.empty:
    #         print("City not found")
    #         return 

    #     coord_1 = (city["latitude"].values[0], city["longitude"].values[0])

    #     cls.train_station_df[['lat', 'lon']] = cls.train_station_df['C_GEO'].str.split(',', expand=True).astype(float)

    #     cls.train_station_df['distance'] = cls.__haversine_vectorized(
    #         coord_1[0], coord_1[1],
    #         cls.train_station_df['lat'].values, cls.train_station_df['lon'].values
    #     )

    #     distance_df = cls.train_station_df[['distance', 'LIBELLE']].copy()
    #     return distance_df.loc[distance_df["distance"].min() == distance_df["distance"]]

    @classmethod
    def fuzzy_search(cls, name):
        name = name.lower().replace("-", " ")
        result_df = []

        result_label = process.extractOne(name, cls.all_names_df["label"].values)
        result_region = process.extractOne(name, cls.all_names_df["region"].values)
        result_department = process.extractOne(name, cls.all_names_df["department"].values)

        result_df.append(
            {"name": result_label[0], "score": result_label[1], "class_name": "city"}
        )

        result_df.append(
            {"name": result_region[0], "score": result_region[1], "class_name": "region"}
        )
        
        result_df.append(
            {"name": result_department[0], "score": result_department[1], "class_name": "department"}
        )

        result_df = pd.DataFrame(result_df)

        if not result_df.empty:
            best_result = result_df.loc[result_df["score"].idxmax()]
            return {
                "name": best_result["name"],
                "class_name": best_result["class_name"]
            }
        else:
            return None

    @classmethod
    def __get_department(cls, name):
        entity = cls.all_names_df.loc[
            cls.all_names_df["department"] == name
        ]

        if entity.empty:
            return None

        response = entity.groupby("nearest_train_station").value_counts().sort_values(ascending=False).idxmax()
        return response[6]

    @classmethod
    def __get_region(cls, name):
        entity = cls.all_names_df.loc[
            cls.all_names_df["region"] == name
        ]

        if entity.empty:
            return cls.__get_department(name) 

        response = entity.groupby("nearest_train_station").value_counts().sort_values(ascending=False).idxmax()
        return response[6]

    @classmethod
    def get_closest_train_station(cls, name):
        entity = cls.all_names_df.loc[
            cls.all_names_df["label"] == name
        ]

        if entity.empty:
            return cls.__get_region(name)
        if (entity["class_name"].values[0] == "train_station"):
            return name

        return entity["nearest_train_station"].values[0]
