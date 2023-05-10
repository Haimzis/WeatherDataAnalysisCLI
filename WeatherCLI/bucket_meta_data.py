import re
from typing import List

import pandas as pd
import requests
import xmltodict

from WeatherCLI import config


class BucketWeatherMetaData:
    _WEATHER_CSV_KEY_PATTERN = r'weather_data/weather_data_\d{4}-\d{2}-\d{2}\.csv'

    @classmethod
    def get_weather_csv_keys(cls) -> List[str]:
        """
        Retrieves the list of keys for weather CSV files from the bucket URL.
        :return: A list of keys for weather CSV files.
        """
        # Send a GET request to the bucket URL to retrieve the contents of the bucket
        response = requests.get(config.BUCKET_URL)
        content_dict = xmltodict.parse(response.content)
        contents = content_dict['ListBucketResult']['Contents']

        weather_data = []

        # Loop through each item in the contents and check if it matches the weather CSV key pattern
        for item in contents:
            key = item['Key']
            size = int(item['Size'])
            if re.match(cls._WEATHER_CSV_KEY_PATTERN, key) and size > 0:
                weather_data.append(key)

        # Return the list of weather CSV file keys
        return weather_data

    @classmethod
    def get_weather_stations_names(cls, stations_list: List[str], year: int = 2021) -> pd.DataFrame:
        """
        Retrieves the names of the weather stations in the given stations list and year.

        :param stations_list: A list of weather station IDs to retrieve names for.
        :param year: The year to retrieve the weather station metadata for (default: 2021).
        :return: A pandas DataFrame containing the weather station IDs and names.
        """
        # Initialize an empty list to store the chunks of weather station metadata
        names = []

        # Loop through each chunk of the weather station metadata CSV file
        for chunk in pd.read_csv(cls._get_weather_meta_data_path(year), chunksize=config.CHUNK_SIZE):
            # Filter the chunk by the station_id
            filtered_chunk = chunk[chunk['id'].isin(stations_list)]
            # Append the filtered chunk to the list
            names.append(filtered_chunk)

        # Concatenate all the chunks and return the weather station IDs and names
        return pd.concat(names)[['id', 'name']]

    @classmethod
    def _get_weather_meta_data_path(cls, year: int) -> str:
        return config.BUCKET_URL + 'weather_data/{}_weather_stations.csv'.format(year)
