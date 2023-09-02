# Script: Read CSV Files and Analyze Trades

This script reads CSV files containing financial data and analyzes random trades based on the data. It calculates the profitability of the trades and provides a summary of the results.

## Prerequisites

- Python 3.x
- Required packages: `datetime`, `numpy`, `os`, `pandas`, `random`, `multiprocessing`

## Usage

1. Clone the repository or download the script file.
2. Update the `csv_dir` variable in the script to specify the directory containing the CSV files to be analyzed.
3. Run the script using `python rndmtrd.py`.

## Description

The script performs the following steps:

1. Imports the necessary libraries and modules.
2. Defines the list of column names for the CSV files.
3. Sets up logging.
4. Retrieves the list of CSV files in the specified directory.
5. Defines a function to read a CSV file in parallel.
6. Reads the CSV files in parallel using multiprocessing.
7. Concatenates the data from all the CSV files into a single array.
8. Selects a random subset of trades from the concatenated array.
9. Initializes variables to track profits, losses, trade exits, and unfinished trades.
10. Iterates over the random trades and analyzes each trade.
11. Calculates the profit and loss percentages for each trade.
12. Updates the profit and loss counters based on the calculated percentages.
13. Determines the exit point of each trade.
14. Prints the summary of the trade analysis, including the number of profitable trades, losing trades, unfinished trades, profit percentage, loss percentage, and total profit.
15. Logs the completion of the script.

## Note

- The script assumes that the CSV files contain financial data with columns in the specified order: 'Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'.
- The script uses multiprocessing to read the CSV files in parallel, which can significantly speed up the process for large datasets.
- The script randomly selects a subset of trades for analysis to demonstrate the functionality. Adjust the `random_trades` variable to analyze a different number of trades or modify the logic to select trades based on specific criteria.
- The script calculates the profit and loss percentages based on predefined thresholds (`profit_percent` and `loss_percent`). Modify these values to customize the analysis according to your requirements.