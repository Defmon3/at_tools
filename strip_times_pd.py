import argparse
from pathlib import Path

import pandas as pd
from loguru import logger as log


def load_data(file_path: Path) -> pd.DataFrame:
    log.info("Loading data from {}", file_path)
    data = pd.read_csv(file_path)
    data.columns = handle_duplicate_column_names(data.columns)
    return data


def handle_duplicate_column_names(columns):
    seen = {}
    for idx, column in enumerate(columns):
        if column in seen:
            seen[column] += 1
            columns[idx] = f"{column}_{seen[column]}"
        else:
            seen[column] = 0
    return columns


def preprocess_data(data: pd.DataFrame, time_column: str) -> pd.DataFrame:
    log.info("Preprocessing data...")
    data[time_column] = pd.to_datetime(data[time_column])
    data = data.sort_values(time_column)
    return data


def filter_data(data: pd.DataFrame, entity_id_column: str, time_column: str) -> pd.DataFrame:
    log.info("Filtering data...")
    data.set_index(time_column, inplace=True)
    data = data.groupby(entity_id_column).resample('5T').first().reset_index(level=0, drop=True)
    return data


def save_data(data: pd.DataFrame, file_path: Path):
    log.info("Saving filtered data to {}", file_path)
    data.to_csv(file_path)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Filter CSV files to only include one row per entity ID per 5-minute interval.")
    parser.add_argument("input", nargs='+', type=str,
                        help="Paths to input CSV files or directories containing CSV files")
    parser.add_argument("--time_column", type=str, default="timestamp", help="Name of the column containing time data")
    parser.add_argument("--entity_id_column", type=str, default="entity_id",
                        help="Name of the column containing entity ID data")
    return parser.parse_args()


def find_csv_files(paths: list[str]) -> list[Path]:
    csv_files = []
    for path in paths:
        p = Path(path)
        if p.is_dir():
            csv_files.extend(p.rglob('*.csv'))
        elif p.is_file():
            csv_files.append(p)
        else:
            log.warning("Path {} is neither a file nor a directory.", p)
    return csv_files


def main():
    args = parse_arguments()
    csv_files = find_csv_files(args.input)
    log.debug(f"Filtering columns: {args.entity_id_column} by {args.time_column}")
    for csv_file in csv_files:
        log.info("Processing {}", csv_file)
        data = load_data(csv_file)
        data = preprocess_data(data, args.time_column)
        data = filter_data(data, args.entity_id_column, args.time_column)
        output_file = csv_file.with_stem(f"{csv_file.stem}-strip-time")
        save_data(data, output_file)


if __name__ == "__main__":
    main()
