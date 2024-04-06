#!/usr/bin/env python3
"""Extracts entity IDs from all files in a directory."""
import argparse
import csv
import os.path


def files_to_parse(csv_dir: str) -> None:
    """Extracts entity IDs from a list of CSV files and generates a search string for lighthouse.

    Args:
        :param csv_dir: Path do directory containing CSV files
    Returns:
        :return: None

    """
    if not os.path.exists(csv_dir):
        print(f"Directory '{csv_dir}' does not exist.")
        return

    entity_ids = set()
    csv_files = [file for file in os.listdir(csv_dir) if file.endswith('.csv')]

    if not csv_files:
        print(f"No CSV files found in '{csv_dir}'.")
        return

    for file_name in csv_files:
        full_path = os.path.join(csv_dir, file_name)
        with open(full_path, newline='', encoding='utf-8') as csvfile:
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
    parser = argparse.ArgumentParser(
        description="Extract entity IDs from CSV files and generate a search string for lighthouse.")
    parser.add_argument('csv_dir', metavar='directory', type=str,
                        help='Directory containing CSV files to parse.')
    args = parser.parse_args()

    files_to_parse(args.csv_dir)
