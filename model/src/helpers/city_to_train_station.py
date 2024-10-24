import os

import numpy as np
import pandas as pd


class VisualizerHelper:
    train_station_df = pd.read_csv('../../../data/liste-des-gares.csv', sep=';')
    cities_df = pd.read_csv('../../../data/cities.csv')

    @staticmethod
    def __haversine_vectorized(lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
        c = 2 * np.arcsin(np.sqrt(a))

        r = 6371

        distance = c * r
        return distance

    @classmethod
    def get_nearest_station(cls, city_name):
        city = cls.cities_df.loc[cls.cities_df["label"] == city_name]

        if city.empty:
            print("City not found")
            return 

        coord_1 = (city["latitude"].values[0], city["longitude"].values[0])

        cls.train_station_df[['lat', 'lon']] = cls.train_station_df['C_GEO'].str.split(',', expand=True).astype(float)

        cls.train_station_df['distance'] = VisualizerHelper.__haversine_vectorized(
            coord_1[0], coord_1[1],
            cls.train_station_df['lat'].values, cls.train_station_df['lon'].values
        )

        distance_df = cls.train_station_df[['distance', 'LIBELLE']].copy()
        return distance_df.loc[distance_df["distance"].min() == distance_df["distance"]]


