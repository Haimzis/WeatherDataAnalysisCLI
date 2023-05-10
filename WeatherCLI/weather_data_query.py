from typing import List, Set
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

from WeatherCLI import config
from WeatherCLI.logger import logger


class WeatherDataQuery:
    @staticmethod
    def _filter_data_by_metric(chunk: pd.DataFrame, metric: str) -> pd.Series:
        return chunk[chunk['metric'] == metric]['value']

    @staticmethod
    def _filter_data_by_query_args(chunk: pd.DataFrame, stations_list: List[str], metric: str) -> pd.DataFrame:
        return chunk[(chunk['station_id'].isin(stations_list)) & (chunk['metric'] == metric)]

    @staticmethod
    def _retrieve_data_from_content(content_path: str, stations_list: List[str], metric: str) -> pd.DataFrame:
        """Retrieve data from a CSV file and filter by station IDs and metric - while doing it in chunks.

        Args:
            content_path: The url to the CSV file containing the data.
            stations_list: A list of station IDs used for filtering.
            metric: The metric used for filtering.

        Returns:
            A filtered DataFrame containing the station IDs, values, and global values sum and counter.
        """

        filtered_data = []
        metric_values_sum = 0
        num_metric_values = 0
        chunk_size = config.CHUNK_SIZE  # Number of rows to read per chunk

        # Use chunked reading to avoid loading large files into memory
        for chunk in pd.read_csv(content_path, chunksize=chunk_size):
            filtered_chunk_by_metric = WeatherDataQuery._filter_data_by_metric(chunk, metric)
            filtered_chunk_by_query = WeatherDataQuery._filter_data_by_query_args(chunk, stations_list, metric)

            if len(filtered_chunk_by_query) > 0:
                filtered_data.append(filtered_chunk_by_query)

            metric_values_sum += filtered_chunk_by_metric.to_numpy().sum()
            num_metric_values += len(filtered_chunk_by_metric)

        # Concatenate the filtered dataframes and add global sum and counter columns
        filtered_df_from_csv = pd.concat(filtered_data)
        filtered_df_from_csv['global_values_sum'] = metric_values_sum
        filtered_df_from_csv['global_values_counter'] = num_metric_values
        filtered_df_from_csv = filtered_df_from_csv[['station_id', 'value', 'global_values_sum', 'global_values_counter']]

        return filtered_df_from_csv

    @classmethod
    def query(cls, stations_list: List[str], filtered_contents: Set[str], metric: str) -> pd.DataFrame:
        """
        Query the data for the specified stations, metrics, and filtered contents.
        """
        urls = [f'{config.BUCKET_URL}{key}' for key in filtered_contents]

        with ThreadPoolExecutor(max_workers=config.MAX_WORKERS) as pool:
            logger.info(f"Using {config.MAX_WORKERS} workers for CSVs reading")
            # Use concurrent.futures.ThreadPoolExecutor for parallel execution
            filtered_dfs_list = list(pool.map(lambda url: WeatherDataQuery._retrieve_data_from_content(url, stations_list, metric), urls))
            accumulated_filtered_df = pd.concat(filtered_dfs_list, axis=0)

            return accumulated_filtered_df
