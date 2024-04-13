#!/usr/bin/env python3
"""Extracts entity IDs from all files in a directory."""
import argparse
import csv
import zipfile
from pathlib import Path
from typing import Iterable


def main(directory: str, clean: bool) -> None:
    """Main function to process the directory."""
    target = Path(directory)

    if not target.exists():
        print(f"Directory '{directory}' does not exist.")
        return

    if clean:
        remove_csvs(target)

    z_files: Iterable[Path] = Path(target).rglob('*.zip')

    for zip_file in z_files:
        extract_zip(zip_file, target)

    parse_files(target)


def remove_csvs(target: Path) -> None:
    """Remove all CSV files in the specified directory."""
    for csv_file in target.rglob("*.csv"):
        csv_file.unlink()


def extract_zip(z_file: Path, target: Path) -> None:
    with zipfile.ZipFile(z_file) as zip_ref:
        zip_ref.extractall(target)


def parse_files(target: Path) -> None:
    entity_ids = set()
    csv_files = target.rglob('*.csv')

    if not csv_files:
        print(f"No CSV files found in '{target.name}'.")
        return

    for csv_file in csv_files:
        with open(csv_file.absolute(), newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            entity_ids.update({row['Entity Id'] for row in rows if row.get('Entity Id')})

    # Create the combined CSV file
    output_file = Path(target / "eid-ss.txt")
    print("#################### SEARCH STRING ####################\n")
    with open(output_file, 'w', newline='') as textfile:
        for n, eid in enumerate(entity_ids):
            if n == len(entity_ids) - 1:
                textfile.write(f"entity_id:{eid}")
                print(f"entity_id:{eid}")
            else:
                textfile.write(f"entity_id:{eid}  OR \n")
                print(f"entity_id:{eid}  OR ")
    print("\n#################### SEARCH STRING END ####################")
    print(f"Combined CSV files successfully written to '{output_file}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract entity IDs from CSV files and generate a search string for lighthouse.")
    parser.add_argument('csv_dir', metavar='directory', type=str,
                        help='Directory containing CSV files to parse.')
    parser.add_argument("--clean", action="store_true", help="Clean old CSV files before processing")

    args = parser.parse_args()

    main(args.csv_dir, args.clean)
