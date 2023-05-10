# Weather Data Analyzer

This is a Python script that allows you to analyze weather data from a remote server. It retrieves weather data from a bucket, performs calculations and analysis on the data, and exports the results.

## Prerequisites

- Python 3.x
- Required Python packages are given by requirements.txt
- `setup.py` file is provided

## Features
1. Retrieve weather data from a remote server
2. Analyze weather metrics such as precipitation (PRCP) or average temperature (TAVG)
3. Filter data by specific stations, date ranges, or other criteria
4. Calculate statistical measures on the data, including averages, sums, or custom calculations
5. Export the analysis results in CSV or other formats
6. Customizable output directory for the generated results
Command-line interface (CLI) for easy execution and configuration

## Usage

1. Clone the repository or download the script.

2. Run the following command to execute the script:

   ```bash
   python weather_analyzer.py [--stations STATIONS] --metric METRIC --start-date START_DATE --end-date END_DATE [--filter FILTER] [--calculation CALCULATION] [--export_type EXPORT_TYPE] [--output_path OUTPUT_PATH]
   ```

   Replace the arguments in square brackets with your desired values. The required arguments are as follows:

   - `--metric`: Type of metric to be analyzed (PRCP or TAVG).
   - `--start-date`: Start date in yyyy-mm-dd format.
   - `--end-date`: End date in yyyy-mm-dd format.

3. Optional arguments:

   - `--stations STATIONS`: List of station ids to be analyzed. If not provided, all stations will be analyzed.
   - `--filter FILTER`: Type of filter to be applied on the data (mondays-only).
   - `--calculation CALCULATION`: Type of calculation to be applied on the data (average by default).
   - `--export_type EXPORT_TYPE`: Type of output to be generated (csv by default).
   - `--output_path OUTPUT_PATH`: Output directory path (results/ by default).

## Example

To analyze PRCP (precipitation) data from January 1, 2023 to January 31, 2023, you can run the following command:

```bash
python weather_analyzer.py --metric PRCP --start-date 2023-01-01 --end-date 2023-01-31
```

This will analyze the precipitation data for all stations within the specified date range and generate the output in CSV format.
