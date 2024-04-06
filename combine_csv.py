#!/usr/bin/env python3

import argparse
import csv


def combine_csv_files(file_list):
    """Combines multiple CSV files with potentially different headers into a single file.

    Args:
        file_list (list): A list of CSV file paths.

    Returns:
        None (writes the combined data to a new CSV file)
    """

    all_fields = set()  # Collect all unique fields
    data_rows = []

    # Collect fields and data from each file
    for file_path in file_list:
        with open(file_path, 'r', newline='') as csvfile:
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
    parser.add_argument('csv_files', metavar='file', type=str, nargs='+',
                        help='CSV files to combine')
    args = parser.parse_args()

    combine_csv_files(args.csv_files)
ls nlsearch | tr '\n' ' ' | xargs -I {} python3 combine_csv.py {}
