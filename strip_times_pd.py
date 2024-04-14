import argparse
import csv
from pathlib import Path
from typing import List, Dict, Any

import pendulum
from loguru import logger as log


def load_data(file_path: Path) -> List[Dict[str, Any]]:
    log.info(f"Loading data from {file_path}")
    with open(file_path, encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file)
        data = list(reader)
        reader.fieldnames = handle_duplicate_column_names(list(reader.fieldnames))
    return data


def handle_duplicate_column_names(columns: List[str]) -> List[str]:
    seen = {}
    for idx, column in enumerate(columns):
        if column in seen:
            seen[column] += 1
            columns[idx] = f"{column}_{seen[column]}"
        else:
            seen[column] = 0
    return columns


def sort_data_by_time(data: List[Dict[str, Any]], time_column: str) -> List[Dict[str, Any]]:
    log.info("Sorting data by time...")
    for row in data:
        row[time_column] = pendulum.parse(row[time_column], strict=False)
    return sorted(data, key=lambda x: x[time_column])


def filter_data(data: List[Dict[str, Any]], entity_id_column: str, time_column: str) -> List[Dict[str, Any]]:
    last_entry = {}
    filtered = []
    for row in data:
        entity_id = row[entity_id_column]
        time = row[time_column]
        if entity_id not in last_entry or time > last_entry[entity_id][time_column]:
            last_entry[entity_id] = row
            filtered.append(row)
    return filtered


def save_data(data: List[Dict[str, Any]], file_path: Path) -> None:
    log.info(f"Saving data to {file_path}")
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Filter CSV files to only include one row per entity ID per 5-minute interval.")
    parser.add_argument("input", nargs='+', type=str,
                        help="Paths to input CSV files or directories containing CSV files")
    parser.add_argument("--time_column", type=str, default="timestamp", help="Name of the column containing time data")
    parser.add_argument("--entity_id_column", type=str, default="entity_id",
                        help="Name of the column containing entity ID data")
    return parser.parse_args()


def find_csv_files(paths: List[str]) -> List[Path]:
    csv_files = []
    for path in paths:
        p = Path(path)
        if p.is_dir():
            csv_files.extend([f for f in p.rglob('*.csv') if 'strip-time' not in f.stem])
        elif p.is_file() and 'strip-time' not in p.stem:
            csv_files.append(p)
        else:
            log.warning(f"Path {p} is neither a file nor a directory.")
    return csv_files


def main():
    args = parse_arguments()
    csv_files = find_csv_files(args.input)
    log.debug(f"Found {len(csv_files)} CSV files")
    log.debug(f"Filtering columns: {args.entity_id_column} by {args.time_column}")
    for csv_file in csv_files:
        log.info(f"Processing {csv_file}")
        data = load_data(csv_file)
        data = sort_data_by_time(data, args.time_column)
        data = filter_data(data, args.entity_id_column, args.time_column)
        output_file = csv_file.with_stem(f"{csv_file.stem}-strip-time")
        save_data(data, output_file)


if __name__ == "__main__":
    import sys

    sys.argv.append("test")
    sys.argv.append('--time_column')
    sys.argv.append('Event Time')
    sys.argv.append('--entity_id_column')
    sys.argv.append('Entity Id')
    main()
