import os
from enum import Enum
import pandas as pd
import matplotlib.pyplot as plt
from WeatherCLI.logger import logger

from WeatherCLI import config
from WeatherCLI.stats_calculation import CalculationType


class ExportType(Enum):
    PLOT = 'bar_plot'
    CSV = 'csv'


class ResultsExporter:
    def __init__(self, output_dir: str = config.DEFAULT_OUTPUT_DIR):
        self._output_dir = output_dir
        self._create_output_dir()

    def export_stats(self, stats_df: pd.DataFrame, calculation_type: CalculationType, metric_name: str,
                     export_type: ExportType = ExportType.CSV):
        """
        Exports the statistics data to the specified output type.

        Args:
            stats_df (pd.DataFrame): A pandas DataFrame containing the statistics data.
            calculation_type (CalculationType): The type of calculation that was performed on the data.
            export_type (ExportType): The type of output to export. Defaults to ExportType.CSV.
            metric_name (string): PRCP/TAVG
        """
        if export_type is ExportType.CSV:
            # Export the stats as a CSV file
            stats_df.to_csv(os.path.join(self._output_dir, config.OUTPUT_CSV_NAME.format(calculation_type.value)), index=False,
                            na_rep='NaN')

        elif export_type is ExportType.PLOT:
            is_there_missing_names = stats_df['name'].isna().any()
            if is_there_missing_names:
                logger.warning("Some stations names are missing, the stations ids will be used instead")
            x_axis_name = 'station_id' if is_there_missing_names else 'name'
            # Replace missing station names with 'Unknown'
            stats_df['name'].fillna(x_axis_name, inplace=True)

            # Plot the stats as a bar chart
            # TODO: For some stations ids the name is missing - need to validate with Alon.
            stats_df.plot(x=x_axis_name, y=config.CALCULATION_STAT_COL_NAME, kind='bar')
            plt.title(calculation_type.value + '/' + metric_name + f"({'mm' if metric_name == 'PRCP' else '1/10 Celsius'})")
            plt.ylabel(config.CALCULATION_STAT_COL_NAME)
            plt.xticks(rotation=0)
            plt.show()

    def _create_output_dir(self):
        """
        Creates the output directory if it doesn't already exist.
        """
        if not os.path.isdir(self._output_dir):
            os.mkdir(self._output_dir)
