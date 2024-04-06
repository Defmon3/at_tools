#!/usr/bin/env python3
"""Extracts entity IDs from a list of CSV files and generates a search string for lighthouse."""
import argparse
import csv
from typing import Iterable


def files_to_parse(file_list: Iterable[str]) -> None:
    """Extracts entity IDs from a list of CSV files and generates a search string for lighthouse.

    Args:
        :param field: Field to extract from the CSV files.
        :param file_list: List of CSV file paths.
    Returns:
        :return: None

    """
    if not file_list:
        print("No files to parse.")
        return

    entity_ids = set()
    for file_path in file_list:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            entity_ids.update({row['Entity Id'] for row in rows if row.get('Entity Id')})

    # Create the combined CSV file
    output_file = "entity_id_search_string.txt"
    with open(output_file, 'w', newline='') as textfile:
        for n, eid in enumerate(entity_ids):
            if n == len(entity_ids) - 1:
                textfile.write(f"entity_id:{eid} OR \n")
            else:
                textfile.write(f"entity_id:{eid} ")

    print(f"Combined CSV files successfully written to '{output_file}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine CSV files with compatible data structures.")
    parser.add_argument('csv_files', metavar='file', type=str, nargs='+',
                        help='CSV files to combine')
    args = parser.parse_args()

    files_to_parse(args.csv_files)
