from enum import Enum
import pandas as pd

from WeatherCLI import config


class CalculationType(Enum):
    AVERAGE = 'average'
    MIN = 'min'
    MEDIAN = 'median'
    AVERAGE_DIFFERENCE = 'average_difference'


class WeatherStatsCalculator:
    @classmethod
    def calculate_stats(cls, weather_stations_data_df: pd.DataFrame, calculation_type: CalculationType) -> pd.DataFrame:
        """
        Calculate weather statistics based on the selected calculation type.

        Args:
            weather_stations_data_df (pd.DataFrame): A pandas DataFrame containing the weather data to be analyzed.
            calculation_type (CalculationType): An instance of the CalculationType enum representing the type of calculation to perform.

        Returns:
            pd.DataFrame: A DataFrame containing the calculated statistics.
        """
        # Define the column names used for grouping and calculating the stats
        GROUP_BY_COL = 'station_id'
        VALUE_COL = 'value'

        # Initialize the variable to store the calculated stats
        stats_series = None

        # Group the weather data by station_id
        grouped_stations_by_id = weather_stations_data_df.groupby(GROUP_BY_COL)

        # Calculate the stats based on the selected calculation type
        if calculation_type is CalculationType.MIN:
            stats_series = grouped_stations_by_id[VALUE_COL].min()

        elif calculation_type is CalculationType.AVERAGE:
            stats_series = grouped_stations_by_id[VALUE_COL].mean()

        elif calculation_type is CalculationType.AVERAGE_DIFFERENCE:
            global_avg = grouped_stations_by_id['global_values_sum'].sum() / grouped_stations_by_id[
                'global_values_counter'].sum()
            stations_avg = grouped_stations_by_id[VALUE_COL].mean()
            stats_series = abs(stations_avg - global_avg)

        elif calculation_type is CalculationType.MEDIAN:
            stats_series = grouped_stations_by_id[VALUE_COL].median()

        # Convert the stats from a Series to a DataFrame and rename the last column
        stats_df = stats_series.reset_index(name=config.CALCULATION_STAT_COL_NAME)
        return stats_df
