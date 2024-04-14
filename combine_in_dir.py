#!/usr/bin/env python3

import argparse
import csv
from pathlib import Path


def combine_csv_files(target_dir: str) -> None:
    """Combines multiple CSV files with potentially different headers into a single file.

    Args:
        target_dir (list): A list of CSV file paths.

    Returns:
        None (writes the combined data to a new CSV file)
    """

    all_fields = set()  # Collect all unique fields
    data_rows = []
    csv_files = Path(target_dir).rglob('*.csv')
    # Collect fields and data from each file
    for file_path in csv_files:
        with open(file_path.absolute(), newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            all_fields.update(reader.fieldnames)  # Add fields to the master set

            # Store data rows for later writing
            data_rows.extend(list(reader))

    # Create the combined CSV file
    output_file = "combined.csv"
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(all_fields))
        writer.writeheader()  # Write the comprehensive header row

        # Write data rows, filling in missing fields with blanks
        for row in data_rows:
            writer.writerow({field: row.get(field, '') for field in all_fields})

    print(f"Combined CSV files successfully written to '{output_file}'")


if __name__ == "__main__":
    # Argument parsing for command-line usage
    parser = argparse.ArgumentParser(description="Combine CSV files with compatible data structures.")
    parser.add_argument('target', metavar='file', type=str,
                        help='CSV files to combine')
    args = parser.parse_args()

    combine_csv_files(args.target)
