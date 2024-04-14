import argparse
import csv
from datetime import datetime, timedelta
from pathlib import Path


def parse_event_time(time_str: str):
    """Parse the 'Event Time' string to a datetime object."""
    return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f")


def should_include_record(current_time, last_time, interval_minutes=5):
    """Determine if the current record should be included based on the time interval."""
    if last_time is None:
        return True
    interval = timedelta(minutes=interval_minutes)
    return (current_time - last_time) >= interval


def process_csv_file(file_path):
    """Process a single CSV file to strip times."""
    output_file_path = file_path.with_name(f"{file_path.stem}-time-strip.csv")
    with open(file_path, newline='') as file, open(output_file_path, mode='w', newline='') as output_file:
        reader = csv.DictReader(file)
        writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames)
        writer.writeheader()

        # Reading all data and grouping by Entity Id
        entries = {}
        for row in list(reader):
            entity_id = row['Entity Id']
            if entity_id not in entries:
                entries[entity_id] = []
            entries[entity_id].append(row)

        # Sorting and filtering each group
        last_times = {}
        for entity_id, rows in entries.items():
            sorted_rows = sorted(rows, key=lambda x: parse_event_time(x['Event Time']))
            for row in sorted_rows:
                event_time = parse_event_time(row['Event Time'])
                if should_include_record(event_time, last_times.get(entity_id)):
                    writer.writerow(row)
                    last_times[entity_id] = event_time


def process_target(target_path):
    """Process each CSV file found at the target path."""
    path = Path(target_path)
    if path.is_file():
        process_csv_file(path)
    else:
        for file_path in path.rglob('*.csv'):
            process_csv_file(file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Strip time from CSV data.")
    parser.add_argument("target", help="Path to file or directory")
    args = parser.parse_args()

    process_target(args.target)
    print(f"Processed data saved to {args.target.replace('.csv', '-time-strip.csv')}")
