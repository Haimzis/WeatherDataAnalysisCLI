#!/usr/bin/env python3
import argparse
from datetime import date

from WeatherCLI.stats_exports import ExportType, ResultsExporter
from WeatherCLI.stats_calculation import WeatherStatsCalculator, CalculationType
from WeatherCLI.weather_data_query import WeatherDataQuery
from WeatherCLI.bucket_meta_data import BucketWeatherMetaData
from WeatherCLI.input_utils import DatesFilter
from WeatherCLI.logger import logger


def parse_arguments():
    parser = argparse.ArgumentParser(description='Analyze weather data from remote server.')

    # Add arguments for user input
    parser.add_argument('--stations', nargs='+', default=None,
                        help='List of station ids to be analyzed. Default is all stations.')
    parser.add_argument('--metric', choices=['PRCP', 'TAVG'], required=True,
                        help='Type of metric to be analyzed. Required argument.')
    parser.add_argument('--start-date', type=date.fromisoformat, required=True, help='Start date in yyyy-mm-dd format.')
    parser.add_argument('--end-date', type=date.fromisoformat, required=True, help='End date in yyyy-mm-dd format.')
    parser.add_argument('--filter', choices=['mondays-only'], default=None,
                        help='Type of filter to be applied on the data.')
    parser.add_argument('--calculation', type=CalculationType, choices=CalculationType, default=CalculationType.AVERAGE,
                        help='Type of calculation to be applied on the data. Default is average.')
    parser.add_argument('--export_type', type=ExportType, choices=ExportType, default=ExportType.CSV.value,
                        help='Type of output to be generated. Default is csv.')
    parser.add_argument('--output_path', type=str, default='results/', help='Output directory path')
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    logger.info(f'Parsed arguments: {args}')
    # Bucket content selection
    day_filter = 0 if args.filter == 'mondays-only' else None
    existing_weather_records_files_keys = BucketWeatherMetaData.get_weather_csv_keys()
    logger.info(f'Found {len(existing_weather_records_files_keys)} CSVs files on S3')
    filtered_records_files_keys_by_dates_range = DatesFilter.filter_existing_keys_by_dates_range(
        existing_weather_records_files_keys,
        args.start_date, args.end_date,
        day_filter)
    logger.info(f'Selected {len(filtered_records_files_keys_by_dates_range)} CSVs files by the given filters')
    # Data grabbing & filtering from the bucket
    queried_data = WeatherDataQuery.query(args.stations, filtered_records_files_keys_by_dates_range, args.metric)
    logger.info(f'Found {len(queried_data)} records by the DataQuery object')
    # Desired stat calculation
    calculation_output = WeatherStatsCalculator.calculate_stats(queried_data, calculation_type=args.calculation)
    logger.info(f'Calculated the {args.calculation.value}')
    # Find stations names and add them to the dataframe
    selected_stations_names = BucketWeatherMetaData.get_weather_stations_names(stations_list=args.stations, year=2021)
    merged_df = calculation_output.merge(selected_stations_names, how='left', left_on='station_id', right_on='id').drop(
        'id', axis=1)
    logger.info(f"Found {merged_df['name'].count()}/{len(merged_df)} stations names in the meta-data")
    # Stats Export
    results_exporter = ResultsExporter(args.output_path)
    results_exporter.export_stats(merged_df, args.calculation, args.metric, args.export_type)
    logger.info(f"Query completed.")


if __name__ == '__main__':
    main()

